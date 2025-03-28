# mConvShellTex

**mConvShellTex** is a Python visualization package for rendering 3D mantle convection simulations. It utilizes **3D cartographic projection** and **shell texturing** to create novel visualizations of mantle dynamics.

## Features

- **3D Cartographic Projection**: Transforms latitude and longitude coordinates onto a 2D ellipse while using simulation radius as height (e.g., [Coppin P.W. 2021](https://virtual.ieeevis.org/year/2021/poster_a-sciviscontest-posters-1007.html)). This projection reduces occlusion and enhances the visibility of internal structures.
- **Shell Texturing**: Visualizes isosurfaces by computing 2D temperature contours at multiple radial shell levels, assigning color variations to improve depth perception (e.g., [`GarrettGunnell/Shell-Texturing`](https://github.com/GarrettGunnell/Shell-Texturing)).

## Visualization Output  

![out_zm_f100_dpi300](https://github.com/user-attachments/assets/598cd281-4d2a-424e-a0a6-a18279fafbf7)


Each frame of the visualization represents a time step of the simulation, showing surfaces of equal temperature at different depths. The color scheme helps distinguish vertical layering, making it easier to interpret mantle convection patterns.

Rotation can also be added:

![out_rotzm_f100_dpi300](https://github.com/user-attachments/assets/b36e9662-15d2-438b-8d71-8ed281ba4739)

## Recognition  

This package received an **honorable mention** in the *Acerola Shell Texturing Graphics Competition* for its innovative use of volumetric rendering in geophysical visualization.

See here for the highlight: [timestamp](https://youtu.be/O-2viBhLTqI?t=1698).

## Installation & Usage  

(*Add installation instructions and usage examples here.*)

