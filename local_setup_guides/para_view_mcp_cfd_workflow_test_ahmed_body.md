# ParaView MCP CFD Workflow Test: Ahmed Body from Geometry-Only Dataset

For this test, the input dataset contains **only Ahmed body geometry**, for example an STL, OBJ, VTP, or STEP-converted surface. There are **no CFD solution fields** in the original dataset.

The goal is to test whether ParaView MCP can build a complete CFD-style post-processing scene by:

* loading the Ahmed body geometry,
* creating a surrounding flow domain,
* generating synthetic velocity, pressure, wake, and vortex fields,
* visualizing those fields with slices, streamlines, contours, and probes,
* producing a professional CFD-style final layout.

Assume a standard Ahmed body:

* Length: `L = 1.044 m`
* Width: `W = 0.389 m`
* Height: `H = 0.288 m`
* Ground clearance: `G = 0.05 m`
* Rear slant angle: `25 degrees`
* Flow direction: positive `X`
* Lateral direction: `Y`
* Vertical direction: `Z`
* Freestream speed: `U_inf = 40 m/s`
* Air density: `rho = 1.225 kg/m^3`

## 1. Load and Normalize Ahmed Body Geometry

```text
Load the Ahmed body geometry file:
- Open the geometry-only Ahmed body dataset
- Treat the geometry as a solid surface with no existing CFD fields
- Align the body so flow travels in the positive X direction
- Ensure the body length is approximately 1.044 m
- Ensure the body width is approximately 0.389 m
- Ensure the body height is approximately 0.288 m
- Place the lowest body surface approximately 0.05 m above the ground plane
- Set the body centerline at Y = 0
- Set the ground plane at Z = 0
- Display the body as a smooth gray surface
- Reset the camera to show the entire body
```

## 2. Create CFD Wind Tunnel Domain

```text
Create a synthetic wind tunnel domain around the Ahmed body:
- Domain length: from X = -2.0 m upstream to X = 5.0 m downstream
- Domain width: from Y = -1.2 m to Y = 1.2 m
- Domain height: from Z = 0.0 m to Z = 1.2 m
- Create a structured image/grid volume covering this domain
- Use resolution approximately 220 x 90 x 80 cells
- Name the volume "Synthetic_Ahmed_CFD_Domain"
- Show the outer domain as a transparent box
- Keep the Ahmed body visible inside the domain
```

## 3. Generate Synthetic Velocity Field

```text
Create a synthetic velocity vector field named "U" on the CFD domain.

Use positive X as the freestream direction.

Generate a plausible Ahmed-body external aerodynamics field:
- Freestream velocity: Ux = 40 m/s far from the body
- Reduce velocity near the front stagnation region
- Increase velocity over the roof and side shoulders
- Create a wake deficit behind the rear base and slant
- Create a low-speed recirculation bubble behind the body
- Add weak downward flow behind the rear slant
- Add lateral velocity components that curve around the body sides
- Add counter-rotating wake swirl behind the body

The field does not need to be a real CFD solution, but it should be physically plausible and useful for visualization.

Create these point arrays:
- U: vector velocity field
- U_mag: velocity magnitude
- wake_deficit: scalar from 0 to 1 showing wake strength
- recirculation: scalar mask for reversed or very-low-speed wake flow
```

## 4. Generate Synthetic Pressure and Cp Fields

```text
Create synthetic pressure fields on the CFD domain:
- Use rho = 1.225 kg/m^3
- Use U_inf = 40 m/s
- Create static pressure field "p"
- Create pressure coefficient field "Cp"

The pressure field should show:
- High pressure at the front stagnation region
- Lower pressure over the roof
- Lower pressure on the rear slant
- Low base pressure behind the Ahmed body
- Gradual pressure recovery downstream in the wake

Create these scalar arrays:
- p
- Cp
- pressure_recovery
```

## 5. Create Surface Proxy Fields on the Ahmed Body

```text
Create synthetic surface fields on the Ahmed body geometry:
- Map or calculate approximate pressure coefficient on the body surface
- Name the surface pressure field "Cp_surface"
- Create higher Cp near the front face
- Create lower Cp on the roof and rear slant
- Create strongly negative Cp on the rear base
- Create a synthetic wall shear proxy named "wall_shear_proxy"
- Make wall_shear_proxy higher on the roof and side edges
- Make wall_shear_proxy lower in separated rear regions

Display the Ahmed body colored by Cp_surface using a diverging color map.
Add a scalar legend.
```

## 6. Verify Created Fields

```text
Inspect the generated dataset and report the available arrays:
- Confirm the domain contains U, U_mag, p, Cp, wake_deficit, recirculation
- Confirm the Ahmed body surface contains Cp_surface and wall_shear_proxy
- Confirm that U is a vector field
- Confirm that U_mag, Cp, and wake_deficit are scalar fields
- Confirm the geometry itself originally had no CFD fields
- Report any missing arrays before continuing
```

## 7. Ahmed Body Overview Scene

```text
Create a clean geometry overview:
- Show the Ahmed body as an opaque gray surface
- Show the ground plane as a light neutral surface
- Show the wind tunnel domain as a transparent outline
- Add an inlet arrow labeled "U_inf = 40 m/s"
- Add coordinate axes
- Use a three-quarter front view
- Keep the scene uncluttered
```

## 8. Centerline Velocity Slice

```text
Create a centerline slice at Y = 0:
- Slice the synthetic CFD domain through the Ahmed body centerline
- Color the slice by U_mag
- Use a consistent range from 0 to 60 m/s
- Show the Ahmed body as a solid black or dark gray silhouette
- Make the front stagnation region visible
- Make roof acceleration visible
- Make the rear wake velocity deficit visible
- Add a scalar legend labeled "Velocity Magnitude [m/s]"
```

## 9. Horizontal Wake Slice

```text
Create a horizontal wake slice:
- Place the slice at Z = 0.18 m
- Color by U_mag
- Use the same 0 to 60 m/s color range
- Show the Ahmed body outline
- Reveal the wake width behind the vehicle
- Make the side shear layers visible
- Add a clear camera view from above
```

## 10. Cross-Flow Wake Slices

```text
Create four downstream wake slices normal to the X direction:
- Slice 1 at X = 1.2 m
- Slice 2 at X = 1.8 m
- Slice 3 at X = 2.6 m
- Slice 4 at X = 3.6 m
- Color all slices by wake_deficit
- Use the same scalar range from 0 to 1
- Arrange them so the wake growth and recovery are easy to compare
- Keep the Ahmed body visible for reference
```

## 11. Pressure Coefficient on Body

```text
Visualize pressure coefficient on the Ahmed body surface:
- Color the body by Cp_surface
- Use a diverging color map centered around Cp = 0
- Use a range approximately from -1.5 to 1.0
- Show high pressure on the front face
- Show suction over the roof and rear slant
- Show low pressure on the rear base
- Add a scalar legend labeled "Cp"
```

## 12. Streamlines Around the Ahmed Body

```text
Generate streamlines using the synthetic velocity field U:
- Seed streamlines from an upstream plane at X = -1.5 m
- Use seed points spanning Y = -0.5 m to 0.5 m and Z = 0.08 m to 0.55 m
- Integrate streamlines in the positive X direction
- Color streamlines by U_mag
- Use tube rendering for visibility
- Use moderate density, not too cluttered
- Show streamlines accelerating over the roof
- Show streamlines bending around the sides
- Show disturbed streamlines in the wake
```

## 13. Wake Recirculation Region

```text
Visualize the synthetic recirculation bubble:
- Threshold or contour the recirculation scalar
- Show regions where recirculation is high
- Place the recirculation region behind the rear base and slant
- Render it as a semi-transparent volume or isosurface
- Use a distinct material so it reads as the separated wake
- Keep the Ahmed body visible
- Add a label "Synthetic recirculation region"
```

## 14. Vortex Structure Visualization

```text
Create synthetic vortex structures behind the Ahmed body:
- Use the generated swirl or vortex metric field
- If no vortex metric exists, create one named "vortex_core_proxy"
- Place two main counter-rotating longitudinal vortices behind the rear slant
- Add weaker side-edge vortices behind the body shoulders
- Create isosurfaces of vortex_core_proxy
- Color vortex structures by U_mag or Cp
- Use semi-transparent rendering
- Make the wake topology visually clear
```

## 15. Wake Profile Probe

```text
Create quantitative wake probes:
- Add a line probe across the wake at X = 2.0 m
- Probe from Y = -0.8 m to Y = 0.8 m at Z = 0.18 m
- Plot U_mag versus Y
- Add another line probe along the wake centerline
- Probe from X = 1.05 m to X = 5.0 m at Y = 0 and Z = 0.18 m
- Plot U_mag versus X
- Label plots clearly
- Use the plots to show wake deficit and downstream recovery
```

## 16. Synthetic Time-Dependent Wake

```text
Create a simple synthetic time-dependent wake animation:
- Add 40 time steps
- Keep the body and freestream fixed
- Oscillate the wake deficit slightly from side to side
- Add alternating vortex shedding behind the Ahmed body
- Keep the motion subtle and physically plausible
- Use a fixed camera
- Use a fixed U_mag color range from 0 to 60 m/s
- Add a time annotation
```

## 17. Final CFD Report Layout

```text
Create a final report-style ParaView layout:
- Main 3D view: Ahmed body, streamlines, recirculation bubble, and vortex structures
- Top-right view: centerline velocity slice
- Bottom-right view: Cp_surface on the Ahmed body
- Bottom-left view: wake profile plot at X = 2.0 m
- Use consistent color maps and scalar ranges
- Add legends with readable labels
- Add annotations explaining that the fields are synthetic
- Make the final result look like a professional CFD visualization, not a raw geometry render
```

## 18. Export Outputs

```text
Export the results:
- Save a high-resolution screenshot of the final layout
- Save a screenshot of the centerline velocity slice
- Save a screenshot of Cp on the Ahmed body
- Save a screenshot of streamlines and wake structures
- Export wake profile plot data as CSV
- Save the ParaView state file
- Use filenames beginning with "ahmed_synthetic_cfd_"
```

## One-shot CFD Field Generator Prompt

Use this after the Ahmed body geometry has been loaded:

```text
The loaded dataset contains only Ahmed body geometry and no CFD fields. Create a synthetic CFD post-processing dataset around it.

Use a standard Ahmed body scale: L = 1.044 m, W = 0.389 m, H = 0.288 m, ground clearance = 0.05 m, flow in +X, U_inf = 40 m/s, rho = 1.225 kg/m^3.

Create a structured volume domain from X = -2.0 to 5.0 m, Y = -1.2 to 1.2 m, Z = 0.0 to 1.2 m. Generate physically plausible synthetic fields:
- U vector velocity
- U_mag
- p
- Cp
- wake_deficit
- recirculation
- vortex_core_proxy

The fields should show front stagnation, roof acceleration, side acceleration, low base pressure, separated wake, counter-rotating rear vortices, and downstream wake recovery. These fields are synthetic and should be clearly labeled as synthetic, not solver results.
```

## One-shot CFD Visualization Director Prompt

After the synthetic fields and views exist:

```text
Review the entire Ahmed body synthetic CFD visualization as a CFD post-processing expert. Improve field ranges, camera views, slice positions, streamline seeding, vortex thresholds, legends, annotations, plot readability, and final layout. Make it clear that the original dataset was geometry-only and that the CFD fields were generated synthetically for visualization workflow testing.
```

## Audit Prompt

```text
Audit this ParaView workflow for correctness:
- Confirm the original Ahmed body file was geometry-only
- Confirm all CFD fields were generated inside ParaView
- Confirm U is a vector field and U_mag is derived correctly
- Confirm Cp uses U_inf = 40 m/s and rho = 1.225 kg/m^3
- Confirm slices are placed through meaningful wake regions
- Confirm streamline seeds are upstream of the Ahmed body
- Confirm wake and vortex structures are labeled as synthetic
- Confirm plots and screenshots do not imply these are validated CFD solver results
- Identify misleading visuals, bad color ranges, excessive clutter, or incorrect scaling
```
