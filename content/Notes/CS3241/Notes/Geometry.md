# Basics
==Geometry== is the study of the spatial relationships among objects in an $n$-dimensional space.

In computer graphics, we want the *minimum* set of primitives from which we can build more sophisticated objects

*3* basic elements:
1. Scalars
2. Vectors
3. Points

## Scalars
>[!note] Definition
> Members of sets which can be combined by 2 operations (addition and multiplication), obeying some fundamental axioms (associativity, commutativity, inverses)

Scalars alone have no geometric properties.

---

## Vectors
>[!note] Definition
>A *vector* is a quantity with direction and magnitude.

1. Every vector has an inverse which is another vector equal in magnitude but in opposite direction.
2. Every vector can be *multiplied* by a scalar.
3. Zero vector exists which has zero *magnitude* but undefined direction.
4. Sum of any two vectors is a vector

>[!caution]
>Vector spaces insufficient for geometry. Vector spaces need points.

---

## Points
>[!note] Definition
>Points are a location in space.

Point-point subtraction yields a vector.

>[!caution]
>Note that the explicit form $y = mx + c$ is a membership test and therefore, not a good choice for drawing a line.

---

## Planes

>[!caution] Normal vectors
>Normal vectors are important for lighting computation

For a plane in the for $ax + by + cz + d = 0$, the ==normal vector== is $(a, b, c)$.

---

# Coordinate systems

>[!aside | right +++++]
>A basis is a set of *linearly independent vectors*.

Consider a *basis* $v_1, v_2, … , v_n$ → this forms the coordinate systems that are agreed on.

A *vector* is written $v = \alpha_1 v_1 + \alpha_2 v_2 + ... + \alpha_n v_n$, then the list of scalars ${\{ \alpha_1, \alpha_2, ... , \alpha_n\}}$ is the *representation* of $v$ with respect to the given basis.

We can write the representation as a row of ==column array== of scalars. This is the *transpose* function.

$$
v = 2v_1 + 3v_2 - 4 v_3
$$
$$
\text{a} = \begin{bmatrix}2 & 3 & -4 \end{bmatrix} ^{T}
$$

>[!note]
>Coordinate systems are for describing ==vectors==.

---

# Frames

>[!caution]
>A coordinate system is insufficient to represent points.
>
>A coordinate system alone is insufficient to represent points because points in space not only have spatial coordinates but also possess a notion of position or location. A coordinate system provides a framework for specifying the spatial coordinates of points, but it does not capture their individual positions or relationships to other points.
>
>To fully represent a point in space, you need both the coordinates within a coordinate system and a reference or origin point. This combination is known as a frame or frame of reference. A frame includes the coordinate system and an additional reference point that provides the position or location of the point within that coordinate system.
>
>By incorporating a reference point, a frame allows for a more complete representation of points in space, considering both their spatial coordinates and their positions relative to the frame's origin. This information is essential for accurately describing and manipulating points in geometric calculations and transformations.

If we work in an *affine space*, we can add ==the origin==, to the basis vectors to form a frame. Therefore, a ==frame== has a *coordinate system* and a *point*.

Therefore, a frame is determined by,
$$
(P_0, v_1, v_2, v_3)
$$

And within this frame,
- every *vector* can be written as $v = \alpha_1 v_1 + \alpha_2 v_2 + ... + \alpha_n v_n$, and
- every *point* can be written as $P = P_0 + \beta_1 v_1 + \beta_2 v_2 + ... + \beta_n v_n$

Note that these can be rewritten as a product of the basis with the origin and the transpose of the representation.

This is the *four-dimensional homogeneous coordinate* representation for 3D space.

>[!summary]
>The key idea in an affine space is that it captures the concept of relative positions and movements without specifying an absolute origin. This makes it suitable for describing and working with geometric properties and transformations that are independent of a specific coordinate system or reference point.

Note that we have the same representation
- For point $\text{p} = \begin{bmatrix}\beta_1 & \beta_2 & \beta_3 \end{bmatrix} ^{T}$
- For vector $\text{v} = \begin{bmatrix}\alpha_1 & \alpha_2 & \alpha_3 \end{bmatrix} ^{T}$

Since a vector has no position, we can rewrite as follows:
- For point $\text{P} = \begin{bmatrix}v_1 & v_2 & v_3 & P_0 \end{bmatrix} \begin{bmatrix}\beta_1 & \beta_2 & \beta_3 & 1 \end{bmatrix} ^{T}$
-  For vector $\text{v} = \begin{bmatrix}v_1 & v_2 & v_3 & P_0 \end{bmatrix} \begin{bmatrix}\alpha_1 & \alpha_2 & \alpha_3 & 0 \end{bmatrix} ^{T}$

Which leads us to *homogeneous coordinates*

---

# Homogeneous coordinates
>[!note] Motivation
>1. To have different representations to distinguish between *points* and *vectors*
>2. To do translation using matrix multiplication
>3. To allow perspective projection using matrix multiplication and perspective division


The homogeneous coordinates for a *three dimensional* point $[x \space y \space z]^{T}$ is given as
$$
\text{p} = \begin{bmatrix} x' & y' & z' & w \end{bmatrix} ^T = \begin{bmatrix} wx & wy & wz & w \end{bmatrix} ^T
$$

>[!aside | right +++++]
>If $w \neq 1 \& w \neq 0$, then the value of $x, y, z$ is not the true coordinates. Then, to get the real $x, y, z$ coordinates, we need to divide by $w$. This is called ==perspective projection==.

Note that if $w = 0$, the representation is that of a ==vector==. The homogeneous coordinates replace points in 3D by lines through the origin in 4D.

For $w = 1$, the representation of a point is $[x \space y \space z \space 1 ] ^{T}$.

>[!caution]
>All standard transformations (rotation, translation, scaling) can be implemented with matrix multiplications using 4 x 4 matrices.

>[!caution]
>Hardware pipeline works with 4 dimensional representations.

For orthographic viewing we can maintain $w = 0$ for vectors and $w = 1$ for points.

For perspective viewing, use ==perspective division==.

---

# Transformations

>[!note]
>We need only transform endpoints of line segments and let implementation draw line segment between the transformed endpoints.
>
> ==Motivation for using homogeneous coordinates==
> Note that for translation it is a vector addition. However, other transformations are matrix multiplication. With the use of homogeneous coordinates, *all transformations* can be matrix multiplication.

## Affine transformations

Characteristics of affine transformations:
- **Line preserving** : a line segment may undergo multiple transformations but will remain as a straight line. This implies that there is no need to transform *every single point*, but just the *ends* and will remain as a line.
- **Rigid body transformation** : rotation or scaling without changing the shape of the object → this is an affine transformation and cannot be done in linear transformation.

---

## Translation
Translation has *3* degrees of freedom and the ==displacement== is determined by a vector $d$.

To represent translation with the homogeneous coordinate representation,
$$
\text{d} = \begin{bmatrix}
d_x & d_y & d_z & 0
\end{bmatrix}
^{T}
$$

We can also express translation using a 4 x 4 matrix $\text{T}$  in homogeneous coordinates.
$$
\text{T} = \text{T}(d_x, d_y, d_z) = 
	\begin{bmatrix}
		1 & 0 & 0 & d_x \\
		0 & 1 & 0 & d_y \\
		0 & 0 & 1 & d_z \\
		0 & 0 & 0 & 1
	\end{bmatrix}
$$

$$
\text{p'} = \text{T} \text{p} = \begin{bmatrix}
		1 & 0 & 0 & d_x \\
		0 & 1 & 0 & d_y \\
		0 & 0 & 1 & d_z \\
		0 & 0 & 0 & 1
	\end{bmatrix}
	\begin{bmatrix}
		x \\
		y \\
		z \\
		 1
	\end{bmatrix}
	=
	\begin{bmatrix}
		x + d_x \\
		y + d_y \\
		z + d_z \\
		1
	\end{bmatrix}
$$

By using the matrix representation for affine transformations, multiple transformations can be concatenated together.

---

## 2D Rotation

Consider rotation about the origin by $\theta$ degrees. The new points can the $sin$ or $cos$ of the sum of angles → use the sum of angles formula → get the new points.

>[!caution]
>Rotation in 2D space is actually a rotation in 3D space with $z$ pointing towards the observer.

![[rotation.png|500]]

Rotation about z-axis in three dimensions leaves all points with the same $z$. Therefore, it is equivalent to rotation in 2 dimensions in planes of constant $z$.

This can be represented in homogeneous coordinates, $\text{p’} = \text{R}_z (\theta)\text{p}$
$$
\text{R}_z(\theta) = 
	\begin{bmatrix}
		\cos \theta & - \sin \theta & 0 & 0 \\
		\sin \theta & \cos \theta & 0 & 0 \\
		0 & 0 & 1 & 0 \\
		0 & 0 & 0 & 1
	\end{bmatrix}
$$

$$
\text{R}_x(\theta) = 
	\begin{bmatrix}
		1 & 0 & 0 & 0 \\
		0 & \cos \theta & - \sin \theta & 0 \\
		0 & \sin \theta & \cos \theta & 0 \\
		0 & 0 & 0 & 1
	\end{bmatrix}
$$

$$
\text{R}_y(\theta) = 
	\begin{bmatrix}
		\cos \theta & 0 & \sin \theta & 0 \\
		0 & 1 & 0 & 0 \\
		- \sin \theta & 0 & \cos \theta & 0 \\
		0 & 0 & 0 & 1
	\end{bmatrix}
$$

---

## Scaling

Expand or contract along each axis, fixed point of origin
$$
\text{S} = \text{S}(s_x, s_y, s_z) = 
	\begin{bmatrix}
		s_x & 0 & 0 & 0 \\
		0 & s_y & 0 & 0 \\
		0 & 0 & s_z & 0 \\
		0 & 0 & 0 & 1
	\end{bmatrix}
$$

>[!caution] Reflection
>Reflection is derived from the negative scale factor.

---

## Inverses

Suppose we have a matrix of transformation. If we inverse the transformation matrix, then we obtain the inverse transformation. However, note that calculating the inverse of a matrix is expensive.

### Translation
$$\text{T}^{-1}(d_x, d_y, d_z) = \text{T}(-d_x, -d_y, -d_z)$$

### Rotation
Note that
$$
\text{R}^{-1}(\theta) = \text{R}(-\theta)
$$
By trigonometric properties, observe that,
$$
\text{R}^{-1}(\theta) = \text{R}^{T}(\theta)
$$
### Scaling
$$
\text{S} = \text{S}^{-1}(s_x, s_y, s_z) = \text{S}(\frac{1}{s_x}, \frac{1}{s_y}, \frac{1}{s_z})
$$

>[!caution] 
>$$
>(ABC)^{-1} = C^{-1} B^{-1} A^{-1}
>$$
---
# Concatenation

- Premultiply the transformation matrix
- Multiply with the point

Accumulating all the transformation is significantly less expensive than multiplying the transformation to every point.

Consequently, suppose $M = ABCD$ in which it is a transformation matrices, the transformation on the *right* is applied first

---

# Rotation about a fixed point other than the origin

1. Move the fixed point to origin
2. Rotate
3. Move fixed point back

>[!caution] General rotation
>Rotation about an arbitrary axis can be decomposed into the concatenation of rotations about the $x, y, z$ axes, with *Euler Angles*.

![[rotationaboutanyaxis.png| -m | -center]]

This motivates the need for ==instancing== where a simple object is centred at the origin for convenience.

---

# Transformations in OpenGL

>[!caution] Matrices as state
>Note than in OpenGL, matrices and matrix mode are part of the state.

There are 2 *important* matrix modes:
- `GL_MODELVIEW`
- `GL_PROJECTION`

In ==each== matrix mode, there is a 4 x 4 *current transformation matrix* that is part of the state and is applied to all vertices that pass down the pipeline.

The *CTM* is defined in the user program and loaded into transformation unit. To concatenate transformation, just ==post-multiply== the transformation to the matrix loaded in the CTM. Usually, to initialise the CTM, an *identity matrix* is loaded.

>[!caution] CTMs
>Note that the order of transformation in the CTM is backward of the actual desired order of transformation.

![[CTM.png| -m | -center]]

>[!caution]
>The last operation specified is the first operation applied to vertices.

---

## `GL_MODELVIEW`

The ==model-view== is used to *transform* objects into the world space and position the camera (view transformation).

The ==projection matrix== is used to define the *view volume*.

---

# Matrix stacks
OpenGL maintains stack for each matrix mode (as set by `glMatrixMode`)

Suppose we have the following `DrawSquare()` function:
```cpp
void DrawSquare() {
	glBegin( GL_POLYGON );
		glVertex3d( 1.0, 1.0, 0.0 );
	    glVertex3d( -1.0, 1.0, 0.0 );
	    glVertex3d( -1.0, -1.0, 0.0 );
	    glVertex3d( 1.0, -1.0, 0.0 );
	glEnd();
}
```

Then, when we want to `DrawSquare` to form a pattern centred at `(100,200)` : 

```cpp
glTranslated(100.0, 200.0, 0.0); // 4
for (int i = 0; i < 8; i++) {
	glPushMatrix();
		glRotated(i * 45.0, 0.0, 0.0, 1.0); // 3
		glTranslated(10.0, 0.0, 0.0); // 2
		glScaled(0.5, 0.5, 0.5); // 1
		DrawSquare();
	glPopMatrix();
}
```

1. Scale the square by factor $\frac{1}{2}$
2. Translate in the positive $x$-direction by $10.0$
3. Rotate by a factor of $45.0\degree$ on the $z$-axis
4. Translate the entire composite object by $(100.0, 200.0)$

---
