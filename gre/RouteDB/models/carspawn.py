from django.contrib.gis.db import models
from basic import SimpleArrayFile, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class CarSpawnFile(SimpleArrayFile):
    pass

class CarSpawnerItem(models.Model):
    spawner_file = models.ForeignKey('CarSpawnerFile', on_delete=models.CASCADE)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    separation_dist = models.IntegerField()