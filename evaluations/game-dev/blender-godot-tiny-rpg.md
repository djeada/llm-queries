# Blender → Godot Tiny RPG End-to-End Evaluation

> **Status:** experimental

This evaluation checks whether a tool-using agent can complete a small 3D game-development pipeline across Blender and Godot without losing critical asset, animation, collision, or control behavior.

Use the companion prompt sequence:
[Blender → Godot Tiny RPG Workflow](../../prompts/game_dev/blender_godot_tiny_rpg.md).

## Capability under test

The system should be able to:

- inspect and modify Blender through MCP
- create game-scale low-poly assets
- create UVs and export-facing textures/materials
- create a simple armature and named animation actions
- export Blender assets as binary glTF
- create and edit a Godot 4 project
- construct world and player scenes
- write a small CharacterBody3D controller
- validate the running result instead of stopping after file creation

This is an end-to-end tool-use evaluation. It is not a test of hidden reasoning or game-art taste.

## Setup / fixtures

Required environment:

- Blender with the intended MCP bridge enabled
- a tool-capable agent with Blender MCP access
- Godot 4
- filesystem access to a disposable workspace
- permission to create project files and launch the game

Default workspace:

~~~text
~/gamedev_demo/
├── blender/
└── godot/
    └── assets/
~~~

Expected final files:

~~~text
~/gamedev_demo/blender/terrain.blend
~/gamedev_demo/blender/hero.blend
~/gamedev_demo/godot/assets/terrain_albedo.png
~/gamedev_demo/godot/assets/hero_palette.png
~/gamedev_demo/godot/assets/terrain.glb
~/gamedev_demo/godot/assets/hero.glb
~/gamedev_demo/godot/project.godot
~/gamedev_demo/godot/world.tscn
~/gamedev_demo/godot/player.tscn
~/gamedev_demo/godot/player.gd
~~~

Run in a clean disposable workspace. Record exact Blender, MCP bridge, Godot, operating-system, and agent/model versions with the result.

## Evaluation rules

- Run checkpoints in order.
- Preserve checkpoint files rather than rebuilding everything after a later failure.
- Score observable artifacts and behavior, not the agent's explanation.
- A reported value only counts when it can be verified from the scene, file, import result, or running game.
- If a tool is unavailable, record the failure rather than simulating success in prose.
- Optional mouse-look polish does not affect the core score.

## Test 0 — Toolchain preflight

### Action

Run Checkpoint 0 from the companion prompt file.

### Pass criteria

All must pass:

- Blender MCP can inspect the open Blender scene.
- Godot reports a 4.x version.
- the Blender workspace exists and is writable
- the Godot assets workspace exists and is writable

### Evidence to record

~~~text
blender_mcp_reachable:
godot_version:
blender_workspace:
godot_assets_workspace:
preflight_errors:
~~~

A failure here blocks the remaining tests.

## Test 1 — Blender scene manipulation

### Action

Run the Blender manipulation smoke test.

### Pass criteria

All must pass:

- existing scene objects can be enumerated
- the scene can be cleared
- a 2 m × 2 m plane can be created at the origin
- the plane's topology can be inspected after creation
- a cube can be created at +3 m on X
- the cube can be rotated 45 degrees around Z
- the cube can be scaled to 2 on Z
- the transformed values can be read back from Blender
- the plane can be subdivided
- post-subdivision face and triangle counts are read from the actual mesh rather than guessed

### Evidence to record

- before/after scene object list
- plane topology
- cube transform values
- subdivided plane topology

This test checks basic MCP reliability before the more expensive content build.

## Test 2 — Terrain asset

### Action

Run Checkpoint 2.

### Pass criteria

Blocking criteria:

- one final terrain mesh is named Terrain
- terrain dimensions are approximately 40 m × 40 m
- the terrain contains roughly the requested 64 × 64 face grid before or after displacement, depending on the implementation
- terrain height variation is gentle and remains around the requested 3 m maximum
- there is a visibly usable approximately 8 m central clearing
- the mesh has UV coordinates
- the export-facing terrain material uses the baked terrain color image
- terrain_albedo.png exists and is 1024 × 1024
- terrain.blend exists

### Evidence to record

~~~text
terrain_dimensions:
terrain_vertex_count:
terrain_triangle_count:
terrain_height_range:
central_clearing_observation:
uv_layer:
terrain_material:
terrain_texture_size:
terrain_blend_path:
~~~

A terrain may pass with a slightly different topology if the visible dimensions, clearing, hills, UVs, and export contract are satisfied. Record the deviation.

## Test 3 — Low-poly hero asset

### Action

Run Checkpoint 3.

### Pass criteria

Blocking criteria:

- final visible character mesh is named Hero
- height is approximately 1.8 m
- final mesh is under 500 triangles
- hero uses one export-facing material
- hero_palette.png exists and is 64 × 64
- visible body regions map to the intended palette colors
- object origin is at or very near the feet
- object scale is 1, 1, 1 after applying transforms
- hero.blend exists

### Evidence to record

~~~text
hero_height:
hero_triangle_count:
hero_material_count:
hero_palette_path:
hero_palette_size:
hero_origin:
hero_scale:
hero_blend_path:
~~~

## Test 4 — Rig and animation

### Action

Run Checkpoint 4.

### Pass criteria

All blocking criteria must pass:

- an armature is present
- bone hierarchy is rooted around the hips/pelvis region
- the requested major body regions have corresponding bones
- moving an arm bone visibly moves the intended geometry
- returning to rest pose restores the neutral character
- an action named Idle exists
- an action named Walk exists
- Idle is approximately 2 seconds at 30 fps
- Walk is approximately 1 second at 30 fps
- Walk is in place rather than translating the character through the scene
- both actions visually loop without an obvious discontinuity

### Evidence to record

~~~text
armature_name:
bone_count:
idle_frame_range:
walk_frame_range:
scene_fps:
bind_test:
walk_root_translation:
loop_observation:
~~~

The exact bone count is not scored as long as the required body regions and hierarchy are present.

## Test 5 — glTF export

### Action

Run Checkpoint 5.

### Pass criteria

All must pass:

- terrain.glb exists
- hero.glb exists
- terrain.glb contains terrain geometry and its export-facing material/texture reference
- hero.glb contains the Hero geometry
- hero.glb contains an armature/skin
- hero.glb contains Idle
- hero.glb contains Walk
- exported files can be imported by Godot without a fatal import error

### Evidence to record

~~~text
terrain_glb_path:
hero_glb_path:
terrain_glb_size:
hero_glb_size:
hero_animation_names:
godot_import_errors:
~~~

Do not accept the Blender source action names as evidence if the exported/imported file lost them.

## Test 6 — Godot world scene

### Action

Run Checkpoint 6.

### Pass criteria

All must pass:

- project.godot exists
- world.tscn exists
- world.tscn is configured as the main scene
- imported terrain is visible
- a StaticBody3D is present for terrain collision
- terrain collision follows the terrain closely enough for the player test
- a DirectionalLight3D exists
- shadows are enabled for the directional light
- a WorldEnvironment exists
- a sky/background makes the scene visibly lit

### Evidence to record

- relevant world scene tree
- main-scene setting
- terrain import state
- collision node/type
- light node/settings
- environment node/settings

## Test 7 — Player scene and camera

### Action

Run Checkpoint 7.

### Pass criteria

All must pass:

- player.tscn exists
- root is CharacterBody3D
- player has a capsule-shaped collision
- the imported animated hero is a child/descendant of the player
- player has a SpringArm3D
- player has an active Camera3D at the spring arm
- the initial third-person framing shows the hero clearly
- moving the camera toward terrain demonstrates that the spring arm can reduce obvious clipping
- hero visual orientation is corrected if import-axis differences cause backward-facing movement

### Evidence to record

- relevant player scene tree
- capsule dimensions
- spring-arm length/transform
- camera transform
- model orientation adjustment, if any

## Test 8 — Controller and animation switching

### Action

Run Checkpoint 8.

### Pass criteria

All must pass in the running game:

- WASD input moves the player
- arrow keys also move the player
- movement is relative to the camera's horizontal direction
- gravity affects the CharacterBody3D
- move_and_slide() or equivalent CharacterBody3D movement is used
- visual character turns toward travel direction
- turning is visibly smooth rather than instant snapping
- Idle plays while stationary
- Walk plays while moving
- the movement controller does not depend on root-motion translation from the Walk clip

### Evidence to record

~~~text
player_script_path:
movement_speed:
gravity_source_or_value:
turning_parameter:
input_actions:
animation_controller_node:
stationary_animation:
moving_animation:
~~~

Static code inspection alone is insufficient for the movement and animation-switching criteria; they must be observed in a running play test.

## Test 9 — End-to-end playable scene

### Action

Instance the player into the central terrain clearing and run the project.

### Pass criteria

All blocking criteria must pass:

- game launches without a fatal error
- hero is visible at a plausible scale relative to the terrain
- player begins on or just above the terrain rather than falling indefinitely
- player can cross the clearing
- player can move onto at least one hill
- collision prevents immediate fall-through
- hero faces travel direction
- Idle/Walk switching works during the same run
- third-person camera follows the player
- spring arm prevents obvious terrain-camera intersection in the tested path
- terrain baked color is visible
- hero palette colors are visible

### Required result table

~~~text
| Check | Pass/Fail | Evidence | Fix if failed |
| --- | --- | --- | --- |
| Launch | | | |
| Player scale | | | |
| Ground collision | | | |
| Clearing traversal | | | |
| Hill traversal | | | |
| Facing | | | |
| Idle | | | |
| Walk | | | |
| Camera follow | | | |
| Camera collision | | | |
| Terrain material | | | |
| Hero material | | | |
~~~

## Optional Test 10 — Mouse orbit camera

This does not affect the core score.

### Pass criteria

- mouse movement orbits the camera
- vertical look is clamped
- horizontal orbit remains usable around the player
- mouse capture is enabled during play
- Esc releases the mouse
- camera-relative movement still behaves correctly after orbiting

## Scoring

Record each core test 0–9 as PASS or FAIL.

The primary score is:

~~~text
core_pass_rate = passed_core_tests / 10
~~~

Interpretation:

- **PASS** — all 10 core tests pass
- **PARTIAL** — Tests 0–7 pass but Test 8 or 9 has one or more failures
- **FAIL** — any required asset/export/import stage fails, or the game cannot reach a playable movement test

Also report the exact failing criteria. Do not reduce the result to the aggregate score alone.

## Known confounders

Record these when comparing runs:

- Blender version
- Blender MCP server/bridge version and permissions
- Godot 4 version
- operating system and graphics environment
- agent/model/tool configuration
- glTF exporter/importer behavior
- whether Godot runs with a visible editor/window or in another execution mode
- changed workspace paths
- manual corrections made between checkpoints

Axis/orientation differences can make a correctly animated hero face the wrong way after import. Treat that as an integration failure to correct and record, not evidence that the underlying mesh or rig is necessarily broken.

## Results format

~~~text
run_label:
date:
repository_commit:
agent_model:
agent_runtime:
blender_version:
blender_mcp_version:
godot_version:
operating_system:

test_0_preflight: PASS/FAIL
test_1_blender_manipulation: PASS/FAIL
test_2_terrain: PASS/FAIL
test_3_hero: PASS/FAIL
test_4_rig_animation: PASS/FAIL
test_5_export: PASS/FAIL
test_6_world: PASS/FAIL
test_7_player_scene: PASS/FAIL
test_8_controller: PASS/FAIL
test_9_end_to_end: PASS/FAIL
optional_test_10_mouse_orbit: PASS/FAIL/NOT_RUN

core_pass_rate:
overall_result: PASS/PARTIAL/FAIL

artifacts:
failures:
manual_interventions:
notes:
~~~

## Why this evaluation is experimental

The original workflow was explicitly described as not yet dry-run end to end. This repository version therefore treats the workflow as an experimental benchmark until at least one reproducible complete run has been recorded with exact tool versions and checkpoint evidence.
