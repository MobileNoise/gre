from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class TelePoleFile(File):
    pass

class TPoleConfig(models.Model):
    telepole_file = models.ForeignKey('TelePoleFile', on_delete=models.CASCADE)
    file_name = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    shadow = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    separation = models.DecimalField()

class Wire(models.Model):
    tpole_config = models.ForeignKey('TPoleConfig', on_delete=models.CASCADE)
    start_offset = models.PointField(dim=3)