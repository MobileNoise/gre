from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class SSourceFile(File):
    pass

class SoundSource(models.Model):
    ssource_file = models.ForeignKey('SSourceFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    file_name = models.ForeignKey('SmsFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)