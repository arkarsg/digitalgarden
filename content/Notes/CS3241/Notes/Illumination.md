
# Local reflection vs Global illumination

## Local reflection

- Considers relationships between a *light source*, a *single surface point*, and a *view point*
- No interaction with other objects

## Global illumination
- Considers all light sources and surfaces
- *Inter-reflections* and *shadows*

![[illumination-globalvslocal.png|500]]

---

# Illumination model

## Phong illumination equation (PIE)
>[!note] Phong illumination equation
>Given a *surface point*, *light source* and a *viewer*, compute *color* at surface

==Phong Model== is a [[Illumination#Local reflection | local point reflection model]] that compromises both acceptable image quality and processing speed

![[illumination-phong.png|500]]

There are **3** terms in the Phong illumination equation: *ambient*, *diffuse* and *specular*

![PIE|500](Screenshot%202023-11-30%20at%204.52.54%20PM.png)

### Ambient light
>[!info] Ambient light
>Ambient light is *universal*. Every surface receives the same color and intensity of light.

Ambient light is used to produce a *uniform lighting* effect on every point on **every surface** in the scene. 

Its luminance $I_a$ is specified by
$$
I_a = \begin{bmatrix}
I_{ar} \\
I_{ag} \\
I_{ab}
\end{bmatrix}
$$
which is a *universal* value (same color and intensity of light for every surface)

To make different surfaces appear as different colors, specify *ambient material property* for **each surface**.

$$
k_a = \begin{bmatrix}
k_{ar} \\
k_{ag} \\
k_{ab} 
\end{bmatrix}
$$
Then, with the PIE, the ambient color of the surface is:
$$
I_a k_a = \begin{bmatrix}
I_{ar} \enspace k_{ar} \\
I_{ag} \enspace k_{ag} \\
I_{ab} \enspace k_{ab} \\
\end{bmatrix}
$$
>[!note] 
>This creates the ambient color for only 1 surface. Ambient light must be calculated for every surface.

![[illumination-ambient.png|500]]

---

### Diffuse
>[!info] The diffuse term
>The diffuse term gives color to the surface point according to the *light position* and the *surface normal*

>[!note] Surface normal
> **==triangle==** 
> - Triangle with vertices $A$, $B$, $C$ spans a plane
> - Normal vector is given by $N = (B - A) \times (C - A)$
>  
> **==Curved surface==**
> - For every surface *point*, there is a plane parallel to it

>[!note] Lambert’s Cosine Law
>Diffuse reflection $\propto \cos \theta = N \cdot L$
>![lambertslaw|300](Screenshot%202023-11-30%20at%205.01.46%20PM.png)

The diffuse term of the PIE is given by
$$
f_{att} \enspace I_p \enspace k_d \enspace (N \cdot L)
$$
![[illumination-normal.png|200]]

- $L$ is the *unit vector* from the surface point **to** the light source.

- $k_d$ is the diffuse material property $\begin{bmatrix}k_{dr} & k _{dg} & k_{db} \end{bmatrix}^T$ for the surface. This can be different from [[Illumination#Ambient light | k_a]].

>[!caution] 
>Normalize every directional vector ($L$ and $N$)
---
#### Point light source and attenuation
Assume that the light is a point at position $p$ and is emitting light at every direction.
Its color and intensity is specified by vector $I_p$
- However, the light received will be weaker if the object is farther away from the light

>[!note]
>Suppose the distance between light’s position, $p$, and the object is $d$
>$$
>f_{att}I_p = \frac{1}{a + bd + cd^2} I_p
>$$
>where $a, b, c$ are user defined constants. 

![[illumination-diffused.png|500]]

---

### Specular
>[!info] The specular term
>The specular term adds *highlights* to **shiny** surface

Assume light source is a point $\implies$ ==shininess== is *inversely proportional* to the size of the highlight *(ie, more shiny, smaller highlight)*

Highlight is **view dependent**. The highlight on the object will *move on the object* when the viewer moves

Define 4 **unit** vectors
1. $N$ — surface normal
2. $L$ — *unit vector* from the surface point **to** the light source
3. $R$ — reflection vector
4. $V$ — *unit vector* from the surface point **to** the viewer

We obtain the reflection vector $R$, with $N$ and $L$
$$
R = 2 (N \cdot L)N - L
$$

The angle between the vector to the viewer and reflection vector,
$$
\alpha = \cos^{-1} (R \cdot V)
$$


Define $n$ as the *shininess coefficient*
- as $n$ increases, highlights become smaller and sharper

![[illumination-specular.png|500]]

---

## Material properties

Material properties of a surface are modelled by *ambient*, *diffuse*, *specular reflection* coefficients $k_a, k_d, k_s$

- Vector of $3$ colors, $[ 0, 1 ]$.
- Shininess coefficient $n$, $[ 1, 128 ]$.

![[illumination-nk.png| -m | -center]]

---

![[illumination-multiplephong.png| -m | -center]]

---

# OpenGL
>[!note]- Rendering pipeline
>![[Rasterization#OpenGL rendering pipeline]]

- Lighting computation occurs in [[Rasterization#Vertex processing | vertex processing]].
- Lighting computation is performed in *eye space*

The `normal vector` is part of the state and is usually set just before specifying each vertex
```cpp
glNormal3f(x, y, z);
glNormal3fv(p);
```

- Normal vectors need to be *normalized* as length can be affected by transformations

The following allows auto-normalization at a performance penalty.
```cpp
glEnable(GL_NORMALIZE)
```

## Lighting Computation
```cpp
// enable lighting computation
glEnalbe(GL_LIGHTING) // once enabled, glColor() is ignored

// enable each light source individually
glEnable(GL_LIGHTi) i = 0, 1, 2, ...

// Do not use simplifying distant viewer assumption in calculation
glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

// Shade both sides of polygons independently
glLightModeli(GL_LIGHT_MODEL_TWO_SIDED, GL_TRUE)
```

## Defining a point light source
For each light source, set `RGBA` for the *diffuse, specular* and *ambient* components and for the position

```cpp
// set the diffuse, specular, ambient components
GLfloat diffuse0[] = { 1.0, 0.0, 0.0, 1.0 };
GLflaot ambient0[] = { 1.0, 0.0, 0.0, 1.0 };
GLfloat specular0[] = { 1.0, 0.0, 0.0, 1.0 };

// set the position
GLfloat light0_pos[] = { 1.0, 2.0, 3.0, 1.0 };

// enable lighting computations
glEnable(GL_LIGHTING)
// turn on the light
glEnable(GL_LIGHT0)
// set the components and position
glLightfv(GL_LIGHT0, GL_POSITION, light0_pos);
glLightfv(GL_LIGHT0, GL_AMBIENT, ambient0);
glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse0);
glLightfv(GL_LIGHT0, GL_SPECULAR, specular0);

// global ambient term for testing
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient);
```

## Moving light sources
>[!note]
>Light sources are geometric objects whose positions or directions are affected by the  **model-view matrix**

We can
- Move light sources with the objects
- Fix the objects and move the light sources
- Fix the light sources and move the objects
- Move light sources and objects independently

## Material properties
Material properties are also part of the OpenGL state and match the terms in the Phong model
```cpp
GLfloat ambient[] = {0.2, 0.2, 0.2, 1.0};
GLfloat diffuse[] = {1.0, 0.8, 0.0, 1.0};
GLfloat specular[] = {1.0, 1.0, 1.0, 1.0};
GLfloat shine = 100.0 // shine is the specular exponent

glMaterialfv(GL_FRONT, GL_AMBIENT, ambient);
glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse);
glMaterialfv(GL_FRONT, GL_SPECULAR, specular);
glMaterialfv(GL_FRONT, GL_SHININESS, shine);
```

### Front and back faces
- By default, it only shade front faces
- Two sided lighting → shades both sides of a surface

Each side can have its own properties which are set in `glMaterialfv`
```cpp
GL_FRONT,
GL_BACK,
GL_FRONT_AND_BACK
```

## Emissive term
We can simulate a light source in OpenGL by giving a material an *emissive component*

This component is *unaffected* by any sources or transformations

```cpp
GLfloat emission[] = { 0.0, 0.3, 0.3, 1.0 };
glMaterialfv(GL_FRONT, GL_EMISSION, emission);
```

## Multiple light sources

![[illumination-openglphong.png|500]]

---
# Shading
There are 3 types of shading
1. Flat shading
2. Gouraud shading
3. Phong shading ***(different from Phong Illumination)***

## Flat shading
>[!note] Flat shading
>For each polygon, we color *whole polygon* with **one** color only

Pick *any* point on each polygon (a corner) and compute its color using [[Illumination#Phong illumination equation (PIE) | PIE]] using surface normal at that point.

Then, color the entire polygon.

This causes distinctive color difference between neighbouring polygons

```cpp
glShadeModel(GL_FLAT);
```

![flatShading|200](Screenshot%202023-11-30%20at%205.20.57%20PM.png)

---

## Gouraud shading
>[!note] 
>Gouraud shading uses *per-vertex* lighting computation


For each *vertex*, compute the ==average normal vector== of the polygons that share the vertex $\implies$ need to know connectivity.

Then, use PIE at the vertex using the average normal vector. As a result, each vertex has a different normal and position $\implies$ different color by PIE.

Then, smoothly interpolate the computed colors at the vertices to the interior of the polygon during [[Rasterization#Rasterization]].

![[illumination-gouraudnormals.png| -center | -xs]]

```cpp
glShadeModel(GL_SMOOTH);
```

---

## Phong shading
>[!note] 
>Phong shading uses *per-pixel* lighting computation

Same as *Gouraud shading* where every vertex of a polygon has a different vertex normal vector.

**Phong shading** → No computation of colors of the vertices for interpolation

Instead, for each **FRAGMENT**, interpolate the *normal vectors* from the vertices.

Apply PIE at each fragment on the interpolated normal vector to compute a color for the **FRAGMENT**

---

## Gouraud vs Phong

![[illumination-phongvsgouraud.png|500]]
![gouradvsphong|500](Screenshot%202023-11-30%20at%205.28.07%20PM.png)
a. Gourad
b. Phong


### Gouraud
- Produces *only* linear interpolation of colors
- May miss the highlight
- Supported in OpenGL

### Phong
- Highlights are produced more faithfully
- Not supported in OpenGL
- Can be done by reprogramming the rendering pipeline using shaders

