


import sys
from PIL import Image

def png_to_ico(png_file, ico_file):
    # Load the png file
    logo = Image.open(png_file)

    # Save the image as an ico file
    logo.save(ico_file, format='ICO')

if __name__ == '__main__':
    #if len(sys.argv) != 3:
    print("Usage: python png2ico.py image.png image.ico")
    #sys.exit(1)

    png_file = sys.argv[1]
    ico_file = sys.argv[2]

    png_to_ico(png_file, ico_file)
    print(f"convert {png_file} to {ico_file} OK")
