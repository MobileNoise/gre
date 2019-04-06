from django.contrib.gis.db import models
from basic import SimpleArrayFile, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class ForestFile(SimpleArrayFile):
    pass

class F_Forest(models.Model):
    forest_file = models.ForeignKey('ForestFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    width = models.DecimalField()
    height = models.DecimalField()
    min_scale = models.DecimalField()
    max_scale = models.DecimalField()

    @property
    def area(self):
        return (self.width, self.height)

    @property
    def scale_range(self):
        return (self.min_scale, self.max_scale)