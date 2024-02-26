#cs3241 #notes 

# Graphical inputs
==Devices== can be described by their *physical properties*, such as mouse, keyboard, etc and their *logical properties* returned to program via API such as position, object identifier.


```start-multi-column
ID: ID_2edl
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

## Trigger
Input devices contain a *trigger* which can be used to send a signal to the operating system

--- column-end ---

## Measure
When triggered, input devices return information (their *measure*) to the system
- Mouse → position information
- Keyboard → ASCII code

--- end-multi-column

---

## Events
Most systems have more than one input device, each of which can be triggered at an arbitrary time by a user.

Each trigger generates an ==event== whose *measure* is put in an ==event queue== which can be examined by the user program.

![[triggerandmeasure.png|80%]]

| **Types** | **Event**                                                            |
| --------- | -------------------------------------------------------------------- |
| Window    | resize, expose, minimise                                             |
| Mouse     | Click one or more buttons                                            |
| Motion    | Mouse movement                                                       |
| Keyboard  | Press or release key                                                 |
| Idle      | Non-event (define what should be done if no other event is in queue) |

---

## Callbacks

>[!note] Callbacks
>Callbacks are *programming interface* for ==event-driven== input.

If a *callback* function is defined, the user-supplied function is executed when the event occurs for each type of event the graphics system recognizes.

### Examples
```cpp
glutMouseFunc(myMouse);
glutDisplayFunc
glutReshapeFunc
glutKeyboardFunc
glutIdleFunc
glutMotionFunc, glutPassiveMotionFunc
```

---

### Event loops

>[!caution]
>Also refer to ![[OpenGL#Event loop]]


The `glutMainLoop()` puts the program in an **infinite event loop**.

In each pass through the event loop, GLUT
- looks at the events in the queue
- for each event in the queue, GLUT executes the appropriate callback function if one is defined
- if no callback is defined for the event, the event is ignored

### Display callback
>[!note]
> The display callback is executed whenever GLUT determines that the window should be refreshed.

**Event**:
- window is first opened
- window is reshaped
- window is exposed
- user programs wishes to change the display

In `main`, `glutDisplayFunc(mydisplay)` identifies the function to be executed.

>[!caution]
>Every GLUT program must have a display callback.

---

#### **Redisplays**

Many events may invoke the display callback function which can lead to multiple executions of the display callback on a single pass through the event loop. To avoid this, we can use `glutPostRedisplay()` which sets a flag.

>[!info] Why do we want to avoid this?

GLUT checks to see if the flag is set at the end of the event loop. If set, then the display callback function is executed.

#### **Animating a display**

When we *redraw* the display through the display callback, `glClear()` is called before drawing the altered display.

>[!caution] The problem
>The drawing of information in the frame buffer is decoupled from the display of its contents as graphics systems use *dual-ported* memory.
>
>Hence, partially drawn display is observed and causes flickering during animation.

---

#### **Double buffer**

>[!note]
>Instead of one ==color buffer==, we use:
>> 1. **Front buffer** : one that is *displayed* but not written to
>> 2. **Back buffer** : one that is *written* to but not displayed

Program requests ==double buffer== in `main()`. At the end of the ==display callback==, buffers are *swapped*.

```cpp

void mydisplay() {
	glClear(GL_COLOR_BUFFER | ...);
	/* draw graphics here */
	glutSwapBuffer();

}
```

---

### Idle callback

>[!note]
>The idle callback is executed whenever there are no events in the event queue. This is useful for animations.

```cpp
void myIdle() {
	// change something
	t += dt
	glutPostRedisplay();
}

void mydisplay() {
	glClear();

	// draw something that depends on t

	glutSwapBuffers();
}
```

---

### Globals

Note that the function arguments and signature for GLUT callbacks are fixed. Therefore, we need to use **globals** to pass information to callbacks.

---

# Working with callbacks

## Mouse callback

### Positioning
To **window system (and mouse and motion callback)**, position in window is measured in pixels with the ==origin at the top-left corner==. This is the consequence of refresh done from top to bottom.

Position in window is measured in pixels with the origin at the ==bottom-left corner==.
→ Need to invert $y$ coordinate returned by callback by height of window

$$
y_{\textsf{opengl}} = h - 1 - y_{\textsf{win}}
$$

To invert the $y$ position, we need the window height, which can change during program execution.


## Motion callback
>[!note] Use case
>`gultMotionFunc(drawSqaure)` : Draw an object continuously as long as a mouse button is depressed by using the ==motion callback==.
>
>`glutPassiveMotionFunc(drawSquare)` : Draw objects without depressing a button by using the ==passive motion callback==.

## Keyboard callbacks

`glutKeyboardFunc(mykey)`
`void mykey(unsigned char key, int x, int y)`

**Returns** : ASCII code of key depressed and mouse location

---

# Reshaping the window

>[!aside | right +++++]
>Forcing to fit the whole world can alter aspect ratio and cause distortion.

We can *reshape* and *resize* OpenGL display window by pulling the corner of the window. When it is reshaped or resized, the application must:
- redraw
- either display *part* of the world or display the *whole* world but force to fit in new window.

## Reshape callback
`glutReshapeFunc(myreshape)`
`void myreshape(int w, int h)`

**Returns** : the width and height of new window in *pixels*.

>[!note]
> - *Redisplay* is posted automatically at end of the execution of the callback
> - GLUT has a default reshape callback, but good to define your own.

The reshape callback is good to put viewing functions because it is invoked when the window is first opened.

---

>[!caution]
>Refer to lecture slides for additional references and other functions in GLUT

### Example Reshape

==Preserves shapes== by making the viewport and the world window have the same aspect ratio.

```cpp
void myReshape(int w, int h) {
	glViewPort(0, 0, w, h);
	glMatrixMode(GL_PROJECTION); // switch matrix mode
	glLoadIdentity();

	if (w <= h) {
		gluOrtho2D(-2.0, 2.0, -2.0 * (GLfloat) h / 2,
							2.0 * (GLfloat) h / 2);
	} else {
		gluOrtho2D(-2.0 * (GLfloat) w / h,
					2.0 * (GLfloat) w/h, -2.0, 2.0);
	}

	glMatrixMode(GL_MODELVIEW);
}
```