# -*- coding: utf-8 -*-

__author__ = 'Jochen Breuer <brejoc@gmail.com>'
__copyright__ = 'Jochen Breuer <brejoc@gmail.com>'
__license__ = 'BSD 3-Clause License'


import os
import requests
import hashlib
import logging

from base64 import urlsafe_b64decode
from PIL import Image as Pil
from StringIO import StringIO

from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

from image_sizr.models import Image

# Get an instance of a logger
logger = logging.getLogger(__name__)

DEBUG = settings.DEBUG

class MissingContentTypeError(Exception):
    """\
    We need our own Error, so we can catch it.
    """
    pass

class ContentTypeError(Exception):
    """\
    We need our own Error, so we can catch it.
    """
    pass


@cache_page(settings.CACHE_TIME)
def resize(request, url, x, y):
    """\
    Add desciption
    """
    # todo: check parameter
    # todo: also add parameter for quality and file type
    #url = urlsafe_b64decode(request.GET.get('url', None))
    url = urlsafe_b64decode(str(url))
    #new_x = request.GET.get('x', None)
    #new_y = request.GET.get('y', None)
    new_x = int(x)
    new_y = int(y)
    r = requests.head(url)

    if DEBUG is True:
        logger.info(r.headers)

    # create url hash and look it up in database
    url_m = hashlib.md5()
    url_m.update(url)
    img_url_hash = url_m.hexdigest()

    if DEBUG is True:
        logger.info("image url: %s" % url)
        logger.info("image url hash: %s" % img_url_hash)

    images = Image.objects.filter(url_hash=img_url_hash)
    db_image = None
    if images:
        if len(images) > 1:
            logger.warning("Found too many images. Deleting all and starting over.")
            # todo: something is wrong here. there should be only one. delete all and start over
            pass
        else:
            logger.info("Found image.")
            print("Found image.")
            db_image = images[0]
            if not os.path.exists(os.path.join(db_image.path_to_images(), "%s_%sx%s.%s" % \
                    (db_image.url_hash, new_x, new_y, db_image.suffix))):
                print "resized image not found"
                _create_thumb(db_image, new_x, new_y)
    else:
        db_image = _fetch_image(url, img_url_hash, r)
        _create_thumb(db_image, new_x, new_y)

    return redirect("http://localhost:8000/bucket/%(bucket)s/%(url_hash)s/%(img_hash)s/%(url_hash)s_%(x)sx%(y)s.%(suffix)s" % \
                    {
                        "bucket": db_image.bucket,
                        "url_hash": db_image.url_hash,
                        "img_hash": db_image.img_hash,
                        "x": new_x,
                        "y": new_y,
                        "suffix": db_image.suffix,
                    })

def _fetch_image(url, img_url_hash, r):
    """\
    add description!!!
    """

    content_types = settings.CONTENT_TYPES.keys()

    if "content-type" not in r.headers:
        raise MissingContentTypeError("content-type is missing")
    if r.headers["content-type"] not in content_types:
        raise ContentTypeError("content-type '%s' is not in list" % \
            r.headers["content-type"])


    # etag or hash
    img_hash = None
    if r.headers.has_key("etag"):
        img_hash = r.headers["etag"]
        # some servers (like the one play! uses) include quotation marks
        img_hash = img_hash.strip('"')
    elif r.headers.has_key("last-modified"):
        m = hashlib.md5()
        m.update(r.headers["last-modified"])
        # also use content-length if it exists
        if r.headers.has_key("content-length"):
            m.update(str(r.headers.has_key("content-length")))
        img_hash = m.hexdigest()


    if DEBUG is True:
        logger.info("loading image…")
        logger.info("image hash: %s" % img_hash)

    db_image = Image(url=url,
                     url_hash=img_url_hash,
                     img_hash=img_hash,
                     mime_type=r.headers["content-type"],
                     suffix=settings.CONTENT_TYPES[r.headers["content-type"]])
    db_image.save()

    r = requests.get(url)
    image = Pil.open(StringIO(r.content))
    logger.info(image)
    image.save(os.path.join(db_image.path_to_images(), img_hash + "." + db_image.suffix),
               image.format,
               quality=90)
    logger.info("saved image to %s" % os.path.join(db_image.path_to_images(), img_hash))
    return db_image

def _create_thumb(db_image, x, y):
    """\
    add description!!!
    """
    original_image = db_image.path_to_original_image()
    resize_filename = os.path.join(db_image.path_to_images(), "%s_%sx%s.%s" % \
                                            (db_image.url_hash, x, y, db_image.suffix))

    image = Pil.open(original_image)
    width, height = image.size
    print "original size: %s:%s" % (width, height)

    if height > y:
        # portrait images get blurry otherwise
        print "height > y"
        y = height
    new_size = int(x), int(y)
    image.thumbnail(new_size, Pil.ANTIALIAS)
    print "new width and height: %sx%s" % (x, y)
    try:
        image.save(resize_filename, image.format, quality=90, optimize=1)
    except:
        image.save(resize_filename, image.format, quality=90)