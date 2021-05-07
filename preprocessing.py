import numpy as np
import requests

from io import BytesIO
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor


IMAGES_DATA = {
    'Test': {
        'label': 0,
        'link': 'https://sun9-10.userapi.com/impg/IqwCSKy823u3i4ISYXvnU4hreyA8x41b2d6Bmw/VhL-AVYOFdM.jpg?size=300x300&quality=96&sign=073b841060915bec433e3941807143da&type=album'
        },
    'Medal': {
        'label': 1,
        'link': 'https://sun9-41.userapi.com/impg/kolpkBbUGsqG_DGT3QHCgZ_2AzcE6KabeOTW7A/hvhYD0DNTV0.jpg?size=300x300&quality=96&sign=3696a1655d49ea78740b11518f98c854&type=album'
        },
    'PC': {
        'label': 2,
        'link': 'https://sun9-13.userapi.com/impg/lUWcBWPQ_tUJBWRX0adYVTcUX3QUakmdEAxEww/zSfm2knDTHI.jpg?size=300x300&quality=96&sign=72bcc83ca867a4567b1ed8a1958f0319&type=album'
        },
    'Search': {
        'label': 3,
        'link': 'https://sun9-43.userapi.com/impg/857PPw7zUBDcSzmxTrhxL-EpIF7-OIjevOPjjg/hh4I_LDh_dU.jpg?size=300x300&quality=96&sign=7618c81ed53ed53c7e9cf97bf1366b08&type=album'
        },
    'Projector': {
        'label': 4,
        'link': 'https://sun9-54.userapi.com/impg/1nCzXyvB0j8EjETWpmfy5tqvtO_eepe62t8fpg/cTDdThN8uBs.jpg?size=300x300&quality=96&sign=f004fec3d74b991615c4c67f5d0a3582&type=album'
        },
    'Idea': {
        'label': 5,
        'link': 'https://sun9-16.userapi.com/impg/2Pjh7MNLhJfZpJDyaNfWIE-aEJ868rcnR8rBFg/UGVC5u6YRtE.jpg?size=300x300&quality=96&sign=c1effa508282155b2bcf6c2e67fc79d2&type=album'
        },
    'Telescope': {
        'label': 6,
        'link': 'https://sun9-43.userapi.com/impg/nQv8nfsZBmu2GRWL1UQlh-BURPJX_7u7zSFYSw/c9lnX1pexDc.jpg?size=300x300&quality=96&sign=9cfa9affb68d7f6a3180065c87498669&type=album'
        },
    'Briefcase': {
        'label': 7,
        'link': 'https://sun9-21.userapi.com/impg/ZpAA5wx-NBJkktxWeZnGKGlOic46otyWgIAaXg/3rp4JeH5K5Y.jpg?size=300x300&quality=96&sign=76e0cf1f67c4ae236767b9c0eedae58b&type=album'
        },
    'Trofy': {
        'label': 8,
        'link': 'https://sun9-55.userapi.com/impg/IdfjJwkECr8ktZZvTo1q_iEhVnazj-jFmKcAww/gqchy3erCbM.jpg?size=300x300&quality=96&sign=7b6ee8d1e03b9aeb22a077cf18198938&type=album'
        },
    'Cap': {
        'label': 9,
        'link': 'https://sun9-56.userapi.com/impg/tYeVEQk77KFq9zfKjAWIq45KSwtgLn8L0PZbeQ/M9cP5Hzw4eQ.jpg?size=300x300&quality=96&sign=d302eccce2e3238e204fa118219ab875&type=album'
        },
}


def image_to_numpy(image):

    '''
    Convert image to numpy array.

    Args:
        image: PIL.Image. Image for converting.

    Returns:
        Numpy array with shape (height, width, channels).
    '''

    w, h = image.size
    image_data = np.array(image.getdata())
    channels = image_data.shape[-1]
    return np.reshape(image_data, (h, w, channels))


def central_crop(image, size):

    '''
    Apply central crop for image to size.

    Args:
        image: PIL.Image object.
        size: tuple. Size of target image.

    Returns:
        PIL.Image object.
    '''

    w, h = image.size
    target_h, target_w = size
    left = int(w/2 - target_w/2)
    right = left + target_w
    upper = int(h/2 - target_h/2)
    lower = upper + target_h
    return image.crop((left, upper, right, lower))


def load_image_from_link(link, format='RGB', target_size=None):
    '''
    Load image from link with its's original size in RGB format by default.

    Args:
        path: str. Link to image.
        format: str. Formats to attempt to load the file in. Default 'RGB'.
        target_size: tuple. If not None, resize image to target size. Default None. 

    Returns:
        PIL.Image object.
    '''

    response = requests.get(link)
    image = Image.open(BytesIO(response.content)).convert(format)
    if target_size:
        image = image.resize(target_size)
    return image


def load_image_from_path(path, format='RGB', target_size=None):

    '''
    Load image from path with its's original size in RGB format by default.

    Args:
        path: string. Local path to image.
        format: string. Formats to attempt to load the file in. Default 'RGB'.
        target_size: tuple. If not None, resize image to target size. Default None. 

    Returns:
        PIL.Image object.
    '''

    image = Image.open(path).convert(format)
    if target_size is not None:
        image = image.resize(target_size)
    return image


def random_augment_image(image, rfactor=0.14):

    '''
    Returns PIL image.

    Args:
        image: PIL.Image. Image for augmentations.
        rfactor: float. If random values < rfactor then function returns non-augmented image.

    Returns:
        PIL.Image object.

    '''

    def _adjust_random_perspective(image):
    
        def _find_coeffs(pa, pb):
            matrix = []
            for p1, p2 in zip(pa, pb):
                matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
                matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

            A = np.matrix(matrix, dtype=np.float)
            B = np.array(pb).reshape(8)
            res = np.linalg.solve(A, B)
            return np.reshape(res, 8)

        w, h = image.size
        current_coordinates = np.array([
            [0, 0],
            [0, w],
            [h, w],
            [h, 0],
        ])
        deltas = np.random.randint(size=8, low=0, high=int(0.25*np.max([w, h])))
        target_coordinates = np.array([
            [0+deltas[0], 0+deltas[1]],
            [0+deltas[2], w-deltas[3]],
            [h-deltas[4], w-deltas[5]],
            [h-deltas[6], 0+deltas[7]],
        ])
        
        coeffs = _find_coeffs(current_coordinates, target_coordinates)
        result_image = image.transform(image.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        return result_image
    

    def _adjust_random_sharpness(image, low=-3.0, high=5.0):
        factor = np.random.uniform(low, high)
        sharpness = ImageEnhance.Sharpness(image)
        result_image = sharpness.enhance(factor)
        return result_image


    def _adjust_random_brightness(image, low=0.7, high=1.3):
        factor = np.random.uniform(low, high)
        sharpness = ImageEnhance.Brightness(image)
        result_image = sharpness.enhance(factor)
        return result_image


    def _adjust_random_contrast(image, low=0.8, high=1.2):
        factor = np.random.uniform(low, high)
        sharpness = ImageEnhance.Contrast(image)
        result_image = sharpness.enhance(factor)
        return result_image


    def _adjust_random_color(image, low=0.8, high=1.2):
        factor = np.random.uniform(low, high)
        sharpness = ImageEnhance.Color(image)
        result_image = sharpness.enhance(factor)
        return result_image
    

    def _adjust_random_rotation(image, max_angle=360):
        angle = np.random.randint(low=0, high=max_angle)
        return image.rotate(angle)


    if np.random.rand() > rfactor:
        if np.random.rand() > rfactor:
            image = _adjust_random_perspective(image)
        if np.random.rand() > rfactor:
            image = _adjust_random_sharpness(image)
        if np.random.rand() > rfactor:
            image = _adjust_random_brightness(image)
        if np.random.rand() > rfactor:
            image = _adjust_random_contrast(image)
        if np.random.rand() > rfactor:
            image = _adjust_random_color(image)
        if np.random.rand() > rfactor:
            image = _adjust_random_rotation(image)
    
    return image


def get_data(counts=100):

    def _get_augmented_image(key):
        link, label = IMAGES_DATA[key]['link'], IMAGES_DATA[key]['label']
        image = load_image_from_link(link, target_size=(64, 64))
        image = random_augment_image(image)
        image = image_to_numpy(image) / 255.
        return [image, label]

    images = list()
    labels = list()
    data = list()

    keys = np.repeat(list(IMAGES_DATA.keys()), counts)
    np.random.shuffle(keys)

    with ThreadPoolExecutor() as pool:
        data = list(pool.map(_get_augmented_image, keys))

    for x, y in data:
        images.append(x)
        labels.append(y)

    return np.array(images), np.array(labels)