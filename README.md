# Automatic Hand Detection using Wrist Localisation

## Description
This program will help you locate your hand in an image. It does so by detecting approximate location of your wrist and then extracting the hand region above it.

The main purpose of this program is to remove the arm region as much as possible.

## Usage
1. Put image path in the variable IMAGE\_FILE in __get\_my\_hand.py__. Or you can also provide image using -i or --image

   > `python get_my_hand.py -i path\to\img.jpg`

2. Run the file
3. If the hand appears to be upside down, make the 'CORRECTION_NEEDED' variable True.

## Sample results

Original image:

![This was supposed to be the original image](https://github.com/dev-td7/Automatic-Hand-Detection-using-Wrist-localisation/blob/master/sample-results/original.PNG?raw=true)

Result:

![This was supposed to be the result image](https://github.com/dev-td7/Automatic-Hand-Detection-using-Wrist-localisation/blob/master/sample-results/result.PNG?raw=true)

## Constraints
1. There should be good lighting conditions. The wrist detection is heavily dependent on lighting conditions and poor light may lead to poor results.
2. Hand must be in an open state (Like a High-five). If hand is closed (like a fist), the result may not be so accurate.

## References
1. [Grzejszczak T., Nalepa J., Kawulok M. (2013) Real-Time Wrist Localization in Hand Silhouettes. In: Burduk R., Jackowski K., Kurzynski M., Wozniak M., Zolnierek A. (eds) Proceedings of the 8th International Conference on Computer Recognition Systems CORES 2013. Advances in Intelligent Systems and Computing, vol 226. Springer, Heidelberg](https://link.springer.com/chapter/10.1007/978-3-319-00969-8_43#citeas "Link to the technical paper from which I got the idea")
2. [This guy's program showed me how I can detect hands](https://github.com/lzane/Fingers-Detection-using-OpenCV-and-Python)
___
PS: This program logic would soon be part of my undergraduate project. I will reference it here soon!