from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class DeerFile(File):
    file_name = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    distance = models.DecimalField()
    speed = models.DecimalField()
    idle_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    idle_key2 = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_left = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_right = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    success_scarper_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)