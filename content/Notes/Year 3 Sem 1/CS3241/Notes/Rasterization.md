>[!note]- Recall: Rendering pipeline
>![[Image formation#Rendering pipeline]]


# OpenGL rendering pipeline

To render a primitive using OpenGL, the primitive goes through the following main stages:

![[openglpipeline.png]]

---

# Modeling
Modelling provides a *set of vertices* that specifies geometric objects.

- Examples of attributes at a vertex
	1. Color
	2. Material
	3. Vertex normal
	4. Texture coordinates

May perform scene processing to reduce amount of geometric data passed to rendering pipeline, *view-frustum culling, occlusion culling*

---

# Vertex processing

==Model-View== transformation of each vertex to *camera space*, which transforms the vertex normal too.

- Vertex colors are assigned here using [lighting computation](Illumination.md).
- [Texture](Texture%20Mapping.md) coordinates are also computed here
- Performs multiplication with *projection* matrix to clip space

---

# Primitive Assembly

![[spacepipeline.png|300]]

Some operations occur at this stage:
- Vertex data is collected into complete primitives
- Necessary for [[Rasterization#Clipping | clipping]] and [[Rasterization#Back-face culling | back-face culling]]
- Perspective division to [[Camera & Viewing | NDC space]]
- Viewport transformation to [[Camera & Viewing#Viewport transformation | window space]]

---

# Rasterization

>[!note]
>This stage determines which pixels are inside primitive specified by a set of vertices.

If geometric primitive is not clipped out, the appropriate pixels in the frame buffer must be assigned colors

>[!note] Fragments
>Rasterizer produces a set of ==fragments== for each primitive.
>
>Fragments are *potential pixels* which has a pixel location and color and depth attributes which are interpolated over the primitive.


## Interpolation of vertex attributes
Attribute values at fragments are computed by interpolating attribute values assigned to vertices. ==Interpolation is performed in 2D window space==.

### Bilinear interpolation of attribute
>[!note]
>The rasterizer produces fragments row by row horizontally — with a scan line.

The result of a bilinear interpolation on a quadrilateral may not be invariant to rotation and transformation. But it is stable for ==triangles==.

![[bilinearinterpolation.png|500]]

### Color interpolation
To give an appearance of smoothness, assign each vertices to different colors. Then, in each polygon, there will be a color interpolation to give an appearance of smoothness.

>[!caution]
>The different colors of each vertices are computed with ligthing computation.
>
>The combination of *lighting computation* and *color interpolation* is also known as ==Gouraud shading==

![[gouradshading.png|500]]

## Scan conversion of line segments

### Digital Differential Analyzer
Line $y = mx + b$ satisfies the differential equation
$$
dy/ dx = m = \Delta y / \Delta x = (y_e - y_0) / (x_e - x_0)
$$

- $0 \leq |m| \leq 1 \implies$ plot pixel with respect to $x$
- $|m| \geq 1 \implies$ plot pixel with respect to $y$
- Uses floating points operations → inefficient

---

### Bresenham’s algorithm
- Does not use floating point operations
#### Intuition
If we start at a pixel that has been written, there are only two candidates for the next pixel. This turns the problem into a binary decision problem.
#### Approach

We have the line $y = m(x_k + 1) + b$, and define $y_k$ as the position of the pixel center along the $y$-axis.

$$
d_{lower} = y - y_k
$$
$$
d_{upper} = (y_k + 1) - y
$$

Then, we have

>[!note]
>The change in $x$ is not $1$. It is in change in the end point

$$
p_k = \Delta x (d_{lower} - d_{upper}) \\
= 2 x_k \Delta y - 2 y_k \Delta x + c
$$

- If $p_k < 0$, plot lower pixel
- If $p_k > 0$, plot upper pixel

Note that this is incrementally computed from $p_0$. In other words, $p_{k+1}$ is computed from $p_k$.
![IncrementalForm|300](Screenshot%202023-11-30%20at%201.38.24%20PM.png)

- If $p_k < 0, \enspace p_{k+1} = p_k + 2\Delta{y}$
- If $p_k > 0, \enspace p_{k+1} = p_k + 2\Delta{y} - 2\Delta{x}$

where $p_0 = 2\Delta{y} - \Delta{x}$

---

## Polygon scan conversion

- Scan line fill is done on convex polygons only (usually triangles)
	- Non-convex polygons are assumed to be *tessellated*
- This is usually combined with ==z-buffer algorithm==

![[scanlineorder.png|80%]]

---

# Fragment processing

Each generated fragment is processed to determine the color of the corresponding pixel in the frame buffer

>[!caution]
>Even though the fragment can be assigned by the rasterizer, the color may still change with texture mapping.

- Texture access using interpolated texture coordinates (access texture map using texture coordinates)
- Texture application — combine fragment color of the primitive and texture color
---

# Per-fragment operations

- Fragment is discarded if it is blocked by the corresponding pixel already in the frame buffer using ==z-buffer hidden-surface removal==
- Fragment may be blended with the corresponding pixel already in the frame buffer — ==blending== (usually for translucent/ transparent objects)

---

# Clipping

>[!caution] Clipping
>Clipping is done after [[Rasterization#Primitive Assembly]] after vertices have been assembled into primitives and primitives outside the *view volume* must be clipped out.

Clipping is done against *clipping window* for 2D objects, *clipping volume* for 3D objects
## Clipping 2D/ 3D line segments

### Cohen-Sutherland
#### Intuition
- Eliminate as many *easy* cases
#### Approach
- Draw 4 lines that determine the sides of the clipping window

![[boundary.png|50%]]

**Case 1** : Both endpoints inside all four lines
- Draw line segment as is

**Case 2** : Both endpoints outside same line
- Discard the line segment

**Case 3** : One endpoint inside all lines and one outside
- Must do *at least* one intersection

**Case 4** : Both outside
- May have a part inside
- Must do *at least* one intersection
---
### Outcode representation

$4$-bit representation

![[outcode.png|80%]]
- Computation of outcode requires at most 4 subtractions

Consider line segments in that lie on different parts of the outcode
- What happens when you bitwise `AND`?
- Neither zero but logical `AND` yields zero?

#### Cases

1. **`outcode(A) = outcode(B) = 0` → both are inside the viewport**
	- Accept the line segment
2. **`outcode(A) = 0, outcode(B) != 0` → one point inside and one point outside**
	- Location of `1` in `B` determines which edge to intersect with. If `B` has 2 `1`s → two intersections
3. **`outcode(A) & outcode(B) != 0` → both points lie on the outside**
	- `BITWISE AND` is not 0
	- Both outcodes have a `1` in the same bit location → line is outside of corresponding side of clipping window
	- Reject line segment
5. **`outcode(A) != 0 & outcode(B) != 0 & (outcode(A) & outcode(B) = 0)`**
	- Shorten line segment by intersection with one side of the window
	- Compute outcode of intersection (new endpoint of shortened line segment)
	- Re-execute algorithm

---

### In 3D space…
Use $6$-bit representation
- Clip line segment against planes

![[3doutcode.png|80%]]

---
## Clip space
A vertex is in clip space after multiplication by projection matrix and before perspective division and has the ==homogeneous coordinates==
$\begin{bmatrix}x_{clip} & y_{clip} & z_{clip} & w_{clip} \end{bmatrix} ^{T}$

If it is in *canonical view volume* $[-1, 1]^3$ then, it must be that
![[clipcdn.png|80%]]

---

### Pipeline clipping of line segments
![[pipelineclipping.png|80%]]

---

### Polygon clipping
- Line segment results in at most 1 line after clipping
- Clipping a polygon may yield multiple polygons
- Clipping a convex polygon can yield at **most** one other polygon

==Strategy== : Replace *non-convex* polygons with a set of smaller simple polygons (a tessellation of triangles)

#### Pipeline clipping of polygons
Clip top, bottom, right, left for 2D objects. For 3D, add front and back clippers.

#### Simple early acceptance and rejection
Rather than doing clipping on complex polygon, use an **axis-aligned bounding box** — the smallest axis aligned rectangle that encloses the polygon.

This is simple to compute: $\min$ and $\max$ of $x$ and $y$

![[pipeline clipping.png|80%]]

---

# Hidden surface removal
>[!note] Similarities between clipping and hidden surface removal
>In both cases, we are trying to remove objects that are not visible to the camera

Often, we use *visibility* or *occlusion testing* early in the process to eliminate as many polygons as possible before going through the entire pipeline

---

## Painter’s algorithm
- Render polygons ==back-to-front== order so that polygons behind others are simply painted over

---

## Depth sorting
This is a *object-space* approach where objects are sorted using a *pair-wise* testing
- **Worst case** $O(n^2)$
- $O(n \log n)$ possible

---

## Back-face culling
- Eliminate polygon if it is back-facing and invisible.
- A polygon is back-facing if $N_p \cdot N < 0$
![[backfaceculling.png|80%]]

---

## Image Space approach
![[imagespace.png|80%]]

---

## z-Buffer algorithm
- Uses a ==z-buffer== or depth buffer to store the depth of the **closest** object at each pixel found so far
- As we render each polygon, compare the depth of each fragment to the depth in z-buffer
- If less than, place fragment in color buffer and its depth in z-buffer
	- The fragment has become the new closest so far at that pixel location
- Else, discard fragment

---

# z-fighting
- Occurs when two or more primitives have similar or identical values in the *z-buffer*
- Two faces occupy the same space, with neither in front.
- Affected pixels are rendered with fragments arbitrarily determined by the precision of the *z-buffer*
- Results in flickering or noisy rasterization

>[!note]
>This is caused by limited *sub-pixel precision* and floating point and fixed point round-off errors

### Minimising z-fighting
- **Minimise** the distance between the near and far planes
- Smaller range of depth values mapped to 0 to 1
- Able to resolve different *eye-space* z-coordinate values with **higher precision**

---