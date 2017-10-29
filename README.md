# Linked Pixel Steganography technique
Linked Pixel Steganography (LPS) technique is a variant of the well-known LSB steganography. It can be applied to any type of images.
## How it works
LPS doesn’t hide data sequentially in the image. It is inspired by linked list in algorithmic. Just like linked lists, every “block” contains data parts and a pointer to the next pixel holding the rest of the data. Each pixel of an image is composed of at least three channels (R, G, B). LPS uses the LSB of each channel for different usage.

![](/Images/LPS_schema.png?raw=true)

Since LPS uses LSB, several pixels are needed to store the binary representation of the coordinate of the next pixel. That’s why LPS uses blocks of consecutive pixels. The block size is calculated from the image size in pixel, it’s the number of bits needed to store the highest value (height or width). Data is then split into chunks of the same size and padding is added at the end if needed.

![](/Images/decomposition.png?raw=true)

To recover data correctly, one needs to know the coordinates of the starting pixel and calculate the block size. From then, every next pixel can be recovered by reading blocks, until the coordinates of the next pixel are (0, 0). Like in linked lists, the last element has a NULL pointer, which in this case is represented with coordinates of 0.
## Test 1 – LPS on regular PNG image
### Message hidden
>Microsoft se plie à l'écriture inclusive à sa façon. La dernière mise à jour de son logiciel de traitement de texte Word, réservée aux abonnés Office, comprend dans ses paramètres de grammaire et de style une option de «langage inclusif». Une telle fonctionnalité «cible le langage genré à même d'exclure, de rejeter ou de stéréotyper», est-il indiqué sur le site de l'entreprise.
Pour rappel, l'écriture inclusive consiste à inclure le féminin, entrecoupé de points, dans les noms, comme dans «mes ami·e·s» ou «les candidat·e·s à la présidentielle, pour le rendre «visible» et prôner des règles grammaticales plus neutres. L'expression est le fruit d'une réflexion amorcée il y a une vingtaine d'années, autour de l'idée de neutralité dans l'écriture. Longtemps cantonnée aux mouvements féministes, cette graphie s'impose désormais dans le débat public. Le logiciel Word, lui, ne propose pas l'utilisation du point milieu. Il remplacera, par exemple, le terme «les experts» par «les experts et les expertes»

Original Image on the left and image hiding data on the right:

![](Images/test%201%20Alpha/original.png?raw=true) ![](Images/test%201%20Alpha/out.png?raw=true)

Like with LSB steganography, there is no visual difference.
### LSB analysis
![](Images/test%201%20Alpha/original_lsb.png?raw=true) ![](Images/test%201%20Alpha/out_lsb.png?raw=true)

We can clearly see stripes in homogenous areas, revealing the presence of hidden data. But in the center of the image it is very difficult to tell if something is hiding in the LSB. Unlike the classical LSB steganography technique, the randomness of the location where data is hidden makes steganalysis more difficult if the image is chosen correctly.
## Test 2 – LPS on noisy JPEG image
### Message hidden
The message is the same as in test 1.

Original Image on the left and image hiding data on the right:

<img src="Images/Test%202/original.jpg?raw=true" width="400"> <img src="Images/Test%202/out.jpg?raw=true" width="400">

No visual difference like in the previous test.
### LSB analysis
<img src="Images/Test%202/original_lsb.jpg?raw=true" width="400"> <img src="Images/Test%202/out_lsb.jpg?raw=true" width="400">

Just like we saw in figure 4, if the image is noisy, the LSB analysis won’t show clear visual difference. But with a good eye and by zooming, one can distinguish stripes due to LPS:

<img src="Images/Test%202/zoomed_out_lsb.jpg?raw=true" width="400">

The stripes are more visible in less noisy areas.
