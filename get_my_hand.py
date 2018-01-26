"""
Tejas Dastane,
January 25, 2018.

Hand detection using wrist localisation.

Only provide images with hands open (Such as a High-five). Image of a hand which is closed (like fist) may not work
"""

# Imports
import cv2, imutils as im, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',help='Supply image to the program')
args = vars(ap.parse_args())

CORRECTION_NEEDED, IMAGE_FILE = False, 'images/test.jpg'

if args.get('image'): IMAGE_FILE = args.get('image')

# Define lower and upper bounds of skin areas in YCrCb colour space.
lower = np.array([0,139,60],np.uint8)
upper = np.array([255,180,127],np.uint8)

# Read image
img = cv2.imread(IMAGE_FILE)
img = cv2.resize(img, (int(img.shape[1]/2),int(img.shape[0]/2)))
original = img.copy()

# Extract skin areas from the image and apply thresholding
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
mask = cv2.inRange(ycrcb,lower,upper)
skin = cv2.bitwise_and(ycrcb, ycrcb, mask=mask)
_,black_and_white = cv2.threshold(mask,127,255,0)

# Find contours from the thresholded image
_,contours,_ = cv2.findContours(black_and_white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Get the maximum contour. It is usually the hand.
length = len(contours)
maxArea = -1
final_image = np.zeros(img.shape, np.uint8)
if length > 0:
    for i in range(length):
        temp = contours[i]
        area = cv2.contourArea(temp)
        if area > maxArea:
            maxArea = area
            ci = i
    largest_contour = contours[ci]

    # Draw it on the image, in case you need to see the ellipse.
    cv2.drawContours(final_image, [largest_contour], 0, (0, 255, 0), 2)

    # Get the angle of inclination
    ellipse = _,_,angle = cv2.fitEllipse(largest_contour)

    # This statement is kept for debugging purposes only.
    final_image = cv2.ellipse(final_image, ellipse, (0,255,0), thickness=2)

''' 
# Uncomment for debugging
cv2.imshow('Hand image with contours and ellipse', final_image)
cv2.waitKey(100000)
cv2.destroyAllWindows()
 '''

# Vertical adjustment correction
'''
This variable is used when the result of hand segmentation is upside down. Will change it to 0 or 180 to correct the actual angle.
The issue arises because the angle is returned only between 0 and 180, rather than 360.
'''
vertical_adjustment_correction = 0
if CORRECTION_NEEDED: vertical_adjustment_correction = 180

# Rotate the image to get hand upright
if angle>=90: black_and_white = im.rotate_bound(black_and_white, vertical_adjustment_correction+180-angle)
else: black_and_white = im.rotate_bound(black_and_white, vertical_adjustment_correction-angle)

# print('Angle: '+str(angle)) # For debugging purposes only.

h,w = black_and_white.shape

# Find contours
_,contours,_ = cv2.findContours(black_and_white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Get the biggest contour
length = len(contours)
maxArea = -1
final_image = np.zeros(img.shape, np.uint8)
if length > 0:
    for i in range(length):
        temp = contours[i]
        area = cv2.contourArea(temp)
        if area > maxArea:
            maxArea = area
            ci = i
    largest_contour = contours[ci]

    # Get position of hand region from the image. Returns point(x,y) - the top left point and height and width of rectangle
    x,y,w,h = cv2.boundingRect(largest_contour)

    # Use this for debugging if needed
    final_image = cv2.rectangle(skin, (x,y), (x+w,y+h), (0,255,0),thickness=2)

# Extract hand part from the image.
final_image = black_and_white[y:y+h,x:x+w]
temp = final_image.tolist()
n = len(temp)

'''
Since rotate_bound keeps the image intact, any part of the hand present at the end could interfere with our wrist detection.
We traverse until the count of pixels increases and we remove the slanted region formed due to rotate_bound.
'''
min_count, final_row, prev_count = w, 0, 0
counts=[]
i=n-1
for i in range(n-1,int(n/2),-1):
    count=int(sum(temp[i])/255)
    if count<prev_count:
        start = i
        break
    prev_count = count

'''
Now traverse from upwards until half the image 
(Because at the top we have fingers whose pixel count is less than wrist and we want to avoid them)
and find the wrist - having least count of pixels. Get row number of wrist
'''
for i in range(start,int(n/2),-1):
    count=int(sum(temp[i])/255)
    counts.append(count)
    if count<=min_count:
        final_row = i+1
        min_count=count

'''
Uncomment for debugging
# print(final_row)
# print(min_count)
# print(counts)
'''

# Extract the hand part and remove the arm part
final_image = final_image[:final_row,:]

# Show results
cv2.imshow('Extracted Hand', final_image)
cv2.imshow('Original image',original)
cv2.waitKey(100000)
cv2.destroyAllWindows()