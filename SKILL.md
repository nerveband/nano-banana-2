---
name: nano-banana-2
description: Generate, edit, and refine images using Google's Nano Banana 2 (Gemini 3.1 Flash Image) - Pro-level quality at Flash speed with extended aspect ratios, controllable thinking, Google Search grounding, and 0.5K-4K resolution. Use when asked to generate, create, edit, or refine images with Nano Banana 2, or when fast high-quality image generation is needed.
homepage: https://ai.google.dev/
metadata: {"moltbot":{"emoji":"🍌","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Nano Banana 2

Pro-level image generation at Flash speed, powered by Gemini 3.1 Flash Image. Generate, edit, and refine images with extended aspect ratios, controllable thinking, Google Search grounding, and 0.5K-4K resolution.

## What's New vs Nano Banana Pro

| Feature | Nano Banana Pro | Nano Banana 2 |
|---------|----------------|---------------|
| Model | `gemini-3-pro-image-preview` | `gemini-3.1-flash-image-preview` |
| Speed | Pro (slower) | Flash (faster) |
| Resolutions | 1K, 2K, 4K | **0.5K**, 1K, 2K, 4K |
| Aspect ratios | 10 ratios | **14 ratios** (+1:4, 4:1, 1:8, 8:1) |
| Reference images | Up to 14 | Up to 10 objects, 4 characters |
| Thinking control | Built-in (no control) | **Controllable** (high/minimal) |
| Batch API | No | **Yes** |
| Text rendering | Good | **Improved** (infographics, menus, diagrams) |

## Quick Start

```bash
# Text-to-image (prompt only)
uv run {baseDir}/scripts/generate_image.py -p "A serene mountain landscape at sunset" -f landscape.png

# Edit an existing image (prompt + image)
uv run {baseDir}/scripts/generate_image.py -p "Add dramatic sunset colors" -f edited.png -i photo.png

# Multi-image composition (prompt + multiple images)
uv run {baseDir}/scripts/generate_image.py -p "Product lineup" -f lineup.png -i prod1.png -i prod2.png

# Interactive chat for iterative refinement
uv run {baseDir}/scripts/chat_image.py

# Batch generation at 50% off
uv run {baseDir}/scripts/batch_generate.py -f prompts.txt -o ./output/ --wait
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `generate_image.py` | Single image generation with templates, aspect ratios, smart defaults, grounding |
| `chat_image.py` | Interactive multi-turn refinement |
| `batch_generate.py` | Batch generation at 50% off - submit many prompts, get results in up to 24h |

## Usage Modes

### Text-to-Image (prompt only)

Generate a new image from a text description:

```bash
# Simple prompt
uv run {baseDir}/scripts/generate_image.py -p "A cozy coffee shop interior" -f cafe.png

# Detailed prompt with style guidance
uv run {baseDir}/scripts/generate_image.py \
  -p "Watercolor painting of a Japanese garden, cherry blossoms, koi pond, soft morning light" \
  -f garden.png --aspect 16:9

# With system prompt for style consistency
uv run {baseDir}/scripts/generate_image.py \
  -p "A cat on a windowsill" -f cat.png \
  --system "Use only retro pixel art style, 16-bit aesthetic"
```

### Image Editing (prompt + one image)

Pass an existing image with `-i` and describe what to change:

```bash
# Add elements to a photo
uv run {baseDir}/scripts/generate_image.py \
  -p "Add a rainbow in the sky" \
  -f edited.png -i original_photo.png

# Change style of an existing image
uv run {baseDir}/scripts/generate_image.py \
  -p "Convert this to a pencil sketch style" \
  -f sketch.png -i photo.png

# Remove or replace elements
uv run {baseDir}/scripts/generate_image.py \
  -p "Remove the background and replace with a clean white studio backdrop" \
  -f clean.png -i product_photo.png

# Upscale / enhance
uv run {baseDir}/scripts/generate_image.py \
  -p "Enhance this image with sharper details and better lighting" \
  -f enhanced.png -i low_quality.png --resolution 4K

# Translate text in an image
uv run {baseDir}/scripts/generate_image.py \
  -p "Translate all text in this image to Spanish" \
  -f spanish_menu.png -i english_menu.png
```

The aspect ratio and resolution are auto-detected from the input image unless you override with `--aspect` or `--resolution`.

### Multi-Image Composition (prompt + multiple images)

Pass up to 10 images for object reference or up to 4 for character consistency:

```bash
# Combine elements from multiple images
uv run {baseDir}/scripts/generate_image.py \
  -p "Create a collage combining these product photos into a lifestyle scene" \
  -f lifestyle.png -i prod1.png -i prod2.png -i prod3.png

# Character consistency across scenes
uv run {baseDir}/scripts/generate_image.py \
  -p "Show this character riding a bicycle in a park" \
  -f scene2.png -i character_ref.png

# Product in different settings (use same product image as reference)
uv run {baseDir}/scripts/generate_image.py \
  -p "Show this coffee mug on a desk in a modern office" \
  -f mug_office.png -i mug_photo.png

# Style transfer from one image to another
uv run {baseDir}/scripts/generate_image.py \
  -p "Apply the art style of the first image to the subject in the second image" \
  -f styled.png -i style_ref.png -i subject.png
```

**Limits:** Up to 10 reference images for objects, up to 4 for character consistency.

### Interactive Refinement (chat mode)

For iterative back-and-forth editing where each turn builds on the last:

```bash
uv run {baseDir}/scripts/chat_image.py
```

```
> Create a minimalist poster for a jazz festival
[Image generated]
> Make the typography bolder and add a saxophone silhouette
[Refined image]
> Change the color scheme to deep blue and gold
[Refined image]
> /save jazz_poster.png
Saved!
```

The chat preserves context, so each prompt refines the previous result without re-describing everything.

## Core Features

### Aspect Ratios

14 supported ratios: `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`

New ratios `1:4`, `4:1`, `1:8`, `8:1` are great for banners, skyscrapers, and strip ads.

```bash
# Ultra-wide banner
uv run {baseDir}/scripts/generate_image.py -p "Sale banner" -f banner.png --aspect 8:1

# Tall skyscraper ad
uv run {baseDir}/scripts/generate_image.py -p "Vertical ad" -f skyscraper.png --aspect 1:8
```

### Resolutions

| Resolution | Size | Cost | Batch Cost | Best For |
|------------|------|------|------------|----------|
| 0.5K | 512px | ~$0.045/image | ~$0.022 | Thumbnails, icons, quick previews |
| 1K | 1024px | ~$0.067/image | ~$0.034 | Web, social media, iterations |
| 2K | 2048px | ~$0.101/image | ~$0.050 | Digital displays, presentations |
| 4K | 4096px | ~$0.151/image | ~$0.076 | Print materials, large displays |

Roughly **50% cheaper** than Nano Banana Pro at every resolution, with batch pricing halving it again.

### Thinking Control

Control reasoning depth vs speed:

```bash
# High quality - best for complex compositions
uv run {baseDir}/scripts/generate_image.py -p "Intricate steampunk city" -f city.png --thinking high

# Minimal - fastest generation
uv run {baseDir}/scripts/generate_image.py -p "Quick sketch" -f sketch.png --thinking minimal

# Show thinking process
uv run {baseDir}/scripts/generate_image.py -p "Complex scene" -f scene.png --thinking high --include-thoughts
```

### Google Search Grounding

Generate images informed by real-time search data:

```bash
uv run {baseDir}/scripts/generate_image.py \
  -p "Weather infographic for Tokyo today" \
  -f weather.png \
  --search \
  --aspect 16:9
```

### Smart Defaults

Auto-detect recommended settings based on prompt:

```bash
uv run {baseDir}/scripts/generate_image.py -p "Professional headshot" -f portrait.png --smart
# Auto-selects: aspect=3:4, thinking=high
```

Auto-detection works for: `logo`, `portrait`, `landscape`, `product`, `social media`, `infographic`, `banner`

### System Prompts

Enforce consistent constraints:

```bash
uv run {baseDir}/scripts/generate_image.py \
  -p "A cat sleeping" \
  -f cat.png \
  --system "ALL images MUST be in black and white vintage 1920s photography style"
```

### Prompt Templates

```bash
# Photorealistic
uv run {baseDir}/scripts/generate_image.py \
  --template photorealistic \
  --template-var subject="A majestic lion" \
  --template-var action="roaring" \
  --template-var setting="African savanna at golden hour" \
  --template-var camera_angle="low angle shot" \
  --template-var lighting="warm golden hour backlighting" \
  --template-var lens="200mm telephoto" \
  --template-var mood="powerful and majestic" \
  -f lion.png

# Infographic (new template)
uv run {baseDir}/scripts/generate_image.py \
  --template infographic \
  --template-var style="modern flat" \
  --template-var topic="climate change statistics" \
  --template-var title="Global Temperature Rise" \
  --template-var data_points="2.5C increase, 40% ice loss" \
  --template-var color_scheme="blue-to-red gradient" \
  --template-var layout="vertical flow" \
  -f climate.png --aspect 9:16
```

**Available Templates:** `photorealistic`, `product`, `logo`, `social`, `portrait`, `infographic`

### Batch Generation (50% Off)

Submit many prompts at once for half-price processing (up to 24h turnaround):

```bash
# From a text file (one prompt per line)
uv run {baseDir}/scripts/batch_generate.py -f prompts.txt -o ./batch_output/

# Inline prompts
uv run {baseDir}/scripts/batch_generate.py \
  -p "A sunset over mountains" \
  -p "A cat in a spacesuit" \
  -p "Minimalist coffee shop logo" \
  -o ./batch_output/

# With aspect ratio and resolution
uv run {baseDir}/scripts/batch_generate.py -f prompts.txt -o ./output/ --aspect 16:9 --resolution 2K

# Submit and wait for results (blocks until done)
uv run {baseDir}/scripts/batch_generate.py -f prompts.txt -o ./output/ --wait

# Check status of a running job
uv run {baseDir}/scripts/batch_generate.py --status batches/abc123

# Download results when job completes
uv run {baseDir}/scripts/batch_generate.py --download batches/abc123 -o ./output/
```

**Batch pricing** (50% off standard):

| Resolution | Standard | Batch |
|------------|----------|-------|
| 0.5K | $0.045 | **$0.022** |
| 1K | $0.067 | **$0.034** |
| 2K | $0.101 | **$0.050** |
| 4K | $0.151 | **$0.076** |

**How it works:** Prompts are written to a JSONL file, uploaded to the API, and processed asynchronously. Results arrive as images within 24 hours. Use `--wait` to block until done, or check with `--status` and download later with `--download`.

### Chat Commands

- `/save <filename>` - Save last image
- `/aspect <ratio>` - Change aspect ratio (14 options)
- `/resolution <size>` - Change resolution (0.5K/1K/2K/4K)
- `/thinking <level>` - Adjust thinking (high/minimal)
- `/search` - Toggle Google Search grounding
- `/clear` - Clear conversation
- `/config` - Show settings

## Configuration

### API Key

Same key as Nano Banana Pro:
```bash
export GEMINI_API_KEY="your-api-key"
```

Or in `~/.clawdbot/moltbot.json`:
```json
{
  "skills": {
    "nano-banana-2": {
      "apiKey": "your-api-key"
    }
  }
}
```

## Notes

- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`
- The script prints a `MEDIA:` line for Moltbot to auto-attach on supported chat providers
- Maximum 10 reference images for objects, 4 for character consistency
- All images include SynthID watermarking
- Batch API compatible for high-volume workflows
- Model knowledge cutoff: January 2025 (use `--search` for current data)
