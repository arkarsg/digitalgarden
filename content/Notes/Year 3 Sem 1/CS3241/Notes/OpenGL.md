# Basics
>[!caution]
>OpenGL is platform independent for use across all platforms. For example, windowing and key inputs are dependent on the OS. For these functionalities, third-party libraries are used.

==OpenGL Utility Toolkit (GLUT)== is not a part of OpenGL. However, this provides functionality common to all window systems, such as opening a window, get input from mouse and keyboard, menus and event-driven functionalities.

## Software organisation

![[openglarchitecture.png|80%]]

>[!info]- Rendering pipeline
>![[Image formation#Rendering pipeline]]

![[pipeline.png|80%]]

>[!aside | right +++++]
>In perspective and clipping, we have the coordinates in the window space. With that information, we can color that pixel in the *rasterisation* stage.

>[!aside | right +++++]
>Rasterization is also known as scan conversion as the process is done row by row.

>[!note] Vertex processing
>In the vertex processing stage, vertices are processed independently, and must be processed regardless of its visibility.
>
>Vertices are processed independently so that they can be processed in parallel.

>[!note] Fragment processing
>Fragment processing processes the polygon (fragment) such as texture mapping. Fragments are also processed independently.

## OpenGL functions
- Specify primitives — points, line segments, triangles, quadrilaterals, polygons
- Specify vertex attributes — colour, normal vector, material, texture co-ordinates
- Specify transformation — modelling and viewing
- Control
- Input
- Query

>[!note]
>OpenGL is a state machine.

Note that there are *2* types of OpenGL functions:


```start-multi-column
ID: ID_g7vg
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Primitive generating

- Functions can cause output if primitive is visible
- How vertices are processed and appearance of primitive are controlled by state

--- column-end ---

### State changing

- Transformation function
- Attribute function


--- end-multi-column

---

## Example program

``` cpp
#include <GL/glut.h 

// draws a simple square

// the display callback function
void mydisplay() {
	// clear the frame buffer
	glClear(GL_COLOR_BUFFER_BIT);
	glBegin(GL_POLYGON);
		glVertex2f(-0.5, -0.5);
		glVertex2f(-0.5, 0.5);
		glVertex2f(0.5, 0.5);
		glVertex2f(0.5, -0.5);
	glEnd();
	glFlush();
}

int main(int argc, char** argv) {
	glutInit(&argc, argv);
	glutCreateWindow("simple");
	glutDisplayFunc(mydisplay);
	glutMainLoop();
}
```

## Event loop

In the example above, `mydisplay` is a ==display callback function==. A display callback is executed whenever OpenGL *decides the display must be refreshed*.

>[!caution]
>Every GLUT program must have a display callback

The `main` function ends with the program entering an ==event loop==.

---

# Program Structure

*Most* OpenGL programs have a similar structure that consists of the following functions:


```start-multi-column
ID: ID_tcb8
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

>[!note] `main()`
>Defines the [[Input and interaction#Callbacks | callbacks]], and opens one or more windows with the required properties. `main` enters an event loop which is the last executable statement.


--- column-end ---

>[!note] `init()`
>`init()` sets the state variables for viewing and attributes.


--- end-multi-column

>[!note] `callbacks`
>`callbacks` display callback function and input and window functions

---

```cpp
#include <GL/glut.h>

int main(int argc, char** argv) {
	glutInit(&argc, argv);

	// requests properties for the window (the rendering context)
	// RGB color, single buffering, properties logically OR'ed together
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

	// define window properties
	glutInitWindowSize(500, 500);
	glutInitWindowPosition(0, 0);

	// create window with title simple
	glutCreateWindow("simple2");

	// set display callback
	glutDisplayFunc(mydisplay);

	// set OpenGL state
	init();

	// enter infinite event loop
	glutMainLoop();
}
```

```cpp
void init() {
	// clear color -- RGB, Alpha (transparency)
	glClearColor(0.0, 0.0, 0.0, 1.0);

	// set color to white
	glColor3f(1.0, 1.0, 1.0);

	// set viewing volume
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	// set viewing volume/ camera
	glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);
}
```

# Coordinates

The units in `glVertex` are determined by the application and are called *object coordinates*.

The **camera** is positioned in the *world coordinates*.

Internally, OpenGL convert vertices to *camera coordinates* and later to *window coordinates*.


## OpenGL camera

>[!note] Default camera
>By default, OpenGL places a camera at the origin in world space, looking in the *negative z-direction*.
>
>The ==default viewing volume== is a box centred at the origin with a side of length *2*.

![[viewvolume.png|80%]]

### Orthographic viewing
>[!note] Default orthographic view
>In the default orthographic view, points are *projected forward along the z-axis* onto the plane $z = 0$.

>[!caution] The direction of z-axis
>Note that $z-axis$ points towards the viewer. Therefore, the camera is looking towards the negative $z-axis$.

![[orthogonalviewingrectangle.png|80%]]

### Transformations and viewing
>[!note]
> ==Projection== is carried out by a ==projection matrix== (transformation).

There is only one set of transformation functions so we must ==set the matrix mode first== with,
```cpp
glMatrixMode(GL_PROJECTION)
```

Transformation functions are *incremental* so we start with an identity matrix and alter with a projection matrix that gives the ==view volume==.

```cpp
glLoadIdentity();
glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);
```
The `near` and `far` distances are measured in the $-z$ direction, from the $z = 0$ plane of the camera frame.

>[!aside | right +++++]
>In 2D, the view or clipping volume becomes a ==clipping window==.


==Syntax==: `glOrtho(left, right, bottom, top, near, far)`
							 `glOrtho2d(left, right, bottom, top)`

---

## Some issues
- OpenGL will only display polygons correctly if they are:
	- **Simple** : edges cannot cross
	- **Convex** : All points on line segment between two points in a polygon are also in the polygon
	- **Flat** : All vertices are in the same plane

>[!tip]
>Triangles satisfy all conditions


---

# Attributes

==Attributes== are part of the OpenGL *state* and determine the appearance of the objects:
- Color (points, lines, polygons)
- Size and width (points, lines)
- Stipple pattern (lines, pattern — dotted or dashed lines)
- Polygon mode
	- Display as filled: solid color or stipple pattern
	- Display as edges
	- Display as vertices

## RGB color

>[!note]
>Each color component/ channel is stored separately in the framebuffer.

Usually `8 bits` per component/ channel in buffer.

Color is set by `glColor3f()` or `glColor3ub()`. The color set by `glColor` becomes part of the state and will be used until changed.

>[!note]
>Colors and other attributes **are not** part of the object but are *assigned* when the object is rendered.

>[!aside | right +++++]
>Vertices are assigned colors independently. For a triangle to have a solid color, all the vertices must have the same color.

### Smooth color
By default, OpenGL uses ==smooth shading==, where OpenGL interpolates vertex color across visible polygons.

Alternatively, in ==flat shading==, color of the *first* vertex determines fill color.

```cpp
glShadeModel(GL_SMOOTH)

glShadeModel(GL_FLAT)
```

## Viewport
- No need to use the entire window for the image, define values in pixels with
- Allow you to have multiple view of the same object
```cpp
glViewport(x, y, w, h)
```

![[viewport.png|80%]]

---

# Three dimensions
>[!note]
>In OpenGL, 2D applications are a special case of 3D graphics

>[!caution]
>Consider the order in which polygons are drawn or use hidden-surface removal. Polygons should also be simple, convex, flat.

---

# 2D Sierpinski Gasket
>[!note] Constructing the Gasket fractal
>Recursively subdivide the triangle

![[gaskettriangle.png|50%]]

Note that with more subdivisions, $\textsf{area} \rightarrow 0$ and $\textsf{perimeter} \rightarrow \inf$.

# Requesting z-buffer algorithm
>[!note]
>Refer to [[Rasterization#z-Buffer algorithm]]

```cpp
// request in main()
glutInitDisplayMode( GLUT_SINGLE |
						GLUT_RGB |
						GLUT_DEPTH );

// enable in init()
glEnable(GL_DEPTH_TEST);

// clear the depth buffer in display callback
glClear(GL_COLOR_BUFFER_BIT |
		GL_DEPTH_BUFFER_BIT);
```

---