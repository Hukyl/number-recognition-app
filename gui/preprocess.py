import math

from scipy import ndimage
import cv2
import numpy as np
from PIL import Image


def _get_best_shift(img):
    cy, cx = ndimage.center_of_mass(img)

    rows, cols = img.shape
    shiftx = np.round(cols / 2.0 - cx).astype(int)
    shifty = np.round(rows / 2.0 - cy).astype(int)

    return shiftx, shifty


def _shift(img: np.ndarray, sx: float, sy: float):
    rows, cols = img.shape
    M = np.array([
        [1.0, 0.0, sx],
        [0.0, 1.0, sy]
    ]).astype(np.float32)
    shifted = cv2.warpAffine(img, M, (cols, rows))
    return shifted


def prepare_image(img: Image.Image):
    numpy_image = np.array(img)

    # Convert RGBA to grayscale
    gray = cv2.cvtColor(numpy_image, cv2.COLOR_RGBA2GRAY)

    # rescale it
    gray = cv2.resize(255 - gray, (28, 28))  # type: ignore
    # better black and white version
    (_, gray) = cv2.threshold(
        gray, 128, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )

    # Delete top row if empty
    while np.sum(gray[0]) == 0:
        gray = gray[1:]

    # Delete left column if empty
    while np.sum(gray[:, 0]) == 0:
        gray = np.delete(gray, 0, 1)

    # Delete bottom row if empty
    while np.sum(gray[-1]) == 0:
        gray = gray[:-1]

    # Delete right column if empty
    while np.sum(gray[:, -1]) == 0:
        gray = np.delete(gray, -1, 1)

    rows, cols = gray.shape

    if rows > cols:
        factor = 20.0 / rows
        rows = 20
        cols = int(round(cols * factor))
        # first cols than rows
        gray = cv2.resize(gray, (cols, rows))
    else:
        factor = 20.0 / cols
        cols = 20
        rows = int(round(rows*factor))
        # first cols than rows
        gray = cv2.resize(gray, (cols, rows))

    colsPadding = (
        int(math.ceil((28-cols)/2.0)),
        int(math.floor((28-cols)/2.0))
    )
    rowsPadding = (
        int(math.ceil((28-rows)/2.0)),
        int(math.floor((28-rows)/2.0))
    )
    gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')

    shiftx, shifty = _get_best_shift(gray)
    shifted = _shift(gray, shiftx, shifty)

    return shifted.flatten() / 255.0  # type: ignore
