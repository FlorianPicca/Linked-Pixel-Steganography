# Linked Pixel Steganography technique
Linked Pixel Steganography (LPS) technique is a variant of the well-known LSB steganography. It can be applied to any type of images.
## How it works
LPS doesn’t hide data sequentially in the image. It is inspired by linked list in algorithmic. Just like linked lists, every “block” contains data parts and a pointer to the next pixel holding the rest of the data. Each pixel of an image is composed of at least three channels (R, G, B). LPS uses the LSB of each channel for different usage.

![test](/Images/LPS_schema.png?raw=true)

*Figure 1 - Usage of the different channels in LPS using blocks of size 9.*

Since LPS uses LSB, several pixels are needed to store the binary representation of the coordinate of the next pixel. That’s why LPS uses blocks of consecutive pixels. The block size is calculated from the image size in pixel, it’s the number of bits needed to store the highest value (height or width). Data is then split into chunks of the same size and padding is added at the end if needed.
