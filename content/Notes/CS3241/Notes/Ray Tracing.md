# Ray casting
```plain-text
For every pixel
	Construct a ray from the eye
	For every object in the scene
		Find intersection with the ray
		Keep if closest (achieves hidden surface removal)
	Shade depending on light and normal vector (use Phong reflection model)
```

```start-multi-column
ID: ID_g64e
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```
### Rasterization

Given a primitive in 3D space, determine which pixels are covered by the primitive
Outer loop : looping through each primitive
Inner loop : looping through each pixel

--- column-end ---

### Ray casting
At each pixel, determine which primitive covers it
Outer loop: set of all pixels
Inner loop: Looping through each primitive

--- end-multi-column

# Ray tracing
From the closest intersection point, *secondary* rays are produced (in addition to lighting computation):
1. **Reflection ray** 
	1. Are there any objects intersecting with reflection ray? The object’s color is propagated back to the original object
	2. The reflection ray can be spawned recursively
2. **Refraction ray**
	1. For a transparent object, there is *refraction*.
	2. Goes into the object and *refracted* upon entry AND upon exit.
	3. At the intersection point with another object, it calculates the color and propagated back to the original object
3. **Shadow ray**
	1. Shoot a ray towards the light source
	2. If the ray is not intersected, the surface point is not in shadow
	3. Else, the surface point is in shadow

The ray from the eye is considered a *primary ray*.

---
# Whitted Ray Tracing
With Whitted ray tracing, we can achieve:
1. Hidden surface removal (from ray casting)
2. Reflection of light
3. Reflection / refraction of other objects
4. Shadows

**No ad-hoc add-on** : For example, with rasterization, need to do reflection mapping [[Texture Mapping]], or, creating shadows with shadow mapping — no need with ray tracing.

This is also known as *recursive ray tracing* as a primary ray produces $n$ secondary rays and each secondary rays further produces $n$ secondary rays. However, it simulates only *partial global illumination*.

---

![[raytracing-formula.png| -center | -m]]
![[raytracing-rays.png| -m | -center]]

>[!note]
>In the refracted view, imagine you are at the bottom of the swimming pool and looking at the sun. The dot product is the intensity of the light

## Computing reflection / refraction rays
![[raytracing-rays 1.png| -center | -m]]
>[!note] Refraction
>Need to know the refractive index based on Snell’s Law

## Ray tree
>[!caution] 
>Shadow ray is not considered in the branching factor as it is not recursively spawned

![[raytracing-raytree.png| -m | -center]]

## Shadow rays
At each surface intersection point, a shadow ray is shot towards each light source to determine any occlusion between light source and surface point.

- Need to find only one opaque occluder to determine the occlusion
![[raytracing-illumination.png| -m | -center]]

$k_{\text{shadow}}$ : 0 if it is in shadow, 1 if it is not in shadow

### Translucent occluder
- Light is attenuated (weakened) by the $k_tg$ (RGB) triplets of the occluder
- Refraction from light ray from light source is ignored (shadow ray refracted through the object may not end up at object → ignore)

Both are physically inaccurate but it is done this way because it is difficult to calculate such a shadow ray.

---
# Scene description
- Camera view and image resolution – camera position and orientation in world coordinate frame, similar to `gluLookAt()`
- Field of view — similar to `gluPerspective()` , but no need for `far` and `near` plane
- Image resolution — Number of pixels in each dimension

Each *point light source* has:
- Position
- Brightness and color ($I_{\text{source}}$)
- Global ambient ($I_{\text{a}}$)
- Spotlight, possible provide the cone

Each *object surface material*:
- $k_{rg}, k_{tg}, k_a, k_d, k_r, k_t$ where each is a RGB vector
- $n$, $m$
- Refractive index $\mu$ if $k_{tg} \neq 0$ or $k_t \neq 0$
	- Can use different refractive index for RGB

Each *objects*:
- Implicit representations (ie plane, sphere, quadratics)
- Polygon
- Parametric (bicubic Bezier patches)
- Volumetric representation
---
# Recursive ray tracing

>[!note]
>Different levels of recursion creates different results

Suppose light source hits an object at $P$
- $P_t$ (refracted ray) is produced
- $P_r$ (reflected ray) is produced
$$
I(P) = I_{\text{local}}(P) + I_{\text{global}}(P) = I_{\text{local}}(P) + k_{rg} I(P_r) + k_{tg} I(P_t)
$$

where $k_{rg}$ is the *global reflection coefficient* and $k_{tg}$ is the *global transmitted coefficient*.

>[!note]
>In other words, it is recursively calculating the illumination at each intersection based on the reflected ray and the refracted ray spawned form the object, as if the rays are the primary rays.

## Stopping recursion
- When the surface is totally diffuse (and opaque)
- When reflected/ refracted ray hits nothing
- When maximum recursion depth is reached
- When the contribution of the reflected/ refracted ray to the color at the top level is too small — set a threshold

---

# Ray-object intersection

>[!caution]
>Refer to the lecture slides for full reference

Finding ray-object intersection and computing surface normal is central to ray tracing.

## Representing rays
- Two 3D vectors
	- Ray origin position
	- Ray direction vector
- Parametric form
	- $P(t) = \text{origin} + t \times \text{direction}$
	- Looking at a point on the ray

The parametric form allows us to calculate the intersection easily, even if the object is not represented in the parametric form.

### Ray-plane intersection
Let the plane be $Ax + By + Cz + D = 0 \implies N \cdot P + D = 0$

To find ray-plane intersection, substitute ray equation $P(t)$ into plane equation
- We get $N \cdot P(t) + D = 0$
- Solve for $t$ to get $t_0$

If $t_0$ is infinity, no intersection (ray is parallel to plane). Intersection point is $P(t_0)$ and should be non-negative.

The normal at the intersection is $N$

### Ray-sphere intersection
Sphere (centered at origin) is often represented in implicit form.

$$
x^2 + y^2 + z^2 - r^2 = 0 \implies P \cdot P - r^2 = 0
$$



