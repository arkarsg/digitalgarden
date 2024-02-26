#### Question 1
**What is a GLUT display callback function? Give example events for which the display callback function should be called.**

The display callback is executed whenever GLUT determines that the window should be refreshed.
Example of events:
- window is first opened
- window is reshaped
- window is resized
- window is exposed/ covered
- user programs wishes to change the display

>[!caution]
>Include that events are *user registered* and needs window to be refreshed/ redrawn.

---

#### Question 2
**What is the use of the GLUT function `glutPostRedisplay()`?**

`glutPostRedisplay()` sets a flag which invokes the display callback function at the end of the event loop. In other words, this marks the plane of *current window* needing to be redisplayed.

>[!caution]
>For example, if we want to draw 10 circles, window will be refreshed 10 times if we use callbacks only. However, this is inefficient. If we call `postRedisplay()`, it sets a flag and knows that it should refresh, and will only refresh after drawing all 10 circles.

---

#### Question 3
**How does double buffering work? Why do we use it?**

In double buffering, there are two color buffers, front buffer and back buffer. At the end of display callback, the buffers are swapped.

One buffer is read and displayed while the other buffer is drawn into. This hides the rendering process and flickering from the user.

>[!caution]
>The switching is continuous. For example, if there is only 1 buffer for display and rendering, it will show partially rendered objects.

---

#### Question 4

Consider 2 polygons arranged such that a part of polygon, A, exists behind polygon B and a part of A extends in front of B. There is no arrangement that can be sorted in back-to-front order as polygon A is simultaneously in front and behind polygon B.

>[!caution]
>This is called cyclical occlusion. To render this, render the parts that are overlapping rather than treating it as a set of rectangles/ shapes.

---

#### Question 5

>[!caution]
>Note that the viewport is defined from the bottom left corner. There can be multiple viewports. It can be larger than the window but the image will be clipped off. With `glClear()`, it clears the entire viewport.


----

#### Question 6

>[!caution]
> We are taking the proportion of `(x, y)` relative to the window `(x_min, x_max, y_min, y_max)` and scaling it to the viewport.

---

#### Question 7

>[!caution]
