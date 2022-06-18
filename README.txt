Measuring the linear width of an image

[Basic functions]
Input file: JPG (1600 X 1200)
Line definition: a light-colored line on a dark background or a dark-colored line on a light background, either vertically or horizontally
Line width definition: Vertical or horizontal difference of the line outline
Drawing the measurement results: Draw the measurement results on the image using the file you received as a reference.
Output measurement result: Output [original image file name, output image file name, vertical/horizontal judgment, black/white judgment, line width X 10] in CSV format.

[How to use] 1.

1. environment setup

Install the package according to requirements.txt

pip install -r requirements.text

Check the folder structure


before : Folder containing images to be processed
after : Folder containing processed images and csv
ipaexg00401 : Folder containing IPA fonts

Note: There are restrictions on image files.

- jpg files (with .jpg extension)
- Resolution : 1600 X 1200
- Name must be alphanumeric symbols only (Japanese and Greek characters are not allowed)

3. program execution

Execute the program in python.

python main.py

The executable main.py will look for the before and after folders in the same folder.
The gip file is open and ready to run.
Even if the file is accidentally moved or deleted, it will work if the folder with the same name exists.

The brightness of the background image and the height and width of the line are determined and processed.
The processed image and the csv of the processed result are stored in the after folder.

[If it doesn't work]

Lines may not be recognized well depending on the input image.
Try adjusting the following values in the main function according to the color of the background image.

if __name__ == "__main__":
    #Boundary value for binarizing the image when the background image is white
    WHITE_BOUNDARY = 127
    #Boundary value for binarizing an image with a black background
    BLACK_BOUNDARY = 40
    main(WHITE_BOUNDARY,BLACK_BOUNDARY)

WHITE_BOUNDARY = 127

Boundary value for binarizing an image with a white background.
The value can be set between 0~255.
If the lines are too white to be recognized, lowering this value will make them easier to recognize.


BLACK_BOUNDARY = 40

Boundary value for binarization of images with black background.
The value can be set between 0 and 255.
If the lines are too black to be recognized, increasing this value will make them easier to recognize.
