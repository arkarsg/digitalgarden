>[!caution]
>Some derivations are missing

# Position and Orientation
>[!note]
>Projectors are lines that either *converge* at a center of projection or are *parallel*

>[!aside | right +++++]
>Here, we are assuming the projection plane to be flat

Standard projections project onto a plane. Such projections preserve lines but *not necessarily angles*. For applications such as ==map construction==, non-planar projection surfaces are needed.

![[projection.png| -m | -center]]

>[!aside | right +++++]
>Suppose you are projecting an evenly spaced column of pillars. If perspective projection is used, then the spaces between the pillars will not look the same.

```start-multi-column
ID: ID_ocvg
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

>[!note] Orthographic projection
>*Special case* of parallel projection where projectors are *orthogonal* to projection surface. In other words, the line created by the projectors are parallel to the projection surface.

--- column-end ---

>[!note] Perspective Projection
>Projectors *converges* at center of projection. As a result, objects further away from viewer are projection smaller (*diminution*). 
>
>Equal distances along a line are not projected into equal distances (*non-uniform foreshortening*) and *angles* are preserved only in planes ==parallel== to the projection plane.

--- end-multi-column

## Computer Viewing

There are 2 aspects that are implemented in the ==pipeline==.
1. **Positioning the camera** : Setting the model-view matrix
2. **Selecting a lens** : Setting the projection matrix, perspective and the view volume 

![[coordinatetransformation.png| -s | -center]]

### Object space
>[!aside | right +++++]
>When we assign a vertex with `glVertex`, it is by default in their object space. But sometimes, the object space can also be the world space.


- Each object model has its own local coordinate frame. The coordinates of the vertices and vertex normals are specified with respect to the local coordinate frame.

### World space
- A *common* coordinate frame for *all* objects to form the scene to be rendered.
- Each object is transformed from its local space to a common world space. Vertex normals must also be transformed.
- ==Lights== are defined in this space
- ==Camera pose== is defined in this space.

### Camera space
- Also known as the *eye space*

The camera has a local coordinate frame, called the *camera coordinate frame*, following the axes convention.

>[!caution]
>The camera has to look at the negative z-direction because we are using the right-handed coordinate frame

- ==All projections are with respect to the camera frame==
- Initially, the *world* and *camera* frames are the same as the default model-view matrix is an identity matrix.
- To specify the camera pose, we need to specify the *camera coordinate frame* with respect to *world coordinate frame*

---

## View transformation
By default, the *camera frame* coincides with the *world frame*.
>> What should we do if we want to put the camera at other location and orientation?

Position the camera at the required location and orientation with respect to the world frame with `gluLookAt(eyex, eyey, eyez, atx, aty, atz, upx, upy, upz)` function.

>[!aside | right +++++]
>`(up_x, up_y, up_z)` is a direction, not a point

![[cameraspace.png| -m | -center]]

The `eye` and `at` are in the world space. The `eye` specifies the point at which the camera exists and `at` specifies what the “look at” point is. However, the orientation of the camera is ==not constrained==. Therefore, we have to specify a direction in the world space that the camera should follow — `up`.

The derivation of `n, u, v` implies that we can derive the camera space based on the `up` vector.

Internally, it generates a transformation matrix that can be used to express all points in the world frame with respect to the camera frame — this is called ==view transformation==.

>[!caution]
>In OpenGL, the **view transformation** is normally the last transformation in the model-view matrix.

>[!aside | right +++++]
>This is done on a point in the world space


All points in the *world frame* are expressed with respect to *camera frame*.
- This can be done using 4x4 matrix
- It is made up of a translation, then a rotation $M_{view} = \text{R} \space \text{T}$
	- $T$ moves the camera position back to the *world origin*
	- $R$ rotates the axes of the camera frame to coincide with the corresponding axes of the world frame

![[vertextransformationcameratoworld.png| -s | -center]]

### Deriving the view transformation matrix
Suppose the camera has been moved to $e_x, e_y, e_z$, and its $x_c, y_c, z_c$ are the unit vectors $u, v, n$ respectively, then:

>[!aside | right +++++]
>These are all specified w.r.t the **world frame**

$$
M_{view} = 
\begin{bmatrix}
	u_x & u_y & u_z & 0 \\
	v_x & v_y & v_z & 0 \\
	n_x & n_y & n_z & 0 \\
	0 & 0 & 0 & 1
\end{bmatrix}
\cdot
\begin{bmatrix}
	1 & 0 & 0 & -e_x \\
	0 & 1 & 0 & -e_y \\
	0 & 0 & 0 & -e_z \\
	0 & 0 & 0 & 1
\end{bmatrix}
$$

---
# Projection

>[!caution]
>In OpenGL, after a vertex is multiplied by the *model-view* matrix, it is then multiplied by the *projection matrix*.

The projection matrix is a 4x4 matrix that defines the type of projection. The matrix is specified by the *view volume* in the camera frame.
```cpp
glOrtho() // orthographic projection
glFrustum() // perspective projection
```

The *view volume* is specified with respect to the ==camera frame== and is the 3D region of scene to appear in the rendered image.

A ==projection matrix== is then computed such that it maps points in the view volume to a ==canonical view volume== — also known as the ==Normalized Device Coordinates==. The canonical view volume is then [[Camera & Viewing#Viewport transformation| mapped to the viewport]].

>[!note] Canonical view volume
>The canonical volume is a 2x2x2 cube defined by the planes, `x = +/-1, y = +/-1, z = +/- 1`.



## Orthographic projection
The orthographic projection can be specified by defining a view volume in the camera frame using
>> `glOrtho(left, right, bottom, top, near, far)`

The `near` and `far` are not planes in the z-axis, but distances measured in the negative z-direction → `near` and `far` values are positive

The function then generates a matrix that linearly maps the *view volume* to the *canonical view volume*.

- (left, bottom, -near) is mapped to (-1, -1, -1)
- (right, top, -far) is mapped to (1, 1, 1)

![[viewporttocdn.png| -m | -center]]

>[!note] Algorithm to find the mapping
>1. Translate the view volume to origin
>2. Scale the view volume to the size of the canonical view volume

### Projection matrix
The mapping can be found by:
1. **translating** the view volume to the origin
2. **Scaling** the view volume to the size of the canonical view volume

$$
M_{ortho} = S\Big( \frac{2}{{right} - {left}}, \frac{2}{{top} - {bottom}}, \frac{2}{{near} - {far}} \Big) \cdot T \Big( \frac{-({right} - {left})}{2}, \frac{-( {top} - {bottom} ) }{2}, \frac{ {far} + {near}}{2} \Big)
$$

![[orthotransformation.png| -m | -center]]

---

### Viewport transformation

The canonical view volume is then mapped to the viewport.

$z_{win}$ must fall between 0 and 1

![[ndctoviewport.png| -m | -center]]

---

## Perspective projection

In perspective projection, the *center of projection* is at the ==origin== and projection plane lies on $z = d, d < 0$

![[perspectivedivision.png| -m | -center]]

Perspective projection is specified by defining a viewing volume in the camera frame using:
>> `glFrustum(left, right, bottom, top, near, far)`

Note that the `left` of the `near` plane and `far` plane may be different. By convention, we use the `left` coordinates of the near plane.

The `glFrustum` function then generates a matrix that maps the ==view frustum== to the canonical view volume:

![[glfrustumtondc.png| -m | -center]]
### Perspective projection matrix

![[perspectivetransformation.png| -m | -center]]

---
### Perspective projection using field of view

`glFrustum` function allows non-symmetric view volume. For symmetric view volume,
>> `gluPerspective(fovy, aspect, near, far)`



![[frustum.png| -s | -center]]