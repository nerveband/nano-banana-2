---
name: nano-banana-2
description: Generate, edit, and refine images using Google's Nano Banana 2 (Gemini 3.1 Flash Image) - Pro-level quality at Flash speed with extended aspect ratios, Google Image Search grounding, controllable thinking, and 0.5K-4K resolution. Use when asked to generate, create, edit, or refine images with Nano Banana 2, or when fast high-quality image generation is needed.
homepage: https://ai.google.dev/
metadata: {"moltbot":{"emoji":"🍌","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Nano Banana 2

Pro-level image generation at Flash speed, powered by Gemini 3.1 Flash Image. Generate, edit, and refine images with extended aspect ratios, Google Image Search grounding, controllable thinking, and 0.5K-4K resolution.

## What's New vs Nano Banana Pro

| Feature | Nano Banana Pro | Nano Banana 2 |
|---------|----------------|---------------|
| Model | `gemini-3-pro-image-preview` | `gemini-3.1-flash-image-preview` |
| Speed | Pro (slower) | Flash (faster) |
| Resolutions | 1K, 2K, 4K | **0.5K**, 1K, 2K, 4K |
| Aspect ratios | 10 ratios | **14 ratios** (+1:4, 4:1, 1:8, 8:1) |
| Reference images | Up to 14 | Up to 10 objects, 4 characters |
| Image Search | No | **Yes** (exclusive) |
| Thinking control | Built-in (no control) | **Controllable** (high/minimal) |
| Batch API | No | **Yes** |
| Text rendering | Good | **Improved** (infographics, menus, diagrams) |

## Quick Start

### Generate an Image

```bash
# Basic generation
uv run {baseDir}/scripts/generate_image.py -p "A serene mountain landscape at sunset" -f landscape.png

# With aspect ratio and thinking
uv run {baseDir}/scripts/generate_image.py -p "Epic cityscape" -f city.png --aspect 16:9 --thinking high

# Edit existing image
uv run {baseDir}/scripts/generate_image.py -p "Add dramatic sunset colors" -f edited.png -i photo.png

# Multi-image composition (up to 10 images)
uv run {baseDir}/scripts/generate_image.py -p "Product lineup" -f lineup.png -i prod1.png -i prod2.png -i prod3.png

# Ultra-wide banner (new ratio)
uv run {baseDir}/scripts/generate_image.py -p "Website hero banner for tech company" -f hero.png --aspect 8:1

# Fast thumbnail (new 0.5K resolution)
uv run {baseDir}/scripts/generate_image.py -p "App icon" -f icon.png --resolution 0.5K --aspect 1:1

# With Image Search grounding (exclusive to Nano Banana 2)
uv run {baseDir}/scripts/generate_image.py -p "Current Tokyo skyline at night" -f tokyo.png --image-search --aspect 16:9
```

### Interactive Chat Mode

```bash
uv run {baseDir}/scripts/chat_image.py
```

Then chat naturally:
```
> Create a logo for "Acme Corp"
[Image generated]
> Make the text bolder and add a blue gradient
[Refined image]
> /save acme_logo.png
Saved: /path/to/acme_logo.png
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `generate_image.py` | Image generation with templates, aspect ratios, smart defaults, grounding |
| `chat_image.py` | Interactive multi-turn refinement |

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

| Resolution | Size | Cost | Best For |
|------------|------|------|----------|
| 0.5K | 512px | Cheapest | Thumbnails, icons, quick previews |
| 1K | 1024px | ~$0.04/image | Web, social media, iterations |
| 2K | 2048px | ~$0.05/image | Digital displays, presentations |
| 4K | 4096px | ~$0.08/image | Print materials, large displays |

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

### Google Image Search Grounding

Exclusive to Nano Banana 2 - ground generations in real image search results:

```bash
uv run {baseDir}/scripts/generate_image.py \
  -p "Photo of the Eiffel Tower with current lighting installation" \
  -f eiffel.png \
  --image-search \
  --aspect 3:4
```

### Google Web Search Grounding

Generate images with real-time data:

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

### Chat Commands

- `/save <filename>` - Save last image
- `/aspect <ratio>` - Change aspect ratio (14 options)
- `/resolution <size>` - Change resolution (0.5K/1K/2K/4K)
- `/thinking <level>` - Adjust thinking (high/minimal)
- `/search` - Toggle Web Search grounding
- `/imgsearch` - Toggle Image Search grounding
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
- Model knowledge cutoff: January 2025 (use `--search` or `--image-search` for current data)
