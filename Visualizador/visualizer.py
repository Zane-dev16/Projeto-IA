import sys
from PIL import Image
import numpy as np

all_pipes = ['FB', 'LV', 'VC', 'VE', 'FE', 'FC', 'VD', 'BB', 'LH', 'BE', 'BD', 'VB', 'BC', 'FD']

def visualizer(input_file):
    with open(input_file, 'r') as f:
        # Transforms the input into a grid for example, [["FC","VC"],["VC","FC"]]
        grid = [line.strip().split("\t") for line in f]
        path_to_images = 'images/'
        unique_images = {}
        common_size = (300, 300)  

        for img_code in all_pipes: # Load all pipe images into a dictonary as arrays of pixels
            if img_code not in unique_images:
                img_path = f"{path_to_images}{img_code}.png"
                image = Image.open(img_path)
                resized_image = image.resize(common_size)
                unique_images[img_code] = np.array(resized_image)

        #Concatenate the arrays of images to form the final image and save it to Grid_Image
        row_images = [np.concatenate([unique_images[img_code] for img_code in row], axis=1) for row in grid]
        final_image = np.concatenate(row_images, axis=0)
        final_image_obj = Image.fromarray(final_image)
        final_image_obj.save(f'Grid_Image.png')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualizer.py '<path to input_file>'")
        sys.exit(1)
    input_file = sys.argv[1]
    visualizer(input_file)
