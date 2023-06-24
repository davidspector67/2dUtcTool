# README
# Some way to compile C code (currently uses gcc) is required

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for?

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up?

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines

* Writing tests
* Code review
* Other guidelines

### Who do I talk to?

* Repo owner or admin
* Other community or team contact

### Automatic Line Detection

The references files for the Canon NAFLD data were taken from a phantom tube. Since we can only perform analysis on the portion of the ultrasound scan that lay within the tube, we needed a way to automatically detect the boundary of the phantom tube.

To do so, we used a Hough transform to detect the linear boundaries in the scan-converted phantom files.

##### 1) Generate a PNG of the scan-converted image.

![](md_images/scan_converted.png)

##### 2) Convolve the scan-converted image (cv2.filter2D).

Initially, we tried to detect the boundary without modifications to the image, but we found that instead of picking up the contrast between the light gray interior of the tube and the dark gray exterior, it actually picked up the contrast between the noise speckles.

![](md_images/speckles.png)

Blurring the image reduced the noise, enabling the program to detect the boundary.

    filtered = cv2.blur(image, (7, 7))

This worked well for most phantom files. We tried adjusting the blurring kernel size, as well as the threshold values for Canny (see part 3) and Hough (see part 4), but we were unable to find a single set of values that worked for all of the files.

Instead, we ended up using a similar concept to blurring: convolution. This allowed us to specify a different filter for each of the three boundary lines. With this, we could blur only along the horizontal or vertical axis, leaving the desired line relatively clean and easy to detect.

    filtered = cv2.filter2D(src=gray_arr, ddepth=-1, kernel=filter)

![](md_images/show_blurred_0.png)
![](md_images/show_blurred_1.png)
![](md_images/show_blurred_2.png)

##### 3) Edge detection.

This step simplifies the data into edge (white) or no edge (black).

    cv2.Canny(filtered, thresh1, thresh2)

We initially struggled to find a threshold range that would work well for all of the phantoms. However, using different convolution kernels for each of the three lines to be detected enabled us to also specify different threshold ranges for each boundary. Through trial and error, we found that a threshold range of 35-60 worked best for the bottom and left boundaries, but the right boundary was a bit more difficult to detect, so we lowered the threshold range to 30-50.

![](md_images/show_edges_0.png)
![](md_images/show_edges_1.png)
![](md_images/show_edges_2.png)

##### 4) Hough transform line detection.

This function uses the edge data generated in the previous step to identify lines. Again, trial and error revealed that a threshold of 40 worked best. After detecting all of the lines, we isolated the desired lines based on angle and position of the x/y coordinates and selected the line of the highest confidence for each of the three boundary lines.

    cv2.HoughLines(edges, 1, np.pi/180, threshold, min_theta=angle1, max_theta=angle2)

![](md_images/show_result.png)

##### Future Steps

Now that the line detection works well, we need to integrate it into the GUI and use it to exclude windows that lie outside of these boundary lines.