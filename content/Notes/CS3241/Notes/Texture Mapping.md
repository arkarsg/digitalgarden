>[!note] Texture mapping
>Texture mapping is a cheap way to add surface details to surfaces of 3D objects

- Does not increase geometric complexity
- Easily and efficiently implemented in polygon-based graphics hardware

---
# Surface Parameterization
>[!info] 
>Defines a mapping between 3D surfaces and 2D texture map. In other words, which point of the 3D object corresponds to which point in the 2D texture map
>

Defines the mapping $(x_w, y_w, z_w) \leftrightarrow (s, t)$ where $(x_w, y_w, z_w)$ is the 3D coordinates of surface point and $(s, t)$ is the 2D texture coordinates (limited to $[0, 1]^2$)

For polygon models, texture coordinates are specified **only** at the vertices.

There are *two parts* to texture mapping.

1. **S-mapping** : Texture map is first projected onto an “easy” *intermediate surface* (ie plane, cylinder, sphere, cube)
	- $T(s, t) \rightarrow T'(x_i, y_i, z_i)$
2. **O-mapping** : 3D intermediate surface is mapped onto the object surface
	- $T’(x_i, y_i, z_i) \rightarrow O(x_w, y_w, z_w)$

![texmap|300](Screenshot%202023-11-30%20at%206.50.29%20PM.png)

![[omappin.png]]

![[mappingexamples.png]]

---

## Texture filtering
At each fragment, the **interpolated texture coordinates** are then used to look-up texture map. The texture coordinates may not correspond to a *texel center*, bilinear interpolation of adjacent 4 texels may happen.

## Texture coordinates wrapping
At each fragment, the interpolated texture coordinates will be transformed into the range [0, 1] according to the wrapping mode:

**Clamp** : clamped to [0, 1]
**Repeat** : Ignored integer part of texture coordinates
![texcoordwrapping|500](Screenshot%202023-11-30%20at%206.52.30%20PM.png)

---

# Aliasing
>[!caution] Aliasing
>Aliasing can happen if texture map is *point-sampled* at each fragment

This occurs when there is *texture minification* where many texels are mapped to the area of the fragment.

## Anti-aliasing
>[!info]
>Texture map should be *area-sampled* at each fragment

A fragment is mapped to a quadrilateral area (called the *pre-image*) in the texture space

![[texture-antialiasing.png|80%]]

## Mipmapping
By approximating each *pre-image* using a square, we can create a set of **pre-filtered** texture maps and **point-sample** the appropriate pre-filter map for each fragment according to the degree of **texture minification**

A ==mipmap== is created by averaging down the original image successively by half the resolution.

![[texture-mipmapping.png|50%]]

### Selecting mipmap level
A **mipmap** level is chosen for texture lookup according to the amount of texture minification.

The ideal mipmap level be non-integer. This occurs when linear interpolation of texels retrieved from two consecutive mipmap levels may happen. Called **trilinear** texture map interpolation.

---

# Environment / reflection mapping

>[!info] 
>Environment / reflection mapping is a shortcut to rendering **shiny objects**

The image of the surrounding is first captured and stored in texture map. During rendering of the object, the *reflected eye ray* is used to reference the texture map.

![[texture-environment.png|80%]]

>[!caution]
>This is only geometrically correct when object is a point and/or the surrounding is infinitely far away

## Cube map
Image of the environment can be stored in a *cube map* and has 6 separate images, situated in the $+x, -x, +y, -y, +z, -z$ directions.

![[texture-enviromentmap.png|50%]]

## Bump mapping
Simulates small complex geometric features on surfaces without really the need to model them. A height field is used to perturb surface normals, and the perturbed normals are used in light reflection computation.

![bumpmapping|400](Screenshot%202023-11-30%20at%206.59.17%20PM.png)

A height field is used to *perturb* surface normals, and the **perturbed normals** are used in light reflection computation.

## Billboarding
Image based rendering where the static image of an object rotates with the view direction.

---

# 3D texture mapping


```start-multi-column
ID: ID_702b
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```
### 2D texture mapping
- Severe texture distortions on surfaces
- Non-trivial surface topology hard to parameterize

--- column-end ---

### 3D texture mapping
- 3D texture is defined everywhere in 3D space
- Texture value at each surface point is determined by its 3D position in space
- Analogous to sculpting or carving an object out of a block of material

--- end-multi-column

# Texture mapping in OpenGL

>[!note]
>Texture mapping occurs in the [[Rasterization#Fragment processing | Fragment processing]] stage of the rendering pipeline

Refer to the lecture notes for code reference


