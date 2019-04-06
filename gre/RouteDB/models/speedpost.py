from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class SpeedPostFile(File):
    speed_warning_sign_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    restricted_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    end_restricted_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)

class SpeedPostSet(models.Model):
    speedpost_file = models.ForeignKey('SpeedPostFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    speed_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    speed_text_size = models.PointField(null=True, blank=True, default=None, dim=3)
    milepost_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    milepost_text_size = models.PointField(null=True, blank=True, default=None, dim=3)

class PostShape(models.Model): #Abstract
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class SpeedPostParam(models.Model): #Abstract
    text_start_offset = models.PointField(dim=3)
    text_orientation = models.DecimalField()

    class Meta:
        abstract = True

class SpeedSignShape(PostShape):
    pass

class SpeedSignParam(SpeedPostParam):
    speed_sign_shape = models.ForeignKey('SpeedSignShape', on_delete=models.CASCADE)

class MilepostShape(PostShape):
    pass

class MilepostParam(SpeedPostParam):
    milepost_shape = models.ForeignKey('MilepostShape', on_delete=models.CASCADE)