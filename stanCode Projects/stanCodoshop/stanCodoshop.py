"""
SC101 - Assignment3
Adapted from Nick Parlante's Ghost assignment by
Jerry Liao.
-----------------------------------------------
File: stanCodoshop.py
Name: Ian Kuo
-------------------------
The objective of this program is to remove objects that does not belong to the school campus in a given series
of pictures. The way of doing this is to find out the outlier rgb and replace it with the rgb from the pixel
which has the shortest pixel distance, defined as the Euclidean Distance to average rgb.
"""

import os
import math
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the square of the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): squared distance between red, green, and blue pixel values
    """
    pixel_r = pixel.red
    pixel_g = pixel.green
    pixel_b = pixel.blue
    dist = math.sqrt((red - pixel_r) * (red - pixel_r) + (green - pixel_g) * (green - pixel_g) +
                     (blue - pixel_b) * (blue - pixel_b))
    # Calculating the Euclidean Distance between pixel rgb and average rgb
    # square root function reference from SC001 Assignment 2 quadratic_solver.py
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]
    """
    sum_r = 0
    sum_g = 0
    sum_b = 0
    for i in range(len(pixels)):
        ele = pixels[i]
        ele_r = ele.red
        sum_r += ele_r
        ele_g = ele.green
        sum_g += ele_g
        ele_b = ele.blue
        sum_b += ele_b
    pixel_avg = []
    r_avg = sum_r / len(pixels)
    g_avg = sum_g / len(pixels)
    b_avg = sum_b / len(pixels)
    pixel_avg += [r_avg, g_avg, b_avg]
    # Create a list that contains the average RGB values of a list of pixels
    return pixel_avg


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages
    """
    minimum = 10000
    mark = get_average(pixels)
    mark_r = mark[0]
    mark_g = mark[1]
    mark_b = mark[2]
    best = pixels[0]
    # Assign a pixel list, default RGB value equals to that of the first pixel
    for i in range(len(pixels)):
        ele = pixels[i]
        check = get_pixel_dist(ele, mark_r, mark_g, mark_b)
        if minimum > check:
            minimum = check
            best = ele
            # Assign the pixel with the one with the shortest pixel distance
    return best


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    ######## YOUR CODE STARTS HERE #########
    # Write code to populate image and create the 'ghost' effect
    for i in range(images[0].width):
        for j in range(images[0].height):
            check_list = []
            for k in range(len(images)):
                check_pixel = images[k].get_pixel(i, j)
                check_list.append(check_pixel)
            best = get_best_pixel(check_list)
            result.set_pixel(i, j, best)
    ######## YOUR CODE ENDS HERE ###########
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
