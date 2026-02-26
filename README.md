# Nano Banana 2

> Pro-level AI image generation at Flash speed, powered by Google's Gemini 3.1 Flash Image.

An AI agent skill for generating, editing, and refining images. Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex CLI](https://github.com/openai/codex), [Cursor](https://cursor.sh), and any tool that supports [Skillshare](https://github.com/runkids/skillshare).

## What is this?

Nano Banana 2 is a skill (a structured prompt + scripts package) that gives AI coding agents the ability to generate and edit images using Google's Gemini 3.1 Flash Image API. It wraps the API in Python scripts with smart defaults, prompt templates, batch processing, and interactive chat mode.

**Model:** `gemini-3.1-flash-image-preview`
**API:** [Google Gemini API](https://ai.google.dev/gemini-api/docs/image-generation)

## Features

- **Text-to-image** - Generate images from text prompts
- **Image editing** - Pass existing images + prompt to edit, restyle, upscale, translate text
- **Multi-image composition** - Up to 10 reference images for object consistency, 4 for characters
- **Interactive chat** - Multi-turn refinement with context preservation
- **Batch generation** - 50% cheaper async processing for bulk jobs
- **14 aspect ratios** - Including ultra-wide (8:1) and ultra-tall (1:8)
- **4 resolutions** - 0.5K (512px), 1K, 2K, 4K
- **Controllable thinking** - `high` for quality, `minimal` for speed
- **Google Search grounding** - Real-time data in generated images
- **Smart defaults** - Auto-detect aspect ratio and settings from prompt
- **Prompt templates** - Photorealistic, product, logo, social, portrait, infographic

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package runner)
- A [Gemini API key](https://aistudio.google.com/apikey)

```bash
# Install uv if needed
brew install uv

# Set your API key
export GEMINI_API_KEY="your-api-key"
```

## Installation

### Via Skillshare (recommended)

```bash
skillshare install nerveband/nano-banana-2
skillshare sync
```

### Manual

Clone into your skills directory:

```bash
git clone https://github.com/nerveband/nano-banana-2.git ~/.claude/skills/nano-banana-2
```

## Quick Start

```bash
# Generate an image from a prompt
uv run scripts/generate_image.py -p "A serene mountain landscape at sunset" -f landscape.png

# Edit an existing image
uv run scripts/generate_image.py -p "Add dramatic sunset colors" -f edited.png -i photo.png

# Interactive chat mode
uv run scripts/chat_image.py

# Batch generate (50% off, up to 24h)
uv run scripts/batch_generate.py -f prompts.txt -o ./output/ --wait
```

## Scripts

### `generate_image.py` - Single Image Generation

```
uv run scripts/generate_image.py [OPTIONS]

Required:
  -p, --prompt TEXT        Image description
  -f, --filename FILE      Output filename (.png)

Input:
  -i, --input-image FILE   Input image(s) for editing (repeatable, max 10)

Output:
  -r, --resolution SIZE    0.5K | 1K (default) | 2K | 4K
  -a, --aspect RATIO       1:1 | 1:4 | 1:8 | 2:3 | 3:2 | 3:4 | 4:1 | 4:3 |
                           4:5 | 5:4 | 8:1 | 9:16 | 16:9 | 21:9

Advanced:
  --thinking LEVEL         high (default) | minimal
  --include-thoughts       Show model's reasoning in output
  -s, --system TEXT        System prompt for style constraints
  --search                 Enable Google Search grounding
  --smart                  Auto-detect aspect ratio and settings from prompt

Templates:
  --template NAME          photorealistic | product | logo | social |
                           portrait | infographic
  --template-var K=V       Template variable (repeatable)

Other:
  -k, --api-key KEY        Override GEMINI_API_KEY env var
  --no-validate            Skip prompt validation warnings
```

### `chat_image.py` - Interactive Chat Mode

```
uv run scripts/chat_image.py

Commands:
  /save <filename>     Save the last generated image
  /aspect <ratio>      Set aspect ratio
  /resolution <size>   Set resolution (0.5K/1K/2K/4K)
  /thinking <level>    Set thinking level (high/minimal)
  /search              Toggle Google Search grounding
  /clear               Clear conversation history
  /config              Show current settings
  /help                Show help
  exit, quit           Exit
```

### `batch_generate.py` - Batch Generation (50% Off)

```
uv run scripts/batch_generate.py [OPTIONS]

Input (one or both):
  -p, --prompt TEXT        Inline prompt (repeatable)
  -f, --file FILE          Text file with one prompt per line

Output:
  -o, --output DIR         Output directory (default: ./batch_output)

Options:
  -a, --aspect RATIO       Aspect ratio for all images
  -r, --resolution SIZE    0.5K | 1K (default) | 2K | 4K
  --name TEXT              Display name for the batch job
  --wait                   Block until job completes and download results
  --poll-interval SECS     Seconds between status checks (default: 30)

Job management:
  --status JOB_NAME        Check status of an existing job
  --download JOB_NAME      Download results from a completed job
```

## Usage Modes

### 1. Text-to-Image (prompt only)

```bash
uv run scripts/generate_image.py -p "A cozy coffee shop interior" -f cafe.png

uv run scripts/generate_image.py \
  -p "Watercolor painting of a Japanese garden, cherry blossoms, koi pond" \
  -f garden.png --aspect 16:9
```

### 2. Image Editing (prompt + one image)

```bash
# Add elements
uv run scripts/generate_image.py -p "Add a rainbow in the sky" -f edited.png -i photo.png

# Change style
uv run scripts/generate_image.py -p "Convert to pencil sketch" -f sketch.png -i photo.png

# Remove/replace background
uv run scripts/generate_image.py \
  -p "Remove background, replace with white studio backdrop" \
  -f clean.png -i product.png

# Upscale
uv run scripts/generate_image.py \
  -p "Enhance with sharper details" -f hd.png -i low_res.png --resolution 4K

# Translate text
uv run scripts/generate_image.py \
  -p "Translate all text to Spanish" -f spanish.png -i english_menu.png
```

Aspect ratio and resolution auto-detect from the input image unless overridden.

### 3. Multi-Image Composition (prompt + multiple images)

```bash
# Combine products into a scene
uv run scripts/generate_image.py \
  -p "Lifestyle scene with these products" \
  -f scene.png -i prod1.png -i prod2.png -i prod3.png

# Character consistency
uv run scripts/generate_image.py \
  -p "Show this character in a park" -f park.png -i character_ref.png

# Style transfer
uv run scripts/generate_image.py \
  -p "Apply the art style of image 1 to the subject in image 2" \
  -f styled.png -i style_ref.png -i subject.png
```

Limits: 10 reference images for objects, 4 for character consistency.

### 4. Interactive Chat

```bash
uv run scripts/chat_image.py
```

```
> Create a minimalist poster for a jazz festival
[Image generated]
> Make the typography bolder
[Refined image]
> Change colors to deep blue and gold
[Refined image]
> /save jazz_poster.png
```

Each turn builds on the previous result.

### 5. Batch Generation

```bash
# From a file of prompts (one per line)
uv run scripts/batch_generate.py -f prompts.txt -o ./output/ --wait

# Inline prompts
uv run scripts/batch_generate.py \
  -p "Sunset over mountains" \
  -p "Cat in a spacesuit" \
  -o ./output/ --wait

# Async: submit now, download later
uv run scripts/batch_generate.py -f prompts.txt -o ./output/
# ... later ...
uv run scripts/batch_generate.py --status batches/abc123
uv run scripts/batch_generate.py --download batches/abc123 -o ./output/
```

## Pricing

### Nano Banana 2 vs Nano Banana Pro

| Resolution | Nano Banana Pro | Nano Banana 2 | Savings |
|------------|----------------|---------------|---------|
| 0.5K | N/A | $0.045 | New |
| 1K | $0.134 | $0.067 | 50% |
| 2K | $0.134 | $0.101 | 25% |
| 4K | $0.240 | $0.151 | 37% |

### Batch Pricing (50% off standard)

| Resolution | Standard | Batch |
|------------|----------|-------|
| 0.5K | $0.045 | $0.022 |
| 1K | $0.067 | $0.034 |
| 2K | $0.101 | $0.050 |
| 4K | $0.151 | $0.076 |

## Prompt Templates

### photorealistic

```bash
uv run scripts/generate_image.py --template photorealistic \
  --template-var subject="A majestic lion" \
  --template-var action="roaring" \
  --template-var setting="African savanna at golden hour" \
  --template-var camera_angle="low angle shot" \
  --template-var lighting="warm golden hour backlighting" \
  --template-var lens="200mm telephoto" \
  --template-var mood="powerful and majestic" \
  -f lion.png
```

Variables: `subject`, `action`, `setting`, `camera_angle`, `lighting`, `lens`, `mood`

### product

Variables: `product`, `surface`, `lighting`, `angle`, `style`

### logo

Variables: `style`, `elements`, `colors`, `typography`, `background`

### social

Variables: `aspect`, `headline`, `visual`, `details`

### portrait

Variables: `subject`, `pose`, `lens`, `lighting`, `background`, `mood`

### infographic

Variables: `style`, `topic`, `title`, `data_points`, `color_scheme`, `layout`

## Configuration

### API Key

Set via environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Or pass per-command:

```bash
uv run scripts/generate_image.py -p "..." -f out.png --api-key "your-key"
```

Or in `~/.clawdbot/moltbot.json` (for Clawdbot/Moltbot users):

```json
{
  "skills": {
    "nano-banana-2": {
      "apiKey": "your-api-key"
    }
  }
}
```

## Prompting Tips

**Do:**
- Use natural, full-sentence descriptions
- Be specific about camera angles, lighting, lenses
- Use "MUST" and "NEVER" for strict constraints
- Limit text elements to 1-3 for reliability
- Include negative constraints ("no watermarks", "no text")
- Use `--smart` for auto-detected settings

**Don't:**
- Use keyword soup ("beautiful amazing stunning")
- Mix conflicting styles ("photorealistic cartoon")
- Request lots of small text
- Write 500+ word prompts

## File Structure

```
nano-banana-2/
  SKILL.md              Skill definition (loaded by AI agents)
  README.md             This file
  scripts/
    generate_image.py   Single image generation and editing
    chat_image.py       Interactive multi-turn refinement
    batch_generate.py   Batch generation at 50% off
```

## Notes

- All generated images include SynthID watermarking
- Model knowledge cutoff: January 2025 (use `--search` for current data)
- Scripts print `MEDIA: /path/to/image.png` for downstream tooling
- Use timestamps in filenames: `2026-02-26-14-30-00-landscape.png`

## License

MIT

## Links

- [Gemini API Docs - Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Nano Banana Pro skill](https://github.com/nerveband/nano-banana-pro) (predecessor)
- [Skillshare](https://github.com/runkids/skillshare) (skill distribution)
