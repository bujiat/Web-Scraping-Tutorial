import cv2


def handle_img(img):
    """
    Preprocess an image: grayscale → Gaussian blur → Canny edge detection.

    :param img: input image (BGR or BGRA)
    :return: edge-detected image
    """
    if len(img.shape) == 2:
        gray = img
    elif img.shape[2] == 4:
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)
    return cv2.Canny(blurred, 60, 60)


def match(img_jpg_path, img_png_path):
    """
    Find where the small image (slider piece) fits inside the large image (background).

    :param img_jpg_path: path to the background image
    :param img_png_path: path to the slider piece image
    :return: x-coordinate of the best match (drag distance in pixels)
    """
    img_jpg = cv2.imread(img_jpg_path, cv2.IMREAD_UNCHANGED)
    img_png = cv2.imread(img_png_path, cv2.IMREAD_UNCHANGED)
    img = handle_img(img_jpg)
    small_img = handle_img(img_png)

    res = cv2.matchTemplate(img, small_img, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    return max_loc[0]


if __name__ == "__main__":
    distance = match("pic.png", "pic2.png")
    print(distance)
