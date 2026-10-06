# Image-to-3D Asset Pipeline

> **Last verified:** 2026-10-06

A version-sensitive workflow note for turning an AI-generated reference image into a textured, animation-ready 3D asset. It documents two pipelines and, most importantly, separates **shape generation**, **texturing**, and **rigging** instead of treating them as interchangeable steps.

## Pipeline A: FLUX → TripoSR → Make-It-Animatable

```text
text prompt
  → FLUX
  → reference image
  → TripoSR
  → 3D mesh
  → Make-It-Animatable
  → rigged / skinned character
  → animation
```

| Stage | Tool | Role |
| --- | --- | --- |
| 2D concept | FLUX | Generate or edit the source/reference image |
| Image → 3D | TripoSR | Reconstruct a 3D model from a single image |
| Rigging | Make-It-Animatable | Predict joints, skinning weights, and pose-related data so the character can be animated |

This pipeline is useful when the main goal is to get from a generated image to an **animation-ready character** quickly. The final Make-It-Animatable step is what turns the mesh into something that can be posed and animated.

## Pipeline B: Qwen Image → Hunyuan3D → Hunyuan3D-Paint

```text
text prompt
  → Qwen Image
  → reference image
  → Hunyuan3D-Shape
  → 3D mesh
  → Hunyuan3D-Paint
  → textured 3D asset
```

| Stage | Tool | Role |
| --- | --- | --- |
| 2D concept | Qwen Image | Generate or edit the source/reference image |
| Image → shape | Hunyuan3D-Shape | Generate the 3D geometry/mesh from the image |
| Texture/material | Hunyuan3D-Paint | Generate textures/material appearance for an existing mesh |

The important difference is that **Hunyuan3D-Paint is not a rigging step**. It improves the surface appearance of the mesh; it does not replace Make-It-Animatable.

For a static asset, this pipeline can stop after painting. For an animated character, add a separate rigging step:

```text
Qwen Image
  → Hunyuan3D-Shape
  → Hunyuan3D-Paint
  → Make-It-Animatable (or another rigging tool)
  → animation
```

Painting and rigging are separate concerns, so their exact order can be adjusted to fit the downstream DCC/game-engine workflow. The key requirement is that an animation-ready character still needs a skeleton/rig and skinning weights.

## What changed between the pipelines

The switch is **not** a one-for-one replacement of every stage.

| Earlier pipeline | Later pipeline | What changed |
| --- | --- | --- |
| FLUX | Qwen Image | Different image-generation/editing front end |
| TripoSR | Hunyuan3D-Shape | Different image-to-3D/shape generation step |
| Make-It-Animatable | Hunyuan3D-Paint | Not equivalent: rigging was replaced in the written pipeline by texturing |

So a statement such as:

> “I started with FLUX + TripoSR + Make It Animatable, then switched to Qwen Image → Hunyuan3D → Hunyuan Paint.”

should be interpreted as: the creator changed the image/3D-generation stack and added a dedicated texture stage. Unless another step is omitted from the description, the newer pipeline does **not yet describe rigging**.

## Practical decision rule

Use the stages you actually need:

- **Static prop:** image → shape → texture.
- **Renderable character:** image → shape → texture.
- **Animated character:** image → shape → texture + rigging → animation.
- **Existing mesh that already looks right:** skip shape generation and work on texturing/rigging directly where the tools allow it.

Keep intermediate artifacts when possible: the source image, untextured mesh, textured mesh, rigged mesh, and final exported asset. That makes it easier to swap one model without rebuilding the entire pipeline.

## References

- FLUX official inference repository: https://github.com/black-forest-labs/flux
- TripoSR: https://github.com/VAST-AI-Research/TripoSR
- Make-It-Animatable: https://github.com/jasongzy/Make-It-Animatable
- Qwen Image: https://github.com/QwenLM/Qwen-Image
- Hunyuan3D 2.1 / Hunyuan3D-Paint: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
