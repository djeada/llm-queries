# Replacement Notes: Smaller ParaView MCP CFD Workflow Tests

## Why replace the original test

The original Ahmed-body workflow is too large for a reliable model/tool evaluation because it asks one run to do many things at once:

- load and normalize geometry
- create a synthetic wind-tunnel domain
- generate velocity, pressure, wake, recirculation, and vortex fields
- make slices, streamlines, contours, probes, animation, and final report layouts
- export screenshots, CSV data, and ParaView state files

That makes failures hard to diagnose. A model can fail because it misunderstands CFD, because ParaView automation fails, because the visualization is too cluttered, or because the final layout/export step is too complex.

The replacement should use small, exact, inspectable tasks. Each task should test one concept or one ParaView operation.

---

# Replacement Test Set: Velocity Field First

## Test 1 — Geometry-only dataset sanity check

### Goal
Confirm that the input contains only Ahmed body geometry and no CFD solution fields.

### Prompt

```text
Load the Ahmed body dataset.

Inspect the dataset and report:
1. Does the dataset contain geometry?
2. Does the dataset contain any existing CFD velocity field?
3. Does the dataset contain pressure, Cp, wake, or vortex fields?
4. Is this a geometry-only dataset?

Do not create any new fields yet.
Do not create streamlines.
Do not create pressure.
Do not create a final report layout.
```

### Expected output

```text
Geometry present: yes
Existing velocity field: no
Existing pressure/Cp fields: no
Existing wake/vortex fields: no
Dataset type: geometry-only
Result: pass/fail
```

### Pass criteria

Pass if the model correctly identifies that the original dataset is geometry-only and does not pretend that CFD fields already exist.

---

## Test 2 — Explain what a velocity field is

### Goal
Test conceptual understanding before asking the model to create or visualize anything.

### Prompt

```text
Explain what a velocity field is in ParaView/CFD terms.

Use this Ahmed body setup:
- flow direction is +X
- freestream velocity is 40 m/s
- the dataset is geometry-only and has no CFD fields initially

Answer these exactly:
1. Is a velocity field the same thing as streamlines?
2. What does the vector field U contain?
3. What does U_mag mean?
4. Where can U be stored: on points, cells, or the geometry surface?
5. What is needed before ParaView can draw streamlines?
```

### Expected answer

```text
A velocity field is not the same thing as streamlines.

A velocity field is a vector field defined over a domain. At each point or cell, it stores a vector:

U = (Ux, Uy, Uz)

For this Ahmed body setup:
- Ux is the velocity component in the flow direction
- Uy is the side-to-side component
- Uz is the vertical component
- far from the body, U should be approximately (40, 0, 0) m/s

U_mag is the velocity magnitude:

U_mag = sqrt(Ux^2 + Uy^2 + Uz^2)

Streamlines are derived from U. ParaView draws streamlines by seeding points and integrating paths through the vector field.
```

### Pass criteria

Pass if the model clearly distinguishes the velocity field from streamlines.

Fail if the model says streamlines are the velocity field.

---

## Test 3 — Create only a simple synthetic velocity field

### Goal
Create one synthetic vector field without adding pressure, Cp, vortices, animation, or a final layout.

### Prompt

```text
The loaded Ahmed body dataset contains geometry only and no CFD solution fields.

Create one synthetic velocity vector field named U on a surrounding volume domain.

Use:
- flow direction: +X
- freestream speed: 40 m/s
- far-field velocity: U = (40, 0, 0) m/s

The field should contain only these simple effects:
1. slower velocity in front of the body
2. faster velocity over the roof
3. slower velocity behind the rear wake
4. weak side velocity around the body

Also create U_mag from U.

Do not create pressure.
Do not create Cp.
Do not create vortices.
Do not create recirculation.
Do not create animation.
Do not create final report layout.
```

### Expected created arrays

```text
U      vector, 3 components, units m/s
U_mag  scalar, velocity magnitude, units m/s
```

### Pass criteria

Pass if:

- array U exists
- U has 3 components
- array U_mag exists
- U_mag is scalar
- far upstream U_mag is close to 40 m/s
- wake region behind the body has lower U_mag than freestream
- no pressure, Cp, vortex, or animation fields are created

---

## Test 4 — Verify U and U_mag only

### Goal
Make field verification narrow and objective.

### Prompt

```text
Inspect the dataset after creating the synthetic velocity field.

Report exactly:
1. Does array U exist?
2. Is U a vector field?
3. How many components does U have?
4. Does U_mag exist?
5. Is U_mag scalar?
6. What are the approximate min and max values of U_mag?
7. Is the field clearly labeled as synthetic?

Do not create new fields.
Do not create visualizations.
```

### Expected output format

```text
U exists: yes/no
U components: 3 / not 3
U_mag exists: yes/no
U_mag range: min to max m/s
Synthetic label present: yes/no
Result: pass/fail
```

### Pass criteria

Pass if the response gives array existence, component count, scalar/vector type, and approximate velocity magnitude range.

---

## Test 5 — Make one centerline velocity slice

### Goal
Test one simple visualization derived from U_mag.

### Prompt

```text
Create one centerline slice through the synthetic velocity domain.

Use:
- slice plane: Y = 0
- color by U_mag
- color range: 0 to 60 m/s
- show the Ahmed body as a dark solid silhouette
- add a scalar legend labeled "Velocity Magnitude [m/s]"

The slice should show:
1. slower velocity near the front stagnation region
2. faster velocity over the roof
3. slower velocity in the rear wake

Do not create streamlines.
Do not create pressure.
Do not create Cp.
Do not create vortices.
Do not create animation.
Do not create final report layout.
```

### Pass criteria

Pass if there is one centerline slice at Y = 0 colored by U_mag with a 0–60 m/s range.

Fail if the model creates many extra views or unrelated fields.

---

## Test 6 — Explain streamlines before creating them

### Goal
Check whether the model understands that streamlines are computed from a velocity field.

### Prompt

```text
Before creating streamlines, answer:

1. Are streamlines input data or a visualization derived from U?
2. What does ParaView need in order to compute streamlines?
3. Why would streamlines be impossible on the original geometry-only dataset before U was created?

Do not create anything in this step.
```

### Expected answer

```text
Streamlines are derived visualizations, not original input data.

ParaView needs a vector velocity field such as U and seed points or a seed source.

On the original geometry-only dataset, streamlines are impossible because there is no vector field to integrate through.
```

### Pass criteria

Pass if the model says streamlines require a vector velocity field and cannot be computed directly from geometry alone.

---

## Test 7 — Create streamlines from U

### Goal
Create one streamline visualization from the previously generated velocity field.

### Prompt

```text
Create streamlines using the existing synthetic velocity field U.

Use:
- seed plane at X = -1.5 m
- seed region from Y = -0.5 m to 0.5 m
- seed region from Z = 0.08 m to 0.55 m
- integrate in the positive X direction
- color streamlines by U_mag
- use tube rendering for visibility
- use moderate density, not too cluttered

The streamlines should show:
1. flow over the roof
2. flow bending around the sides
3. disturbed flow in the wake

Do not create pressure.
Do not create Cp.
Do not create vortices.
Do not create animation.
Do not create final report layout.
```

### Pass criteria

Pass if streamlines are seeded upstream and integrated through U.

Fail if streamlines are treated as an original dataset field instead of a visualization derived from U.

---

## Test 8 — State what the visualization does and does not prove

### Goal
Prevent misleading CFD claims.

### Prompt

```text
Review the current visualization and write a short note explaining what it does and does not prove.

The note must say:
- the original dataset was geometry-only
- the velocity field U is synthetic
- U_mag is derived from U
- streamlines are derived from U
- the result is useful for workflow testing and visualization testing
- the result is not a validated CFD solver result
```

### Expected note

```text
This visualization uses an original geometry-only Ahmed body dataset. The velocity field U was generated synthetically for workflow testing. U_mag was computed from U, and the streamlines were integrated through U.

The result is useful for testing ParaView automation, visualization layout, color mapping, slicing, and streamline generation. It should not be interpreted as a validated CFD solver result or as physically validated aerodynamic data.
```

### Pass criteria

Pass if the note clearly labels the fields as synthetic and avoids implying solver validation.

---

# Recommended Test Order

Run the tests in this order:

```text
1. Geometry-only dataset sanity check
2. Explain what a velocity field is
3. Create only U and U_mag
4. Verify U and U_mag
5. Make one centerline velocity slice
6. Explain streamlines
7. Create streamlines from U
8. State what the visualization does and does not prove
```

This order keeps each step small and debuggable.

---

# What to remove from the first replacement version

Do not include these in the first simplified test suite:

- synthetic pressure field p
- pressure coefficient Cp
- Cp_surface
- wall_shear_proxy
- wake_deficit scalar
- recirculation scalar
- vortex_core_proxy
- cross-flow wake slices
- wake probes and plots
- time-dependent animation
- final multi-view report layout
- screenshot and CSV export requirements

These can be added later as separate test modules after the velocity-field tasks are reliable.

---

# Optional later modules

After the velocity-field tests pass consistently, add later modules one at a time:

## Later Module A — Pressure only

Create p and Cp from the synthetic velocity field. Do not create streamlines or vortices.

## Later Module B — Wake scalar only

Create wake_deficit as a scalar field. Visualize one wake slice. Do not create pressure or vortices.

## Later Module C — Recirculation only

Create a simple recirculation mask behind the body. Show one transparent isosurface.

## Later Module D — Vortex proxy only

Create vortex_core_proxy and show two counter-rotating rear structures. Keep it clearly labeled as synthetic.

## Later Module E — Final layout only

Only after the individual components work, assemble a final report layout.

---

# Minimal one-shot replacement prompt

Use this if only one compact prompt is needed:

```text
The Ahmed body dataset is geometry-only and contains no CFD solution fields.

Create a simple synthetic velocity field only.

Use:
- flow direction: +X
- freestream velocity: U = (40, 0, 0) m/s
- create U as a 3-component vector field
- create U_mag as sqrt(Ux^2 + Uy^2 + Uz^2)

The field should show only:
1. reduced speed in front of the body
2. increased speed over the roof
3. reduced speed in the rear wake
4. weak side flow around the body

Then verify:
- U exists and has 3 components
- U_mag exists and is scalar
- far upstream U_mag is about 40 m/s
- wake U_mag is lower than freestream

Finally create one visualization:
- centerline slice at Y = 0
- color by U_mag
- color range 0 to 60 m/s
- body shown as dark silhouette

Do not create pressure, Cp, recirculation, vortices, probes, animation, exports, or a final report layout.
Label the field as synthetic and not a validated CFD solver result.
```
