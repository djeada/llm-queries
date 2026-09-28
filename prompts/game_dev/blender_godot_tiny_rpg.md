# Blender → Godot Tiny RPG Workflow

> **Status:** experimental

A staged prompt sequence for building a tiny third-person 3D RPG prototype with Blender through MCP and Godot 4.

The workflow separates asset creation, rigging, export, engine setup, player control, and final validation so failures can be isolated instead of hidden inside one giant prompt.

## Best for

- testing an AI-assisted Blender → Godot game-development workflow
- building a small low-poly third-person prototype
- exercising Blender MCP across modeling, UVs, materials, rigging, and animation
- checking whether exported glTF assets survive import into Godot
- testing agent handoffs between DCC tools, files, and a game engine

## Required input

- a working Blender MCP connection
- Blender with permission to save project files and export assets
- Godot 4 available on the machine
- a writable workspace for Blender source files and the Godot project
- a tool-capable agent that can inspect Blender and edit project files

Suggested workspace:

~~~text
~/gamedev_demo/
├── blender/
└── godot/
    └── assets/
~~~

If a different workspace is used, replace all paths consistently.

## Expected output

The completed workflow should produce:

- a Blender terrain scene
- a Blender low-poly hero scene
- baked terrain and hero textures
- a rigged hero with Idle and Walk actions
- terrain.glb and hero.glb
- a Godot 4 project with world.tscn and player.tscn
- a third-person CharacterBody3D controller
- camera-relative movement, gravity, turning, and animation switching
- a playable scene where the hero can walk over the terrain

Do not claim success from tool-call completion alone. Inspect the resulting objects, files, imported scenes, and running game at each checkpoint.

## Checkpoint 0 — Toolchain and workspace

~~~text
Verify the game-development toolchain before creating assets.

1. Confirm the Blender MCP bridge is reachable and that you can inspect the current Blender scene.
2. Confirm a Godot 4 executable is available and report its exact version.
3. Create these workspace directories if they do not exist:
   - ~/gamedev_demo/blender
   - ~/gamedev_demo/godot/assets
4. Report the Blender connection state, Godot version, and resolved workspace paths.

Do not begin asset creation if Blender cannot be inspected or the workspace is not writable.
~~~

## Checkpoint 1 — Blender manipulation smoke test

Use this before the full build when you want to verify basic MCP scene control.

~~~text
Inspect the current Blender scene and report every object's name and type.

Then:
1. Delete the existing scene objects.
2. Create a 2 m × 2 m plane at the world origin.
3. Report its vertex, edge, and face counts plus the direction of its face normal.
4. Add a cube 3 m along +X from the plane.
5. Rotate the cube 45 degrees around Z.
6. Scale the cube to 2 on Z.
7. Report the cube's location, rotation, and scale.
8. Subdivide the plane three times and report the resulting face and triangle counts from the actual scene.

Do not guess topology counts; inspect them after the operations.
~~~

## Checkpoint 2 — Terrain asset

~~~text
Delete the smoke-test objects and build the game terrain.

Requirements:
- one terrain mesh named Terrain
- approximately 40 m × 40 m
- a 64 × 64 face grid before displacement
- gentle noise-driven hills no more than about 3 m above the base
- an approximately 8 m-wide flat clearing around the center for the player
- applied geometry modifiers before export
- UVs projected from above

Create a terrain material with:
- grass-green flatter areas
- brown dirt/rock on steeper areas
- subtle variation so it is not a single flat color

Bake the terrain's final base color to:
~/gamedev_demo/godot/assets/terrain_albedo.png

Use a 1024 × 1024 image, then make the export-facing material use that baked image rather than depending on Blender-only procedural nodes.

Save the Blender source file as:
~/gamedev_demo/blender/terrain.blend

At the end, report:
- object name
- dimensions
- vertex count
- triangle count
- UV layer name
- baked image path
- saved .blend path
~~~

## Checkpoint 3 — Low-poly hero

~~~text
Create a new Blender scene and build a simple low-poly hero.

Requirements:
- about 1.8 m tall
- standing at the world origin
- facing a consistent forward direction
- box-like torso and head
- upper and lower arm segments on both sides
- upper and lower leg segments on both sides
- fewer than 500 final triangles
- clear temporary part names while constructing the character

Create a 64 × 64 palette texture containing flat swatches for:
- skin
- hair
- shirt
- belt
- pants
- boots

Save it as:
~/gamedev_demo/godot/assets/hero_palette.png

Map the body parts to the palette with UVs and use one export-facing material.

Join the visible character geometry into one mesh named Hero.

Before saving:
- place Hero's origin at its feet
- apply transforms so the final object scale is 1, 1, 1
- verify the final height and triangle count

Save as:
~/gamedev_demo/blender/hero.blend

Report the final height, triangle count, material count, texture path, origin location, scale, and saved file path.
~~~

## Checkpoint 4 — Rigging and animation

~~~text
Rig the Hero for a simple game-ready animation test.

Create an armature with a clear parent hierarchy rooted at the hips. Include bones for:
- hips
- spine
- head
- left/right upper arms
- left/right lower arms
- left/right upper legs
- left/right lower legs

About 12 bones is sufficient; prioritize a coherent hierarchy over an exact count.

Bind the mesh to the armature:
- use rigid 100% weights where a box-like limb should follow one bone
- allow blended/automatic weighting where the torso needs smoother deformation
- verify the bind by posing at least one arm and returning to rest pose

Create two named actions:

Idle
- 2 seconds
- 30 fps
- seamless loop
- subtle chest rise/fall and small arm motion

Walk
- 1 second
- in-place loop
- opposing arm/leg swing
- slight vertical hip motion
- no root translation that moves the character across the Blender scene

At the end, report:
- armature name
- bone count
- action names
- frame ranges
- fps
- whether both actions are intended to loop
~~~

## Checkpoint 5 — Export contract

~~~text
Export the terrain and hero as separate binary glTF files:

~/gamedev_demo/godot/assets/terrain.glb
~/gamedev_demo/godot/assets/hero.glb

Requirements:
- export applied geometry
- include the export-facing materials/textures
- include the hero armature
- include both Idle and Walk animations in hero.glb
- keep the Walk animation in place

After export, inspect the files or re-import them and report what each contains.

Do not mark this checkpoint complete unless both files exist at the expected paths.
~~~

## Checkpoint 6 — Godot world

~~~text
Create a Godot 4 project named "Tiny RPG" in:
~/gamedev_demo/godot

Let Godot import the assets folder.

Create world.tscn with:
- the terrain visual imported from terrain.glb
- a StaticBody3D collision body for the terrain
- collision geometry that follows the terrain closely enough for the player to walk on the hills
- a DirectionalLight3D with shadows
- a WorldEnvironment with a simple sky

Set world.tscn as the project's main scene.

At the end, report the relevant scene-tree nodes and verify that terrain.glb and hero.glb appear in the project and import without fatal errors.
~~~

## Checkpoint 7 — Player scene and camera

~~~text
Create player.tscn.

Root:
- CharacterBody3D

Children/components:
- a CapsuleShape3D collision shape sized to the hero
- the visual/animated Hero imported from hero.glb
- a SpringArm3D positioned for a third-person view
- a Camera3D at the end of the spring arm

Use an initial camera setup around 4 m behind and 2 m above the character, then adjust only if needed to frame the hero and terrain clearly.

Verify that:
- the capsule surrounds the character appropriately
- the camera is active
- the spring arm can shorten when geometry blocks the camera
- the hero's visual forward direction is compatible with movement; if it is not, correct the model orientation in the player scene
~~~

## Checkpoint 8 — Player controller

~~~text
Create player.gd for the CharacterBody3D.

Requirements:
- WASD and arrow-key movement
- movement direction relative to the camera's horizontal orientation
- gravity
- move_and_slide() for character movement/collision
- smooth visual turning toward movement direction
- play Walk while the player is moving
- play Idle while standing
- keep both animations looping
- concise comments suitable for a beginner

Keep movement code separate from the imported hero asset so the Blender file does not contain game logic.

After writing the script:
1. verify the required input actions exist or add them
2. attach the script to the player
3. report the movement speed and any rotation/gravity parameters
4. identify the animation player/controller node used to switch Idle and Walk
~~~

## Checkpoint 9 — End-to-end play test

~~~text
Instance player.tscn into world.tscn and place the player in the central clearing.

Run the project and validate the whole pipeline.

Check:
- the project starts without a fatal error
- the hero is visible at an appropriate scale
- the hero does not immediately fall through the terrain
- directional input moves the CharacterBody3D
- the character can move across the clearing and onto a hill
- the visible model turns toward travel direction
- Idle plays while stationary
- Walk plays while moving
- the camera follows behind the player
- the spring arm prevents obvious camera clipping through terrain
- baked terrain color and hero palette colors are visible

If any item fails, diagnose the first failing layer before changing unrelated parts of the project.

Return a compact validation table with:
check | pass/fail | evidence | fix if failed
~~~

## Optional polish — Mouse orbit camera

~~~text
Add optional third-person mouse look.

Requirements:
- mouse movement orbits the camera around the player
- vertical look is clamped to a usable range
- horizontal rotation can orbit freely around the character
- capture the mouse while playing
- Esc releases the mouse

Keep camera rotation separate from character movement direction calculations so camera-relative movement still works.
~~~

## Failure triage

When the final game fails, debug in this order:

1. **Tool / filesystem** — can Blender, Godot, and the workspace be reached?
2. **Blender asset** — are dimensions, transforms, UVs, rig, and actions valid?
3. **Export** — do the expected .glb files exist and contain the intended data?
4. **Godot import** — do assets import without fatal errors?
5. **Scene structure** — are visual nodes, collision, player, and camera present?
6. **Controller** — do input, gravity, movement, turning, and animation switching run?
7. **Presentation** — materials, camera framing, and optional polish.

Do not rebuild earlier stages if the evidence points to a later-stage failure.

## Review checklist

- Blender source files remain separate from exported game assets.
- Terrain and hero use game-engine-compatible export materials.
- Final hero geometry stays under the low-poly budget.
- Hero transforms are applied before export.
- Rig hierarchy and both named actions survive export/import.
- Godot separates visual meshes from collision.
- Movement is implemented on a CharacterBody3D rather than baked into the Walk animation.
- The final claim of success is based on a running play test, not file creation alone.
