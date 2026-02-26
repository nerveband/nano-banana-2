#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Batch image generation using Nano Banana 2 (Gemini 3.1 Flash Image).
50% cheaper than standard pricing, with up to 24-hour turnaround.

Usage:
    # Generate from a list of prompts
    uv run batch_generate.py -f prompts.txt -o output_dir/

    # Generate from inline prompts
    uv run batch_generate.py -p "A sunset over mountains" -p "A cat in space" -o output_dir/

    # With aspect ratio and resolution
    uv run batch_generate.py -f prompts.txt -o output_dir/ --aspect 16:9 --resolution 2K

    # Check status of existing job
    uv run batch_generate.py --status JOB_NAME

    # Download results from completed job
    uv run batch_generate.py --download JOB_NAME -o output_dir/
"""

import argparse
import json
import os
import sys
import time
import base64
from pathlib import Path


SUPPORTED_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"
]


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def create_batch_request(prompt: str, key: str, aspect: str | None, resolution: str) -> dict:
    """Create a single batch request entry."""
    gen_config = {"responseModalities": ["TEXT", "IMAGE"]}

    image_config = {"imageSize": resolution}
    if aspect:
        image_config["aspectRatio"] = aspect
    gen_config["imageConfig"] = image_config

    return {
        "key": key,
        "request": {
            "contents": [{"parts": [{"text": prompt}]}],
            "generation_config": gen_config
        }
    }


def submit_batch(client, prompts: list[str], aspect: str | None, resolution: str, display_name: str) -> str:
    """Submit a batch job and return the job name."""
    from google.genai import types

    # Write JSONL file
    jsonl_path = Path("/tmp/nano-banana-2-batch.jsonl")
    with open(jsonl_path, "w") as f:
        for i, prompt in enumerate(prompts):
            key = f"image-{i:04d}"
            req = create_batch_request(prompt, key, aspect, resolution)
            f.write(json.dumps(req) + "\n")

    print(f"Created batch file with {len(prompts)} requests")

    # Upload file
    uploaded_file = client.files.upload(
        file=str(jsonl_path),
        config=types.UploadFileConfig(
            display_name=display_name,
            mime_type="jsonl"
        )
    )
    print(f"Uploaded: {uploaded_file.name}")

    # Create batch job
    batch_job = client.batches.create(
        model="gemini-3.1-flash-image-preview",
        src=uploaded_file.name,
        config={"display_name": display_name}
    )
    print(f"Batch job created: {batch_job.name}")
    print(f"State: {batch_job.state.name}")

    return batch_job.name


def check_status(client, job_name: str):
    """Check and print the status of a batch job."""
    batch_job = client.batches.get(name=job_name)
    print(f"Job: {batch_job.name}")
    print(f"State: {batch_job.state.name}")
    if hasattr(batch_job, "display_name") and batch_job.display_name:
        print(f"Display name: {batch_job.display_name}")
    return batch_job


def wait_for_completion(client, job_name: str, poll_interval: int = 30) -> object:
    """Poll until batch job completes."""
    completed_states = {
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
        "JOB_STATE_EXPIRED"
    }

    batch_job = client.batches.get(name=job_name)
    while batch_job.state.name not in completed_states:
        print(f"  State: {batch_job.state.name} - waiting {poll_interval}s...")
        time.sleep(poll_interval)
        batch_job = client.batches.get(name=job_name)

    print(f"Job finished: {batch_job.state.name}")
    return batch_job


def download_results(client, batch_job, output_dir: Path):
    """Download and save images from a completed batch job."""
    from PIL import Image as PILImage
    from io import BytesIO

    output_dir.mkdir(parents=True, exist_ok=True)

    if batch_job.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Error: Job state is {batch_job.state.name}", file=sys.stderr)
        if hasattr(batch_job, "error") and batch_job.error:
            print(f"Error details: {batch_job.error}", file=sys.stderr)
        sys.exit(1)

    result_file_name = batch_job.dest.file_name
    print(f"Downloading results from: {result_file_name}")

    file_content_bytes = client.files.download(file=result_file_name)
    file_content = file_content_bytes.decode("utf-8")

    saved = 0
    errors = 0
    for line in file_content.splitlines():
        if not line:
            continue
        parsed = json.loads(line)
        key = parsed.get("key", f"unknown-{saved}")

        if "error" in parsed and parsed["error"]:
            print(f"  {key}: ERROR - {parsed['error']}")
            errors += 1
            continue

        if "response" not in parsed or not parsed["response"]:
            print(f"  {key}: No response")
            errors += 1
            continue

        candidates = parsed["response"].get("candidates", [])
        if not candidates:
            print(f"  {key}: No candidates")
            errors += 1
            continue

        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            if part.get("text"):
                print(f"  {key} text: {part['text'][:100]}")
            elif part.get("inlineData"):
                image_data = base64.b64decode(part["inlineData"]["data"])
                image = PILImage.open(BytesIO(image_data))

                output_path = output_dir / f"{key}.png"
                if image.mode == "RGBA":
                    rgb = PILImage.new("RGB", image.size, (255, 255, 255))
                    rgb.paste(image, mask=image.split()[3])
                    rgb.save(str(output_path), "PNG")
                elif image.mode == "RGB":
                    image.save(str(output_path), "PNG")
                else:
                    image.convert("RGB").save(str(output_path), "PNG")

                print(f"  {key}: saved {output_path} ({image.size[0]}x{image.size[1]})")
                saved += 1

    print(f"\nDone: {saved} images saved, {errors} errors")
    if saved > 0:
        print(f"Output directory: {output_dir.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch image generation with Nano Banana 2 (50% cheaper)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From a text file (one prompt per line)
  uv run batch_generate.py -f prompts.txt -o ./batch_output/

  # Inline prompts
  uv run batch_generate.py -p "A sunset" -p "A cat" -p "A logo" -o ./batch_output/

  # With options
  uv run batch_generate.py -f prompts.txt -o ./output/ --aspect 16:9 --resolution 2K

  # Check job status
  uv run batch_generate.py --status batches/abc123

  # Download when done
  uv run batch_generate.py --download batches/abc123 -o ./output/

  # Submit and wait for results
  uv run batch_generate.py -f prompts.txt -o ./output/ --wait
        """
    )

    parser.add_argument("-p", "--prompt", action="append", dest="prompts", help="Prompt(s) to generate. Can repeat.")
    parser.add_argument("-f", "--file", help="Text file with one prompt per line")
    parser.add_argument("-o", "--output", default="./batch_output", help="Output directory (default: ./batch_output)")
    parser.add_argument("--aspect", "-a", choices=SUPPORTED_ASPECT_RATIOS, help="Aspect ratio for all images")
    parser.add_argument("--resolution", "-r", choices=["0.5K", "1K", "2K", "4K"], default="1K", help="Resolution (default: 1K)")
    parser.add_argument("--name", default="nano-banana-2-batch", help="Display name for the batch job")
    parser.add_argument("--status", metavar="JOB_NAME", help="Check status of an existing batch job")
    parser.add_argument("--download", metavar="JOB_NAME", help="Download results from a completed batch job")
    parser.add_argument("--wait", action="store_true", help="Wait for batch job to complete and download results")
    parser.add_argument("--poll-interval", type=int, default=30, help="Seconds between status checks (default: 30)")
    parser.add_argument("--api-key", "-k", help="Gemini API key (overrides GEMINI_API_KEY env var)")

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key. Set GEMINI_API_KEY or use --api-key.", file=sys.stderr)
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=api_key)

    output_dir = Path(args.output)

    # Mode: check status
    if args.status:
        check_status(client, args.status)
        return

    # Mode: download results
    if args.download:
        batch_job = client.batches.get(name=args.download)
        download_results(client, batch_job, output_dir)
        return

    # Mode: submit new batch
    prompts = []
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        prompts = [line.strip() for line in file_path.read_text().splitlines() if line.strip()]
    if args.prompts:
        prompts.extend(args.prompts)

    if not prompts:
        print("Error: Provide prompts via -p or -f", file=sys.stderr)
        sys.exit(1)

    print(f"Submitting batch of {len(prompts)} images")
    print(f"  Resolution: {args.resolution}")
    print(f"  Aspect: {args.aspect or 'auto'}")
    print(f"  Estimated cost: ~${len(prompts) * 0.034:.2f} (at 1K batch pricing)")
    print()

    job_name = submit_batch(client, prompts, args.aspect, args.resolution, args.name)

    if args.wait:
        print(f"\nWaiting for completion (polling every {args.poll_interval}s)...")
        batch_job = wait_for_completion(client, job_name, args.poll_interval)
        download_results(client, batch_job, output_dir)
    else:
        print(f"\nJob submitted. To check status:")
        print(f"  uv run batch_generate.py --status {job_name}")
        print(f"To download results when done:")
        print(f"  uv run batch_generate.py --download {job_name} -o {args.output}")


if __name__ == "__main__":
    main()
