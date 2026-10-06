# Local Image-to-3D Asset Experiments

> **Freshness:** version-sensitive · **Last verified:** 2026-10-06
> **Status:** experimental. Commands, model IDs, and export behavior were checked
> against upstream source on this date; the full GPU pipeline has not been run
> here. Hardware available for this review: RTX 5060, 8 GB VRAM.

Use this guide to test whether a reference-image prompt produces a usable Blender
or Godot asset. It complements the repository's
[Blender/Godot game prompt](../prompts/game_dev/blender_godot_tiny_rpg.md): save
intermediate files, compare changes, and inspect the exported asset rather than
judging only the generated picture. The image and 3D models below are separate
from the LLM that helps write or revise the prompt.

Start with **one existing image and TripoSR**. Image generation, Hunyuan painting,
and character rigging are optional experiments after that baseline works.

## Choose the experiment before downloading

| Path | Download/run | Result | Hardware boundary |
| --- | --- | --- | --- |
| First mesh | TripoSR + one PNG | Mesh with vertex colors | Upstream reports about 6 GB VRAM at defaults |
| Image prompt comparison | FLUX.1-schnell and Qwen-Image, separately | Two reference PNGs | Large image models; CPU offloading also requires host RAM |
| Alternative shape | Hunyuan3D **2.1** Shape | Untextured mesh | Upstream reports 10 GB VRAM |
| Texture experiment | Hunyuan3D **2.1** Paint | Mesh with PBR materials | Upstream reports 21 GB VRAM for texture, 29 GB for combined shape + texture |
| Character experiment | Make-It-Animatable **v1**, separately | FBX/BLEND with rig and skin weights | CUDA dependencies; no verified minimum VRAM in this guide |

The VRAM figures are upstream budgets, not measurements on this machine:
[TripoSR installation](https://github.com/VAST-AI-Research/TripoSR#installation),
[Hunyuan3D 2.1 models](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1#-models-zoo).
An 8 GB card is a reasonable starting point for the TripoSR experiment; the
Hunyuan3D 2.1 commands below require a larger GPU. Run each stage in a separate
process so weights from a previous stage do not stay in VRAM.

```text
prompt → FLUX or Qwen → reference.png
reference.png → TripoSR or Hunyuan Shape → shape mesh
shape mesh + reference.png → Hunyuan Paint → textured mesh
character mesh → Make-It-Animatable → rigged FBX/BLEND → animation check
```

Painting does not create a skeleton or skinning weights. A static prop can stop
at the mesh/texture stage. A character is accepted only after a pose and animation
check. Painting can remesh; perform it before rigging in these experiments.

## Working directory and prerequisites

Commands target **Linux with an NVIDIA CUDA GPU**. Install Git, Python 3.10 and
3.11 with `venv`, a C++ compiler, and the CUDA toolkit before installing the 3D
packages. Hunyuan uses CUDA 12.4/PyTorch 2.5.1; the selected MIA v1 dependencies
use CUDA 12.1/PyTorch 2.1.2. Keep their environments separate. Check that the
compiler and driver support the selected toolkit; a PyTorch wheel alone does
not provide `nvcc` for native extensions.

```bash
nvidia-smi
nvcc --version
c++ --version
python3.10 --version
python3.11 --version
mkdir -p "$HOME/image-to-3d-lab"/{inputs,outputs,models,logs}
cd "$HOME/image-to-3d-lab"
export ASSET_LAB="$PWD"
```

In a new shell, set `ASSET_LAB` to this directory again. All paths below use it.
Downloads need internet access and substantial free disk space. Use
`du -sh "$ASSET_LAB/models"` to track storage. Model files are not bundled with
llm-queries. Do not install these dependencies at the repository root.

Copy a PNG you own to `$ASSET_LAB/inputs/reference.png`. Prefer one complete,
centered object, a plain background, visible silhouette, and no cropped parts.
For characters, use a neutral A-pose with separated limbs. Avoid a multi-view
collage: these runs take one reference image, not a set of orthographic views.

## 1. Download and run the first mesh: TripoSR

Use this pinned source revision, whose flags and output paths were inspected:
[run.py](https://github.com/VAST-AI-Research/TripoSR/blob/107cefdc244c39106fa830359024f6a2f1c78871/run.py).

```bash
cd "$ASSET_LAB"
git clone https://github.com/VAST-AI-Research/TripoSR.git
git -C TripoSR checkout 107cefdc244c39106fa830359024f6a2f1c78871
python3.10 -m venv "$ASSET_LAB/venv-triposr"
source "$ASSET_LAB/venv-triposr/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch==2.5.1 torchvision==0.20.1 \
  --index-url https://download.pytorch.org/whl/cu124
cd "$ASSET_LAB/TripoSR"
python -m pip install -r requirements.txt numpy==1.26.4 rembg==2.0.65 \
  opencv-python-headless==4.10.0.84 'onnxruntime<2'
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download('stabilityai/TripoSR', local_dir='../models/TripoSR',
                  allow_patterns=['config.yaml', 'model.ckpt'])
PY
python -c 'import torch; print(torch.__version__, torch.cuda.is_available())'
python run.py --help
python run.py "$ASSET_LAB/inputs/reference.png" \
  --pretrained-model-name-or-path "$ASSET_LAB/models/TripoSR" \
  --model-save-format glb --output-dir "$ASSET_LAB/outputs/triposr"
test -s "$ASSET_LAB/outputs/triposr/0/mesh.glb"
python -m pip freeze > "$ASSET_LAB/logs/triposr-requirements.txt"
```

The CUDA check should print `True`. If it prints `False`, fix the driver/wheel
installation before timing GPU experiments. TripoSR can fall back to CPU, which
would make a GPU timing comparison misleading. The first background-removal run
also downloads rembg's segmentation weights to its own cache.

Outputs: `outputs/triposr/0/input.png` is the processed reference;
`outputs/triposr/0/mesh.glb` is the reconstructed mesh with vertex colors. Import
that GLB into Blender via **File → Import → glTF 2.0**. Rotate it through front,
side, and back views. Check for missing parts, holes, fused limbs, and invented
backside geometry before spending time on textures or rigging.

For a UV texture experiment, run again into a new directory:

```bash
python run.py "$ASSET_LAB/inputs/reference.png" \
  --pretrained-model-name-or-path "$ASSET_LAB/models/TripoSR" \
  --bake-texture --texture-resolution 1024 \
  --model-save-format obj --output-dir "$ASSET_LAB/outputs/triposr-baked"
```

This produces `0/mesh.obj` and `0/texture.png`. Import the OBJ and assign
`texture.png` to the material's Base Color using its UV map; this export does
not promise a ready-made material binding. Vertex colors and a baked UV texture
are different outputs; keep both runs.

## 2. Optional: generate the reference with FLUX or Qwen

Skip this section if you already have an image. Use one shared prompt initially:

```text
A single stylized wooden treasure chest, closed lid, chunky proportions,
three-quarter front view, entire object visible and centered, plain white
background, even diffuse lighting, no ground shadow, no text, no other objects.
```

Create a separate image environment. The selected Diffusers release contains
[QwenImagePipeline](https://github.com/huggingface/diffusers/blob/v0.35.1/src/diffusers/pipelines/qwenimage/pipeline_qwenimage.py).

```bash
cd "$ASSET_LAB"
python3.10 -m venv venv-images
source venv-images/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.5.1 torchvision==0.20.1 \
  --index-url https://download.pytorch.org/whl/cu124
python -m pip install diffusers==0.35.1 transformers==4.51.3 \
  accelerate==1.10.1 sentencepiece protobuf 'huggingface_hub[cli]==0.34.4'
```

Download **only the image model you plan to run**:

```bash
hf download black-forest-labs/FLUX.1-schnell \
  --local-dir "$ASSET_LAB/models/FLUX.1-schnell"
# Optional, separate download for the Qwen comparison:
hf download Qwen/Qwen-Image --local-dir "$ASSET_LAB/models/Qwen-Image"
```

If the FLUX download requires access approval, accept the model's access terms
on its Hugging Face page and run `hf auth login` in this environment. CPU
offloading reduces GPU residency but still needs host RAM for the model; it is
not a verified 8 GB recipe. Qwen-Image's 20B model is especially large. If weights
or inference do not fit, use the official
[Qwen demo](https://huggingface.co/spaces/Qwen/qwen-image), record that it was
hosted, and save the downloaded image under `inputs/`. Do not compare its runtime
with local inference.

Save the following as `$ASSET_LAB/generate_reference.py`. It uses the
[FLUX inference settings](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
and [Qwen inference settings](https://huggingface.co/Qwen/Qwen-Image).

```python
import argparse
import os
from pathlib import Path
import torch
from diffusers import FluxPipeline, QwenImagePipeline

parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['flux', 'qwen'])
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--prompt-file', type=Path, required=True)
args = parser.parse_args()
root = Path(os.environ['ASSET_LAB'])
prompt = args.prompt_file.read_text().strip()
name = 'FLUX.1-schnell' if args.model == 'flux' else 'Qwen-Image'
cls = FluxPipeline if args.model == 'flux' else QwenImagePipeline
pipe = cls.from_pretrained(root / 'models' / name, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
settings = dict(num_inference_steps=4, guidance_scale=0.0,
                max_sequence_length=256) if args.model == 'flux' else dict(
                    num_inference_steps=50, true_cfg_scale=4.0,
                    negative_prompt=' ')
image = pipe(prompt=prompt, width=1024, height=1024,
             generator=torch.Generator('cpu').manual_seed(args.seed),
             **settings).images[0]
output = root / 'inputs' / f'{args.model}-{args.seed}.png'
image.save(output)
print(output)
```

Save the shared prompt to `$ASSET_LAB/inputs/chest.txt`, then run:

```bash
python "$ASSET_LAB/generate_reference.py" flux \
  --prompt-file "$ASSET_LAB/inputs/chest.txt" --seed 42
# Run only after the Qwen download and memory check:
python "$ASSET_LAB/generate_reference.py" qwen \
  --prompt-file "$ASSET_LAB/inputs/chest.txt" --seed 42
python -m pip freeze > "$ASSET_LAB/logs/image-requirements.txt"
```

Use the resulting `inputs/flux-42.png` or `inputs/qwen-42.png` as the image
argument in section 1. Same seed numbers do not mean equivalent noise across
models. Repeat with seeds 43 and 44; retain all images rather than choosing only
the best one.

## 3. Optional: Hunyuan3D 2.1 shape and paint

Use **2.1** throughout this section; its modules and PBR models differ from 2.0.
Follow the upstream [installation](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1#install-requirements)
in its own Python 3.10 environment:

```bash
cd "$ASSET_LAB"
git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1.git
git -C Hunyuan3D-2.1 checkout 82920d643c0dc2f7bfd7255f45f62d386edfe60c
python3.10 -m venv venv-hunyuan
source venv-hunyuan/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 \
  --index-url https://download.pytorch.org/whl/cu124
cd "$ASSET_LAB/Hunyuan3D-2.1"
python -m pip install -r requirements.txt
```

Shape-only users can skip the paint builds/download below. For painting:

```bash
python -m pip install -e hy3dpaint/custom_rasterizer
(cd hy3dpaint/DifferentiableRenderer && bash compile_mesh_painter.sh)
mkdir -p hy3dpaint/ckpt
curl -fL https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
  -o hy3dpaint/ckpt/RealESRGAN_x4plus.pth
```

The shape model downloads `tencent/Hunyuan3D-2.1/hunyuan3d-dit-v2-1` automatically
under `~/.cache/hy3dgen`; Paint downloads `hunyuan3d-paintpbr-v2-1` to the Hugging
Face cache and may also load `facebook/dinov2-giant`. These are additional
weights beyond Real-ESRGAN. The download behavior is in the
[shape loader](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/82920d643c0dc2f7bfd7255f45f62d386edfe60c/hy3dshape/hy3dshape/utils/utils.py)
and [paint loader](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/82920d643c0dc2f7bfd7255f45f62d386edfe60c/hy3dpaint/utils/multiview_utils.py).

Save this as `$ASSET_LAB/Hunyuan3D-2.1/run_asset.py` and run it from that checkout.
The shape and paint modes run separately. The paint mode exports OBJ plus GLB,
matching the [paint exporter](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/82920d643c0dc2f7bfd7255f45f62d386edfe60c/hy3dpaint/textureGenPipeline.py).

```python
import argparse
import sys
from pathlib import Path
sys.path.insert(0, './hy3dshape')
sys.path.insert(0, './hy3dpaint')

parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=['shape', 'paint'])
parser.add_argument('--image', required=True)
parser.add_argument('--output-dir', type=Path, required=True)
parser.add_argument('--mesh')
parser.add_argument('--seed', type=int, default=42)
args = parser.parse_args()
args.output_dir.mkdir(parents=True, exist_ok=True)
if args.stage == 'shape':
    import torch
    from PIL import Image
    from hy3dshape.rembg import BackgroundRemover
    from hy3dshape.pipelines import Hunyuan3DDiTFlowMatchingPipeline
    image = Image.open(args.image)
    if image.mode != 'RGBA' or image.getextrema()[3] == (255, 255):
        image = BackgroundRemover()(image.convert('RGB'))
    image.save(args.output_dir / 'input.png')
    pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        'tencent/Hunyuan3D-2.1')
    mesh = pipe(image=image, num_inference_steps=50,
                generator=torch.Generator('cuda').manual_seed(args.seed))[0]
    mesh.export(str(args.output_dir / 'shape.glb'))
else:
    if not args.mesh:
        parser.error('paint requires --mesh')
    from torchvision_fix import apply_fix
    if not apply_fix():
        raise RuntimeError('torchvision compatibility fix failed')
    from textureGenPipeline import Hunyuan3DPaintPipeline, Hunyuan3DPaintConfig
    config = Hunyuan3DPaintConfig(max_num_view=6, resolution=512)
    config.realesrgan_ckpt_path = 'hy3dpaint/ckpt/RealESRGAN_x4plus.pth'
    pipe = Hunyuan3DPaintPipeline(config)
    pipe(mesh_path=args.mesh, image_path=args.image,
         output_mesh_path=str(args.output_dir / 'textured.obj'))
```

```bash
cd "$ASSET_LAB/Hunyuan3D-2.1"
python run_asset.py shape --image "$ASSET_LAB/inputs/reference.png" \
  --output-dir "$ASSET_LAB/outputs/hunyuan-shape" --seed 42
# On a GPU with enough memory for Paint:
python run_asset.py paint --image "$ASSET_LAB/outputs/hunyuan-shape/input.png" \
  --mesh "$ASSET_LAB/outputs/hunyuan-shape/shape.glb" \
  --output-dir "$ASSET_LAB/outputs/hunyuan-paint"
python -m pip freeze > "$ASSET_LAB/logs/hunyuan-requirements.txt"
```

Inspect `hunyuan-shape/shape.glb` and `hunyuan-paint/textured.glb` in Blender.
Keep the OBJ and adjacent material/texture files together. Paint defaults to
remeshing the input and uses an internal fixed seed of 0 in this revision; the
`--seed` option above controls shape only. Record changes in triangle count and
silhouette as well as material quality. A prettier render is not proof that the
geometry survived.

## 4. Optional: rig a character with Make-It-Animatable v1

Use a humanoid character reference instead of the chest. MIA's v2 branch has a
different backbone and entry point; these commands select the inspected **v1**
revision and [app.py](https://github.com/jasongzy/Make-It-Animatable/blob/8fb51382ff6da556cdb95cc03a48200603f3a493/app.py).

```bash
cd "$ASSET_LAB"
git clone --recursive --single-branch https://github.com/jasongzy/Make-It-Animatable.git
git -C Make-It-Animatable checkout 8fb51382ff6da556cdb95cc03a48200603f3a493
git -C Make-It-Animatable submodule update --init --recursive
python3.11 -m venv venv-mia
source venv-mia/bin/activate
python -m pip install --upgrade pip
cd "$ASSET_LAB/Make-It-Animatable"
python -m pip install -r requirements.txt
python -m pip install 'huggingface_hub[cli]==0.34.4'
hf download jasongzy/Mixamo --repo-type dataset \
  --include 'bones*.fbx' 'animation/**' --local-dir data/Mixamo
hf download jasongzy/Make-It-Animatable \
  --include 'output/best/new/**' 'data/**' --local-dir .
curl -fL https://github.com/facebookincubator/FBX2glTF/releases/download/v0.9.7/FBX2glTF-linux-x64 \
  -o util/FBX2glTF
chmod +x util/FBX2glTF
python -m pip freeze > "$ASSET_LAB/logs/mia-requirements.txt"
python app.py
```

Open `http://localhost:7860`, upload a character GLB/OBJ, and click **Run**.
Download the FBX/BLEND from **Animatable Model (FBX/BLEND)** into
`outputs/mia/`. Select a supplied animation and click **Animate** to check
motion. In Blender, verify an armature exists and moving an arm or leg bone
deforms the intended limb. Watch a walk cycle for foot sliding, collapsed
shoulders, fused limbs, and material loss. The GLB preview can differ from the
FBX materials; inspect the downloaded FBX/BLEND before declaring success.

No training dataset or `train.sh` run is needed. Failed rigging is an experiment
result, not evidence that a textured mesh was animation-ready.

## Experiments to run and what to record

Run these in order; skip stages your hardware cannot execute. Never change the
image generator, mesh generator, and rigging settings in one comparison.

| Experiment | Hold fixed | Change | Checkable result |
| --- | --- | --- | --- |
| Baseline | One `reference.png` | Nothing | Importable TripoSR mesh; front/side/back screenshots |
| Prompt A/B | FLUX, seeds 42/43/44, TripoSR defaults | Add “entire object visible, plain background, no shadow” to a weaker prompt | Compare cropping, fused parts, silhouette; retain all six images/meshes |
| Image model | Prompt, dimensions, downstream TripoSR settings | FLUX vs Qwen, three seeds each | Which references produce usable meshes more often? Record generator settings separately |
| Shape model | Exactly the same reference PNG | TripoSR vs Hunyuan 2.1 Shape | Geometry with a neutral material: holes, missing parts, backside plausibility, triangle count |
| Texture stage | Saved Hunyuan shape and processed PNG | Before/after Paint | Material seams/color consistency plus geometry/remeshing changes |
| Rigging | One final character mesh, same animation | Before/after MIA | Armature, limb deformation, walk-cycle screenshots/video, preserved materials |

For the prompt A/B test, save the weaker version to `inputs/chest-a.txt` and the
revised version to `inputs/chest-b.txt`. Run `generate_reference.py` with each
file and each seed, moving the emitted PNG to an A/B-specific filename after
every run: the script otherwise reuses `flux-42.png`. Use a separate
`--output-dir` for every TripoSR run. Keep raw outputs, including failures.

Create `logs/results.csv` with one row per stage invocation:

```csv
run_id,stage,model_id,model_revision,source_commit,input_sha256,prompt_file,seed,settings,gpu,peak_vram_mb,seconds,output_path,import_ok,geometry_issues,material_issues,rig_issues
```

Record `sha256sum inputs/*.png`, source commit IDs, `pip freeze`, and the model
snapshot revision shown in the download metadata/cache. Code revisions above
are pinned; model downloads follow the available revision unless you explicitly
pin it. Freeze the resolved model revisions for a repeatable comparison. Do not
mix cached revisions within a run set.

Measure download/cold-load time separately from inference. During a run, capture
GPU memory with `nvidia-smi --query-gpu=memory.used --format=csv,noheader -l 1`
in another terminal; this samples whole-device usage, not exact process peaks.
Use an otherwise idle GPU. Record wall time and failures/OOMs; leave unmeasured
fields empty rather than inventing values.

Acceptance gates: a mesh imports and has its major parts; textures survive
export and do not conceal broken geometry; a rig has a skeleton and deforms
correctly in motion. For Godot, export the inspected Blender asset as GLB, import
it into a test scene, and check scale, materials, and animation playback.
Scores here are manual observations, not an automated benchmark or published
quality ranking.

## Troubleshooting

| Symptom | Next action |
| --- | --- |
| CUDA extension build fails | Compare `nvcc`, PyTorch CUDA version, and compiler; rebuild in the correct stage environment |
| TripoSR runs out of memory | Retry with `--chunk-size 4096`; record the changed setting |
| Hunyuan Paint runs out of memory | Use the documented larger GPU budget; do not assume an offloading flag makes it fit 8 GB |
| Hunyuan fails importing `torchvision.transforms.functional_tensor` | Check the pinned checkout's `torchvision_fix.py` and upstream compatibility instructions before importing Paint |
| Mesh includes floor/shadow or limbs are fused | Revise the reference prompt/background, then rerun shape; painting will not repair it |
| OBJ looks white | Assign the exported texture/material files and verify UVs; compare the GLB export |
| Rig loses materials or deforms badly | Inspect FBX/BLEND and the armature; retain the unrigged mesh and record the failure |

For LLM help diagnosing a failure, use
[prompt debugging](../skills/prompt_debugging.md) with the exact prompt, model
revision, reference image, logs, and failed output. Ask for one specific change
and rerun the same inputs; avoid claims about a “better pipeline” without the
comparison artifacts above.
