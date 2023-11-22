#notes #cs3241 


# What is Computer Graphics?

>[!note]  What is computer graphics?
>Whatever areas that have appeared in the Special Interest Group on Computer GRAPHics and Interactive Techniques (**SIGGRAPH**) annual conferences.
>
>Where research and products are showcased.
>
>Computer graphics deals with all aspects of creating images with a computer – hardware, software (algos and methods), applications.

>[!caution] In this course…
>Focus on *real-time interactive 3D computer graphics*.

## *Real time Computer Graphics*
A sub-field of computer graphics where the focus is on producing images in real-time. Real time programs must response within *specified time constraints*.

>[!aside | right +++++]
>Interactive rates depends on application. For example, interactive rates for chess will differ from interactive rates for FPS games.


This usually means *interactive rates*, where interactive refers to the interaction with the human user such that the user feels that the interaction is flowing. 

- Typically uses *GPU* as CPU may not me sufficient to produce high interactive rates.

## Display Processor

>[!aside | right +++++]
>The display processor is a precursor to GPU.


Rather than have the host computer try to refresh display, use a special purpose computer called a *display processor*.

To draw a 3D image, CPU needs to continually refresh display. As such, CPU may not have the resources for other processes. 

## Raster graphics

*Raster graphics* is an array of picture elements (pixels) in the frame buffer.

>[!note]
>Allows us to go from lines and wireframe images to filled polygons.

## Special purpose hardware

Special purpose hardware needed for rendering realism – RenderMan etc

---
# Images
## Elements of image formation
- Objects
- Viewer
- Light sources
- Materials — attribute that govern how light interacts with the materials in the scene

---

# Cameras

## Pinhole camera

Given a ==3D point==  $(x, \space y, \space z)$ , use *trigonometry* to find the projection on the screen.

![[pinholecamera.png| -center | -m]]

## Synthetic camera model

>[!aside | right +++++]
>Image plane (where projection of p) lies can be *virtual*. (ie it does not need to be on the screen of the camera). Unlike the screen of the camera, the resultant image on the image plane will *not be inverted*.

![[projectioncamera.png| -center | -m]]

---

# Luminance and colour

## Luminance images

==Luminance images== are *monochromatic* and the values are grey levels. These also represents the brightness values.

## Color image

>[!aside | right +++++]
>Light is part of the *electromagnetic spectrum* that causes a reaction in our visual systems. Its wavelengths ranges from *350 - 750 nm.* Long wavelengths appear as `red` and short wavelengths appear as *blue*.

==Color images== have perceptional attributes of *hue*, *saturation*, and *lightness* (HSL).

>[!note] Is there a need to produce/ store every frequency in the visible spectrum?

## Three-color theory

The human visual system has *2* types of light sensors.

>[!aside | right +++++]
>The *three* values sent to the brain are known as *tristimulus* values
```start-multi-column
ID: ID_td4n
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

**Rods**
- Monochromatic, night vision

--- column-end ---

**Cones**
- Color sensitive with *three* types of cones
- Therefore, only *three* values are sent to the brain

--- end-multi-column

![[sensitivityoflighttoeyes.png| -center | -s]]

Our eyes are less sensitive to blue light because the range of activation for blue light is smaller than red and green.

## Additive and subtractive color


```start-multi-column
ID: ID_8b5s
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

#### Additive color
Additive colour forms a colour by *adding* amounts of 3 ==primaries== — **RGB**.
- [i] These are usually used for CRTs, projection systems and positive film
- [i] Addition can occur in *space* – screens, or in *time* – strobing colours to give a different colour. 

--- column-end ---

#### Subtractive color
Subtractive colour forms a colour by *filtering* ==white light== with **CMYK**
- [i] This works through light-material interactions (absorption of light by material)

| **Colour** | **Subtracts** |
| ---------- | ------------- |
| Cyan       | Red           |
| Magenta    | Green         |
| Yellow     | Blue          |

- [i] Mixing **CMY** should theoretically give *black*. However, it results in a dirty brown-green mixture. Therefore, there is usually a *black* catridge.

--- end-multi-column

---

# Graphic system design

>[!note] How do we mimic the synthetic camera model to design graphics hardware and software?


There are ==2== main components in a graphic system.


```start-multi-column
ID: ID_w0ah
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

>[!note] API
>API specifies the scene which consists of ==objects, materials, viewer and light==.
>
>API also configures and controls the system.


--- column-end ---

>[!note] Renderer
> Renders the images using scene info and system configuration.

--- end-multi-column

## Rendering approaches

### Ray-tracing
==Ray-tracing== follows rays of light from center of projection until they are ==absorbed== by objects or ==go off to infinity==.

- [p] Can handle global effects — multiple reflections, translucent objects
- [c] Slow
- [c] Must have whole database available at all times

### Radiosity
==Radiosity== is an energy based approach which is very slow and not general.

--- 

# Polygon Rasterization

Image is generated ==incrementally== by processing *polygons* (priimitives) one at a time in order they are generated by the application.
- **Transform**: map each polygon from 3D space to 2D image space
- **Rasterize**: assign colours to the pixels occupied by the polygon

This approach only considers *local lighting* and is *primitive-based rendering*.

#### Polygons
>[!aside | right +++++]
>Polygons are an approximation to represent a 3D object
>
>Each polygon is projected onto the 2D image space (*transform*). The pixels interior of the polygon in the 2D image is then turned on (*rasterization*).


3D objects are *approximated* by and represented as a net or ==mesh== of planar polygonal facets.

![[objecttovertices.png| -center | -m]]

## Rendering pipeline

The pipeline consists of stages that ==each primitive== must go through.

>[!note] Objective
>Turn each given primitive into pixels in the frame buffer.

>[!aside | right +++++]
> ==Primitive== refers to a polygon.

![[vertexpipeline.png| -center | -m]]

![[vertexpipelineexample.png| -center | -m]]

### Vertex processing

Converting object representations from one coordinate system to another occurs here. Each change of coordinates is equivalent to a ==matrix transformation==.

Vertex processor also compute ==vertex colors== (lighting)

The coordinate can be:
1. Object coordinates
2. Camera coordinates
3. Screen coordinates

#### Projection

==Projection== is the process that combines the 3D viewer with the 3D objects to produce the ==2D== image. There are 2 types of projections:
1. **Perspective projections**: all projectors meet at the center of the projection
2. **Parallel projection**: projectors are parallel, center of projection is replaced by a direction of projection

### Primitive assembly

Vertices are collected into geometric objects/ primitives before clipping and rasterization can take place. These objects are:
1. Line segments
2. Polygons
3. Curves and surfaces

### Clipping

Objects that are not within the ==view volume== are said to be clipped out the scene.

### Rasterization

If an object/ primitive is not clipped out (ie it is within the scene), the appropriate pixels in the frame buffer must be assigned colours.

Rasterizer produces a set of ==fragments== for each object.

### Fragment Processing
>[!aside | right +++++]
>They are referred to as potential pixels as they may not even be in the window space as it may be removed by $z$-buffer

>[!note] Fragments
> ==Fragments== are *potential pixels* which have location in the frame buffer and have ==colour== and ==depth== attributes.
> 
> Vertex attributes are interpolated over primitives by the rasterizer.

Fragments are processed to determine the colour of the corresponding pixel in the frame buffer.

>[!note]
>Refer to [[Rasterization#Interpolation of vertex attributes]]

Colours can be determined by ==texture mapping== or ==interpolation of vertex colours==.

Fragments may be blocked/ occluded by other fragments — **hidden surface removal**.

---

# API

- Includes ==functions== that specify what is needed to form an image
	- Image
	- Viewer
	- Light source(s)
	- Materials
- Input from devices such as mouse and keyboard
- Capabilities of system

All primitives are defined through ==location== in space or *vertices*.

## Camera specification
- Six degrees of freedom — position and orientation
- Lens
- Film size
- Orientation of film plane

## Lights and materials
- Types of lights
	- Point sources vs distributed sources
	- Spot lights
	- Near and far sources
	- Colour properties
- Material properties
	- Absorption: color properties
	- Scattering — **diffusion**, **specular**

---

