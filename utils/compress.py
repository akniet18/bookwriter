from PIL import Image, ImageFile
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import sys
from django.core.files.base import ContentFile
import base64

ImageFile.LOAD_TRUNCATED_IMAGES = True

def compress_image(uploaded_image, size):
    temp = Image.open(uploaded_image)
    temp.thumbnail(size, Image.ANTIALIAS)
    outputIOStream = io.BytesIO()
    temp = temp.convert('RGB')
    temp.save(outputIOStream, format='JPEG', quality=80)
    outputIOStream.seek(0)
    uploaded_image = InMemoryUploadedFile(outputIOStream, 'ImageField', '%s.jpg', uploaded_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIOStream), None)
    return uploaded_image


def base64img(imgn, name):
    im = (imgn.replace(' ', '+')+"===")
    data = ContentFile(base64.b64decode(im), name=str(name)+'.jpg')
    return data