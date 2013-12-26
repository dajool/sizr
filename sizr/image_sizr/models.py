# -*- coding: utf-8 -*-

__author__ = 'Jochen Breuer <brejoc@gmail.com>'
__copyright__ = 'Jochen Breuer <brejoc@gmail.com>'
__license__ = 'BSD 3-Clause License'

import os
import random
import string
import logging

from shutil import rmtree

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _


# returns the absolute path to this file extended by the parameter
abs_path = lambda parameter: os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    parameter)

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Image(models.Model):
    """\
    …
    """

    url_hash = models.CharField(max_length=32, primary_key=True)
    url = models.URLField()
    bucket = models.CharField(max_length=2, blank=True, null=True)
    suffix = models.CharField(max_length=8)
    # regarding the length of the mime type field:
    # http://tools.ietf.org/html/rfc4288#section-4.2  |  127 + 1 + 127 = 255
    mime_type = models.CharField(max_length=255)
    img_hash = models.CharField(max_length=255,
                                help_text=_(u"""This is either the etag or a md5sum
                                generated from last-modified and content-length"""))

    class Meta:
        verbose_name = _(u"Image")
        verbose_name_plural = _(u"Images")

    def __unicode__(self):
        return self.url_hash

    def save(self, *args, **kwargs):
        """\
        Randomly choose bucket and save.
        """
        model = self.__class__
        if self.bucket is None or self.bucket == "":
            self.bucket = ''.join(random.choice(string.digits) for x in range(2))
        mkdir_p(self.path_to_images())
        return super(Image, self).save(*args, **kwargs)

    def path_to_images(self):
        return os.path.join(settings.BUCKET_ROOT, self.bucket, self.url_hash, self.img_hash)

    def path_to_original_image(self):
        return os.path.join(self.path_to_images(), self.img_hash + '.' + self.suffix)


@receiver(pre_delete)
def del_images(sender, instance, **kwargs):
    """\
    Also delete images from Bucket when dataset is deleted.
    """
    if sender==Image:
        try:
            rmtree(instance.path_to_images())
        except:
            logger.error("Couldn't remove bucket: %s" % instance.path_to_images())


def mkdir_p(path):
    if not os.path.isdir(path):
        os.makedirs(path)