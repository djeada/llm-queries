# Blender Fluid Physics Tests

Three small Blender scene prompts for testing realistic liquid simulation. Each project is intentionally compact enough to iterate on while stressing a different aspect of fluid behavior.

## Best for

- Testing liquid simulation realism in Blender
- Comparing model-generated Blender scene setups
- Evaluating viscosity, splashing, buoyancy, overflow, and surface tension
- Small projects that can be rendered and reviewed quickly

## Expected Output

For each prompt, produce a Blender scene or build plan that prioritizes physically believable fluid motion over exaggerated effects. Keep the scene scope small, use realistic scale and materials, and make the fluid behavior easy to inspect from a close-up camera.

## Prompts

### 1. Carbonated soda poured from a can into a full bowl

```text
Create a photorealistic 6–8 second Blender animation of a tilted aluminum soda can pouring dark carbonated soda into a ceramic bowl that begins nearly full.

Simulate realistic liquid viscosity, gravity, momentum, splashing, surface tension, and collision with the curved bowl. The stream should break up slightly as it falls, create ripples and small droplets on impact, and swirl around the bowl as the liquid level rises. Because the bowl is already nearly full, the incoming soda should cause a believable overflow over part of the rim and create a small puddle beneath it.

Add a light foam layer and bubbles near the impact area and bowl edges. Include condensation droplets on the cold can. Use a simple studio setup, close-up camera, realistic liquid reflections, 60 fps, and physically believable motion rather than exaggerated splashes.
```

**Physics focus:** inflow, rising liquid level, overflow, splashing, surface tension, foam, and collision handling.

### 2. Thick honey poured onto pancakes

```text
Create a photorealistic close-up Blender animation of honey slowly pouring from a small glass jar onto a stack of three pancakes.

The honey should have noticeably high viscosity, stretching into a thick continuous strand, folding over itself, spreading slowly across the top pancake, and eventually dripping naturally over one edge. Simulate adhesion to the pancake surface, slow pooling, rounded edges caused by surface tension, and one or two long sticky strands forming as the jar moves away.

Keep the scene small and simple: pancakes, plate, jar, honey, tabletop, and one soft area light. Focus on realistic viscous-fluid behavior and macro-level material detail.
```

**Physics focus:** high viscosity, adhesion, slow pooling, strand formation, and surface tension.

### 3. Glass of water overflowing with ice cubes

```text
Create a photorealistic Blender animation of three ice cubes being dropped one after another into an almost-full transparent drinking glass.

Simulate the water displacement realistically: each cube should enter the surface, produce a small crown splash and droplets, temporarily sink, then rise and float due to buoyancy. After the final cube enters, water should overflow naturally over one side of the glass and form a small puddle on the table.

Include realistic refraction through the glass and water, wet surfaces, small trapped air bubbles around the ice, and physically believable floating and rotation of the cubes. Use a locked close-up camera and neutral studio lighting so the fluid behavior is easy to evaluate.
```

**Physics focus:** displacement, impact splash, buoyancy, rigid-body interaction, overflow, and refraction.

## Review checklist

- Fluid scale and gravity feel physically believable.
- Collisions do not visibly leak through containers or surfaces.
- Splashes are proportional to the speed and mass of the impacting object or stream.
- Surface tension is visible without looking gelatinous.
- Overflow follows the container geometry naturally.
- Materials and lighting make the fluid boundary easy to inspect.
- The simulation avoids unexplained volume gain or loss.
