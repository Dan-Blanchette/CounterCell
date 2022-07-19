#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:52:58 2022

@author: danb22
"""

import matplotlib.pyplot as plt
import skimage.io as io
import os
import skimage.filters
import skimage.color
import skimage.measure
from PIL.Image import core as _imaging


# this fucntion produces three images across the pixel channel spectrum
# def rgb_splitter(image):
#     rgb_list = ['Reds', 'Greens', 'Blues']
#     fig, ax = plt.subplots(1, 3, figsize=(15,5), sharey=True)
#     for i in range(3):
#         ax[i].imshow(image[:,:,i], cmap = rgb_list[i])
#         ax[i].set_title(rgb_list[i], fontsize = 15)


    

# prints original image plot to notebook/photoviewer
# and returns the file read variable to be used in other functions
def show_img(image):
    new_img = io.imread(image)
    plt.imshow(new_img)
    # plt.axis('off')
    plt.show()
    return new_img

# Isolates the microglia cells based on thresholded values of the RGB channels
# and gererates a modified copy of the original image with only the 
# microglia cells being identified.
def cells_only(image_path, connectivity = 1, count = 1):
    img1 = show_img(image_path)
    green_filtered_cells = (img1[:,:,1] > 132) & (img1[:,:,0] <= 97) & (img1[:,:,2] <= 97)
    
    cells_new = img1.copy()
    cells_new[:,:,0] = cells_new[:,:,0] * green_filtered_cells
    cells_new[:,:,1] = cells_new[:,:,1] * green_filtered_cells
    cells_new[:,:,2] = cells_new[:,:,2] * green_filtered_cells
    
    gray_cells = skimage.color.rgb2gray(cells_new)
    blurred_image = skimage.filters.gaussian(gray_cells, sigma = 3.0)
    mask = blurred_image > 0.1
    labeled_image, cell_count = skimage.measure.label(mask, connectivity=connectivity, return_num=True)
    print(f"There are {cell_count} cells in {image_path}")
    
    
    colored_label_image = skimage.color.label2rgb(labeled_image, bg_label=0)
    summary_image = skimage.color.gray2rgb(gray_cells)
    summary_image[mask] = colored_label_image[mask]
    
    
    # plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='none', clear=True)
    # plt.box(on=None)
    # plt.axis('off')
    plt.imshow(summary_image)
    plt.show()
    return summary_image
    
    # plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='none', clear=True)
    # plt.box(on=None)
    # plt.axis('off')
    # plt.imshow(cells_new)
    # plt.show()
    # plt.imshow(mask)
    # plt.show()