#### Question 1
To be able to display realistic images, our display devices need to be able to produce every frequency in the visible light spectrum. True or False? Why? What are the advantages and disadvantages?

>[!caution] Non-answer
>False. Since the visible light is on a spectrum and there exists a continuous range of frequencies, colors must be represented in floating points to represent every color. This requires the use of larger number of bits for each RGB which results in the following:
> - Inaccuracies in transformations
> - Larger storage space needed
> >[!note]- Why?
> >The visible light spectrum is continuous, but this does not mean that colors must be represented in floating points. In fact, most display devices use a discrete color model, such as RGB, to represent colors. This is because discrete color models are more efficient and easier to implement.
> >
> >Using a discrete color model does not mean that colors cannot be represented accurately. With a sufficient number of bits per color, a discrete color model can represent any color in the visible light spectrum. However, the more bits per color, the larger the storage space needed.
> >
> >The statement also mentions that using floating points to represent colors can result in inaccuracies in transformations. This is true, but it is not a problem unique to floating points. Any color representation can be inaccurate if the transformations are not done correctly.
> >
> >Overall, the statement is not accurate. There are no inherent advantages to using floating points to represent colors in display devices. In fact, discrete color models are more efficient and easier to implement, and they can represent colors just as accurately as floating points.
> >
> >Here are some additional points to consider:
> >
> >- The human eye can only distinguish between a finite number of colors. This means that even if we could represent colors using floating points, there would be some colors that we would not be able to see.
> >  
> >  - The colors that we see are also affected by the surrounding environment. For example, the same color may look different under different lighting conditions.
> >    
> >  - The goal of a display device is to produce images that are visually appealing to humans. This means that it is not always necessary to represent colors accurately. In some cases, it may be more important to produce colors that are consistent with the user's expectations.



False. Most devices cannot produce every frequency of light. A display device uses the discrete [[Image formation#Color image | RGB model]]. There is no choice of 3 primary colors that can fully represent the perceivable colors. This can be shown with the [CIE color space](https://en.wikipedia.org/wiki/CIE_1931_color_space#%2Fmedia%2FFile%3ACIE1931xy_blank.svg). If we wish to display all colors, we will require 7 channels — ==ROYGBIV==.

Displays also cannot display full range of luminance as it is limited by the brightness and number of pixels.


```start-multi-column
ID: ID_suzm
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

Advantages
- more realistic images
- produce wider range of colors
- simulate lighting effects

--- column-end ---

Disadvantages
- more complex and expensive
- consume more power
- Humans cannot perceive slight differences

--- end-multi-column

---

#### Question 2

>[!aside | right +++++]
>Reference: https://en.wikipedia.org/wiki/8-bit_color

Each pixel in a frame-buffer has 8 bits for each of the R, G and B channels. How many different colors can each pixel represent? Is this enough? On some systems, each pixel has only 8 bits (for all R, G, and B combined). How would you allocate the bits to the R, G and B primaries?

>[!aside | right +++++]
>With 256 values of grey values, we can still observe the ==banding effect==, and therefore, it will not be smooth. However, the total number of colors is still enough for smooth effect.

For each color channel, there are $2^8 = 256$ values. Therefore, there are $256 * 256 * 256 = 16,777,216$ colors. This is enough as human eye can only resolve a maximum of 10 million colors as [[Image formation#Three-color theory | each cone]] can only resolve 100 shades.

Note that human eyes are [[Image formation#Three-color theory | less sensitive to blue light]]. Therefore, allocate `3, 3, 2`.

---

#### Question 3

![[tut01q3.jpeg| -m | -center]]

---

#### Question 4

Why do we need primitive assembly stage in rendering pipeline architecture?

In primitive assembly, [[Image formation#Primitive assembly | vertices are collected into geometric objects]] to form line segments, polygons or curves and surfaces.

This is necessary as vertices are processed independently. Primitive assembly is also necessary future stages such as rasterization and clipping.

Once the program knows the shape formed by the vertices, renderer can perform rasterization and clipping correctly.

---

#### Question 5

What does the rasterization stage (rasterizer) do in the rendering pipeline architecture? Describe what it does to a triangle that is supposed to be filled, and the three vertices have different color. Assume smooth shading is turned on.

If an object is not clipped out, then the appropriate pixels in the buffer frame are activated and assigned colors. The rasterizer produces a set of fragments for each object.

When three vertices have different colors, pixels within the triangle will be assigned colors based on the addition of colors between each vertices and a point on the primitive.

>[!note] Addition of color
>The addition of color depends on the algorithm used and there exists different algorithms to interpolate the colors. Choice of algorithm depends on the complexity of the scene, desired level of realism and performance requirements.

---

#### Question 6

What is hidden-surface removal? When is it not necessary?

[[Image formation#Fragment Processing | Hidden surface removal]] falls under the fragment processing stage of the rendering pipeline. With hidden surface removal, fragments which are blocked or occluded by other fragments are removed using the `z-buffer` algorithm.

Hidden surface removal is not necessary when the camera is positioned in such a way that no fragments are blocked or fragments are sufficiently isolated, or the scene is rendered using a wireframe or point cloud representation.

Painter’s algorithm — Paint the scene with the largest depth first.

---

#### Question 7

Differences between the 2 programs:


```start-multi-column
ID: ID_aitr
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

A

Creating a primitive in each iteration

--- column-end ---

B

Creating a primitive that consists of 3 x 3 x N points  


--- end-multi-column

B is more efficient as the vertices can be processed and rendered in a single pipeline. Whereas in A, vertices undergo the rendering pipeline for every instance of triangle created. Thus, B incurs less overhead.

>[!caution] Why can’t we do the same for polygons?
>OpenGL cannot collect the vertices properly to create polygons.

---

#### Question 8

Why does OpenGL support `GL_TRIANGLE_FAN` and `GL_TRIANGLE_STRIP`?

They are simple, convex and flat.

If we only use `GL_TRIANGLE`, we need to specify more vertices. With `GL_TRIANGLE_FAN`, we only need to specify the outer vertices and the inner vertex. 

>[!note]
>Use OpenGL docs for the exact formula

---

#### Question 9

Devise a test to check whether a polygon in 3D space is planar.

1. Construct a normal vector with a point within the triangle.
2. Check all vertices that the dot product == 0

>[!note]
>We are checking that all the normals are parallel to each other.

---

#### Question 10

Devise a test to check whether a polygon on the x-y plane is convex

Given an ordered set of points of the polygon in a clockwise or anti-clockwise direction, check that the cross product all the points are in the same direction. That is, the product of the cross products of 2 different set of edges > 0.



---


