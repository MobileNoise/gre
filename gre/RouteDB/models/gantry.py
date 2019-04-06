from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class GantryFile(File):
    pass

class GantrySet(models.Model):
    gantry_file = models.ForeignKey('GantryFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    style = models.ForeignKey('GantryStyle', on_delete=models.CASCADE)
    separation_dist = models.IntegerField()

class GantryStyle(NamedDial):
    pass

class GantryTableEntry(models.Model):
    gantry_set = models.ForeignKey('GantrySet', on_delete=models.CASCADE)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    distance = models.IntegerField()