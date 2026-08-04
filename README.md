<h1 align="center">Simple Image Ditherer</h1>

<p align="center"><strong>Performant Python image dithering tool</strong><br></p>

![Landing image for simple image ditherer showcasing UI](/assets/readME_landing_image.png)

## What this is:
Exactly what it says in the tin! A simple lightweight image dithering tool. Parses images using numpy arrays and Numba JIT compiling to be as performant as possible. Able to process a rage of different dithering algorithms, including:

- Ordered dithering using Bayer's matrices
- Error diffusion (Floyd-Steinberg & Atkinson)

The tool is also capable of limited image preprocessing, colourising dithered outputs and applying bloom effects, all wrapped in an intuitive GUI.

## How to run this:
This project was developed in Python version 3.13.3 and must be installed prior to using this tool. Installation is simple, follow the steps below:
1) Download the repository
2) Run the following command "python [your local directory to the repository]/main.py"

**That's it!**

## Features:

There are three main tabs in the navigation bar which all manipulate the image in different ways. The buttons along the bottom of the GUI allow for loading, saving and resetting the image.

### Adjust

This tab performs pre-processing of the images and is applied prior to the dithering. There are two settings: 
- ***Contrast*** which will increase the value of the pixels 
- ***Brightness*** which linearly adds or subtracts values to all the pixels in the image

### Dithering

This is where the real meat and potatoes of the tool reside. It contains the core functionality of the tool and these adjustments all affect the dithering in one way or another.
- The ***Algorithm*** drop down changes what dithering method is applied to the image
- ***Noise*** will add randomised greyscale pixel values to the dithered image, useful if the dithered output is too ordered
- ***Values*** determines the range of values in the dithered image, between 2 - 6. Higher the value, higher the fidelity of the final output
- ***Pixel Size*** changes how large or small the pixels of the image are exponentially. The default is 1 : 1 to the original image

### Effects

The effects tab colourises and adds bloom effects to the dithered image and is applied after the image is dithered.

- ***Colour Map*** allows the colour palette of the dithered greyscale output to be changed. The number of colours is determined by the ***Values*** slider and defaults to greyscale values between white and black
- ***Bloom Intensity*** adjusts how strong the bloom effect is applied. The bloom selects the last colour as the threshold value upon which all pixel values brighter will have the bloom applied to it.
- ***Bloom Spread*** adjusts how many pixels the bloom is applied to. It has an inner and outer range where different intensities are applied (box bloom)