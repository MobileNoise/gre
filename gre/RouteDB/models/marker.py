from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class MarkerFile(File):
    pass

class Marker(models.Model):
    pos = Position()
    name = models.CharField(max_length=40, null=True, blank=True, default=None)
    flag = models.PositiveSmallIntegerField()