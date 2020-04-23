""""
    Views all images in a folder and separates them into folders according to user input.
"""


import argparse
import wx
import cv2
import os
from shutil import copyfile, move


def label_images(image_folder, keys, folder_names, output_folder, screen_factor, delete):
    """Labels all images in a folder and copies them to respective folders according to user input. It also produces
    a csv file with the labels of the images.

    Args:
        image_folder (str): path to the folder containing the images to be labeled
        keys (list): list of shortcuts that the user will input to label images
        folder_names (list): list of the name of the folders corresponding to the labels
        output_folder (str): path to the folder on which to store labeled images
        screen_factor (float): percentage of the screen that the image will occupy in case it is too big
        delete (bool): indicates whether or not to delete original image in image folder
    """

    # Create all folders
    create_folders(output_folder, folder_names)

    for img_name in os.listdir(image_folder):
        if is_image(img_name):
            show_image(os.path.join(image_folder, img_name), img_name, screen_factor)
            key = cv2.waitKey(0)

            for i, shortcut in enumerate(keys):
                if key == ord(shortcut):
                    if delete:
                        move(os.path.join(image_folder, img_name),
                             os.path.join(output_folder, '{}/{}'.format(folder_names[i], img_name)))
                    else:
                        copyfile(os.path.join(image_folder, img_name),
                                 os.path.join(output_folder, '{}/{}'.format(folder_names[i], img_name)))
                    break
            cv2.destroyAllWindows()


def show_image(img_path, img_name, screen_factor):
    """Shows input image to fit the screen.
    Source: https://enumap.wordpress.com/2019/02/25/python-opencv-resize-image-fit-your-screen/

    Args:
        img_path (str): path to the image
        img_name (str): name of the image
        screen_factor (float): percentage of the screen that the image will occupy in case it is too big
    """

    # get Screen Size
    w_screen, h_screen = get_screen_size()
    w = w_screen * screen_factor
    h = h_screen * screen_factor

    orig_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    height, width, depth = orig_img.shape

    if height > h or width > w:
        scale_width = float(w) / float(width)
        scale_height = float(h) / float(height)
        if scale_height > scale_width:
            img_scale = scale_width
        else:
            img_scale = scale_height

        new_x, new_y = orig_img.shape[1] * img_scale, orig_img.shape[0] * img_scale

    else:
        # No need to resize
        new_x = width
        new_y = height

    new_img = cv2.resize(orig_img, (int(new_x), int(new_y)))
    cv2.namedWindow(img_name)
    cv2.moveWindow(img_name, 30, 30)
    cv2.imshow(img_name, new_img)


def get_screen_size():
    """Determines width and height of screen.

    Returns:
        width (int): width of the screen
        height (int): height of the screen
    """

    app = wx.App(False)
    width, height = wx.GetDisplaySize()

    return width, height


def create_folders(parent_folder, subfolder_names):
    """Creates destination folder and all input sub-folders, in case they do not exist yet.

    Args:
        parent_folder (str): path to the parent folder
        subfolder_names (list): list of sub-folder names
    """

    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)

    for folder in subfolder_names:
        f = os.path.join(parent_folder, folder)
        if not os.path.exists(f):
            os.mkdir(f)


def is_image(f_name):
    """Determines whether or not the name of the file corresponds to an image

    Args:
        f_name (str): name of a file

    Returns:
        is_img (bool): whether or not the name of the file corresponds to an image
    """

    ext = os.path.splitext(f_name)[1]
    return ext in ['.png', '.jpg', '.jpeg']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_folder", type=str, help='Path to the folder containing the images.')
    parser.add_argument(
        "--output_folder", type=str, help='Path to the parent folder on which we will store copied images.')
    parser.add_argument(
        "--folder_names", type=str, nargs='*', help='Name of the folders on which to copy images (one for each class).')
    parser.add_argument(
        "--keys", type=str, nargs='*',
        help='List containing the keys that the user will press to label images (one for each class).')
    parser.add_argument(
        "--screen_factor", type=float, default=0.9,
        help='Percentage of the screen that the image will occupy in case it is too big.')
    parser.add_argument(
        '--delete', dest='delete', default=False, action='store_true')
    args = parser.parse_args()

    label_images(args.image_folder, args.keys, args.folder_names, args.output_folder, args.screen_factor,
                 args.delete)