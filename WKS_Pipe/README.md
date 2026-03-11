# Hyperbolic Pipe Geometry Interpolator

## Description

This module is designed to calculate the intermediate spatial coordinates `(X, Y)` of curved pipe structures. This solution is applicable when only the boundary dimensions of the part are known (maximum and minimum diameters, as well as the total length). The pipe profile is described by a hyperbolic function.

> This mathematical solution generates an array of discrete points with a specified step and automatically transmits them for further processing (e.g., for CNC machines or quality control systems).

## Tech 

### Python:
- numpy 
- requests

## Mathematical Module

The mathematical core is based on the canonical equation of a hyperbola. The pipe profile is modeled taking into account the shift of the coordinate system's center to the middle of the part.

Equation of a hyperbola:
$$\frac{y^2}{b^2} - \frac{x^2}{a^2} = 1$$

- b - semi-minor axis (determined by the minimum radius at the center of the pipe)

- a - parameter dynamically calculated using the known boundary conditions (pipe length and maximum radius at the ends)

![hyperbolic Pipe Geometry](/WKS_Pipe/img/kws_math_background.png)

To calculate the hyperbola parameter a, we use a formula that expresses a through a point guaranteed to be on the pipe.

$$a = \sqrt{\frac{x_t^2}{\frac{y_t^2}{b^2} - 1}}$$

- `x_t` - half of the pipe length, representing the X-axis coordinate of the point guaranteed to lie on the pipe.

- `y_t` - maximum radius, representing the Y-axis coordinate of the known point, which corresponds to the `x_t` coordinate.

The code implements an adaptation of this equation with the center shifted. The calculation of the Y coordinate for any point X is performed using the derived formula:
$$y(x) = b \sqrt{1 + \frac{(x - \frac{L}{2})^2}{a^2}}$$

- L - pipe length

- x - an element of the X list

- a, b - calculated hyperbola parameters

## Architectural Solutions

The core logic is encapsulated within the `Pipe` class. It provides:

- protection of basic geometric constants from accidental modification

- utilization of the `numpy` library for fast calculation of the point array

- the `calculate_points_Y` method, which allows adjusting the distance between points depending on the requirements

### calculate_points_Y

A method of the `Pipe` class for calculating the x and y coordinates of points along the pipe's curve.

It takes the step value between $x$ coordinates and creates an evenly spaced list of $X$ points using the `numpy.linspace` library function.

It calculates the $Y$ list for the y coordinates of points on the pipe corresponding to the $X$ list.

It applies the following formula to each $X$ value:
$$y = b \sqrt{1 + \frac{(x - \frac{L}{2})^2}{a^2}}$$

- L - pipe length
- x - an element of the X list
- a, b - hyperbola parameters calculated in the **init** constructor

Next, it outputs the coordinates as a list consisting of dictionaries.

## Generating Coordinates

The calculation of intermediate points is performed with a specified step. The result is returned as a list of dictionaries for easy JSON serialization:

### Usage

Create a `Pipe` object and pass the known pipe parameters:

- `longest_dim` - the largest diameter of the pipe

- `shortest_dim` - the narrowest diameter of the pipe

- `pipe_length` - the total length of the pipe

Call the `calculate_points_Y` method and pass the step value between points along the X-axis:

- `Y_sample` - a list of dictionaries, where each dictionary contains $X$ and $Y$ keys.

If you have an endpoint capable of processing the data from the calculate_points_Y function, use code similar to this:

```python
url = "http://127.0.0.1:8000/[your endpoint URI]"
response = requests.post(url, json=Y_sample)
```
url - the URL address of the endpoint; change this to yours.

<div align="center">

**Authors**  
[@cyjiky](https://github.com/cyjiky) $\cdot$ [@yeghor](https://github.com/yeghor)

</div>
