>[!note]
>So far we have been using polygons to approximate curved surfaces

# Applications of curves and surfaces
- Drawing *vector-based* smooth curves (defined by mathematical equations)
- Font design, representation and rendering
- Smooth animation paths (for objects, light, camera)
- Designing smooth functions – image color and tone adjustment
- 3D model design, representation and rendering
- Data fitting

## Advantages
1. More *compact representation* than a set of straight line segments or a set of polygons
	- Adaptively produce polygons or line segments. For example, if it is very far away, we can use less polygons and if it is very near, we can use more polygons
2. Provide *scalable* geometric primitives
3. Provide *smoother* and more continuous primitives than straight lines and planar polygons
4. *Animation* and *collision detection* may become ==simpler== and ==faster== – easier to check for collision with other objects when it is with mathematical formulas. If it is a set of polygons, it is harder to find the intersection.
	- Example: finding intersection between ray and sphere
	- Sphere is represented using implicit form.
	- If it is represented as a set of polygons, it is inefficient

---
# Design Criteria
1. Local control of the shape
	- Editing one part of the curve should not greatly affect other parts of the curve
2. Smoothness and continuity
3. Ability to evaluate derivatives — can compute a normal/ tangent vector at any point to derive speed
4. Stability — when one parameter change, the shape of the curve *should not* change a lot
5. Ease of rendering

---
# Forms of representation
>[!note] Goal
>We want to find a form that allows us to find the derivate quickly
## Explicit form

### Curves in 2D
>[!example]
>The value of the *dependent variable* is given in terms of the *independent variable*.
>> $$y = f(x)$$

Some surfaces cannot be represented, such as a vertical straight line.

### Curves in 3D
>[!example]
>Requires two *independent variables*
>$$
>y = f(x)
>$$
>$$
>z = g(x)
>$$

### Surfaces in 3D
>[!example]
>Requires two *independent variables*
>$$
>z = f(x, y)
>$$

Some surfaces cannot be expressed in explicit form, such as a sphere

---
## Implicit form
### Curves in 2D
$$f(x,y) = 0$$
Now, you can represent vertical lines where a straight line will be $ax + by + c = 0$

### Curves in 3D
Represented as the intersection of two surfaces:
$$ f(x, y, z) = 0$$
$$ g(x, y, z) = 0$$
>[!caution] Drawbacks of implicit form
>- Difficult to obtain points on the curves and surfaces because the equations are just a *membership* test.
>- Difficult to render using rasterization approach, but easier to render using ray tracing

### Surfaces in 3D
$$
f(x, y, z) = 0
$$
- $ax + by + cz + d = 0$ (plane)
- $x^2 + y^2 + z^2 - r^2 = 0$ (sphere)

---
## Parametric form
### Curves in 2D and 3D
Each spatial variable for points on the curve is expressed in terms of an independent variable $u$, the parameter.

For curves in 2D
$$
p(u) = \begin{bmatrix}
x(u) \\
y(u)
\end{bmatrix}
$$

For the case of curves in 3D space,

$$
p(u) = \begin{bmatrix}
x(u) \\
y(u) \\
z(u)
\end{bmatrix}
$$

Then, we can also find the *tangent vector* (velocity) at a point by finding the derivative:

$$
\dfrac{dp(u)}{du} = \begin{bmatrix}
\dfrac{dx(u)}{du} \\
\dfrac{dy(u)}{du} \\
\dfrac{dz(u)}{du}
\end{bmatrix}
$$


### Surfaces in 3D
Now requires 2 parameters which forms a rectangular domain
$$
p(u, v) = \begin{bmatrix}
x(u, v) \\
y(u, v) \\
z(u, v)
\end{bmatrix}
$$
To find the normal vector at a point on the curve, find the cross product of the derivative

![[curvesandsurfaces-parametricform.png|300]]

### Parametric polynomial curves
- Parametric forms are not unique. Given a curve or surface, it can be represented in many ways
- Parametric forms where functions *polynomials in $u$ (and $v$)* are most used in computer graphics — they also possess the [[Curves and Surfaces#Design Criteria]]
- Stability is only achieved for polynomials of lower degree in this case

A parametric polynomial curve of degree $n$ (or order $n + 1$) is of the form:
![[curvesandsurfaces-parametricpolynomial.png|400]]
Note that the each parametric function is polynomial in $u$ $\implies$ we need $n+1$ for each degree.

>[!example]
>We need $n(n + 1)$ coefficients
>For a curve degree 3, we need $3(3 + 1) = 12$ values of $c$. 

Then, we need to limit the range of $u$ as otherwise, we will be creating an infinite segment.
$$ u_{min} \leq u \leq u_{max}$$
By convention, we assume,
$$ 0 \leq u \leq 1 $$
### Parametric polynomial surfaces
A parametric polynomial surface is of the form
![[curvesandsurfaces-parametricpolynomialsummation.png|200]]
which needs $3(n + 1)(m + 1)$ coefficients in { $c_{ij}$ } and $n = m = 3$. Therefore, we need 48 coefficients
- Restrict the range $0 \leq u, v \leq 1$ to define a *surface patch*

>[!caution] 
>We use degree 3 most commonly for stability — cubic parametric polynomial curve segments

## Parametric Cubic Polynomial Curves

To create a *long* curve, we join multiple segments of lower degree. This gives greater local control of shape and stability of the curve.

>[!example]
>If it is of degree 2 (quadratic polynomial), we can only bend at one point

$$
p(u) = c_0 + c_1u + c_2u^2 + c_3u^3 = \sum_{k = 0}^3 u^k c_k
$$
where $c_k = \begin{bmatrix} c_{xk} & c_{yk} & c_{zk}\end{bmatrix}^T$.

---
Rewrite as
$$
p(u) = c_0 + c_1u + c_2u^2 + c_3u^3 = \sum_{k = 0}^3 u^k c_k = u^T c
$$
where $c = \begin{bmatrix} c_0 & c_1 & c_2 & c_3\end{bmatrix}^T$ and $u = \begin{bmatrix} 1 & u & u^2 & u^3 \end{bmatrix}^T$

---

### Specifying curve segments
Normally, we do not provide values of 12 coefficients of $p(u)$.

Instead, provide geometric data that can be used to derive the values of the coefficients of $p(u)$. This data consists of a small number of control points or data points
![[curvesandsurfaces-controlpoints.png|500]]
#### Cubic interpolation curves
Given control points $p$, the curve must pass through all the points in $p$, such that

$$
\begin{align}
p(0) = p_0 \\
p(1) = p_3
\end{align}
$$

![[curvesandsurfaces-pathpoints.png|200]]

### Deriving cubic interpolating curves
>[!info] Goal
>Seek coefficients $c$ such that the polynomial passes through the control points

1. Assume the curve segment interpolates $p_0, p_1, p_2, p_3$ at equally-spaced values
$$
u = 0, ⅓, ⅔, 1
$$

![[bezier-cubicinterpolation.png|50%]]

With the 12 equations, solve for the coefficients.

#### Solving the equations
Let
$$
p = \begin{bmatrix}
p_0 \\
p_1 \\
p_2 \\
p_3 \\
\end{bmatrix},
\enspace
A = \begin{bmatrix}
1 && 0 && 0 && 0 \\
1 && \frac{1}{3} && \frac{1}{3}^2 && \frac{1}{3}^3 \\
1 &&  \frac{2}{3} && \frac{2}{3}^2 && \frac{2}{3}^3 \\
1 && 1 && 1 && 1 \\
\end{bmatrix}
$$

Solve
$$
p = Ac
$$

==Interpolation geometry matrix== is the inverse of A.

$$
M_I = A^{-1} = \begin{bmatrix}
1 && 0 && 0 && 0 \\
-5.5 && 9 && -4.5 && 1 \\
9 &&  -22.5 && 18 && -4.5 \\
-4.5 && 13.5 && -13.5 && 4.5 \\
\end{bmatrix}
$$

$M_I$ is the same for any 4 control points.

Then, ==$c = M_I p$==


### Blending functions
Essentially a weighted sum of the control points and the *weights* are given by the ==blending function==.

Since $c$ can be computed from the control points and the interpolation geometry matrix, we can rewrite as:
$$
p(u) = u^T c = u^T M_I p
$$
Let $b(u)$ be a column matrix of 4 *blending polynomials*, where each is a cubic.
>[!caution]
>Refer to lecture notes
![[[bezier-blendingfunction.png|80%]]

With the blending function, we can transform $p(u)$ into a weighted sum of the control points:
$$
\sum b_i(u)p_i
$$

## Cubic interpolation patch
*Bicubic* surface patch (bicubic as it is a polynomial in $u$ and $v$)
$$
p(u, v) = \sum_i \sum_j u^i v^j c_{ij}
$$

Similar to curves, we need to specify *16 control points* and the patch needs to pass though *all* the points. The 16 points will be used to calculate all the 48 points.

### Blending patches

Surface is formed by blending together 16 simple patches, each weighted by a control point

---

# Geometric and parametric continuity
>[!note] Goal
>We want to maintain the smoothness,
>and we wish to describe the smoothness at the joints.

Consider two curve segments $p(u)$ and $q(u)$

- $p(1) = q(0) \implies C^0$ parametric continuity at the join point
	- The two ends lie at the same point. However, it can be the case that there is a sharp joint.
- $p'(1) = q'(0) \implies C^1$ parametric continuity at the join point
	- This implies that the 2 curves have the same segment at the points and therefore, will be a smooth join.
	- The first derivative of *end point* is the same as the first derivative of another *start point*
- $p'(1) = \alpha q'(0) \implies G^1$ parametric continuity at the join point
	- Relaxed condition of $C^1$

The idea can be applied for derivates of higher order. However, at most $2$ is necessary for cubic parametric curves.

---

# Cubic Bézier curves
Given control points, $p_0, p_1, p_2, p_3$, we want
![[curvesandsurfaces-beziercurveswithequation.png| -center]]

Then, we have the following:

$$
c = M_B p \enspace \text{where} \enspace
p = \begin{bmatrix}
p_0 \\
p_1 \\
p_2 \\
p_3
\end{bmatrix}
$$

$M_B$ is the Bezier geometry matrix:
$$
M_B= \begin{bmatrix}
1 && 0 && 0 && 0 \\
-3 && 3 && 0 && 0 \\
3 &&  -6 && 3 && 0 \\
-1 && 3 && -3 && 1 \\
\end{bmatrix}
$$

## Blending functions

Rewrite $p(u)$ as $u^T M_B p$ and we have the blending function $b(u)$

These are known as *Bernstein polynomial* of degree 3 which have the following property
- $0 < b(u) < 1$
- $\sum b_i (u) = 1$

$p(u)$ expressed as a weighted sum is a *convex sum*.

![[curves-convexsum.png|400]]

Consequently, $p(u)$ must lie in the *convex hull* of the four control points

![[curves-convexhull.png|200]]

---

# Bicubic Bézier Surface Patch


---

# Rendering curves and surfaces

>[!note] 
>All the curves that can be generated using the [[Curves and Surfaces#Cubic interpolation curves]] method can also be generated using the [[Curves and Surfaces#Cubic Bézier curves]] method, and vice versa.

Given the representation of the curve segment, how to draw the curve?

- Evaluate $p(u)$ at a sequence of $u$ values and join the points using straight line segments (polyline)

![[Screenshot 2023-11-18 at 6.12.44 PM.png|300]]

>[!caution]
>Note that in areas with high curvature, it is not represented accurately, such as $u_2, u_3$. Therefore, we need an adaptive way of choosing the values of $u$.

## Rendering Bézier curves

### De Casteljau’s algorithm
$p(u)$ is computed by a sequence of recursive linear interpolations between successive control points.

Suppose we have the 4 control points
![[Screenshot 2023-11-18 at 6.15.45 PM.png|300]]
1. Linearly interpolate $u$ between $p_i$ and $p_{i+1}$
![[Screenshot 2023-11-18 at 6.16.48 PM.png|300]]
2. Recursively interpolate between the points until there is only 1 set of interpolation
![[Screenshot 2023-11-18 at 6.18.18 PM.png|300]]

Then, we can obtain $p(u)$ in an adaptive manner

### Subdivisions of Bézier curves
- We can recursively subdivide a curve segment into two shorter Bezier curve segments
Observe that the each interpolating points become the new control points
![[Screenshot 2023-11-18 at 6.22.02 PM.png|300]]
- Now there is a *left* curve segment and *right* curve segment
- Check if the *convex hull* of the *left* and *right* is flat enough
	- If it is flat, draw as a straight line
	- If it is not flat enough, subdivide with De Casteljau’s algorithm
![[Screenshot 2023-11-18 at 6.26.04 PM.png|300]]

---

## Rendering other polynomial curves
Other polynomial curve segments can be converted to Bézier curve segments and rendered using the recursive subdivision approach.

---

## Bézier patches
The Bezier curve subdivision can be extended to Bézier patches
- *Convex hull* defined by the control points of the subdivision patch to determine its *flatness*
- If it is, draw
