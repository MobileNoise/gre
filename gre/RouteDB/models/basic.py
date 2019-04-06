from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Project(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField(null=True, blank=True, default=None)
    main_global = models.ForeignKey('Global', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    main_track = models.ForeignKey('Track', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    main_sound = models.ForeignKey('Sound', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    track_b = models.ForeignKey('Track_B', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    track_k = models.ForeignKey('Track_K', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    track_t = models.ForeignKey('Track_K', on_delete=models.SET_NULL, null=True, blank=True, default=None)



class Folder(models.Model): # Abstract
    name = models.TextField(unique=True)
    path = models.FilePathField(allow_files=False, allow_folders=True)

    class Meta:
        abstract = True

class Global(Folder):
    pass

class Track(Folder):
    main_world = models.ForeignKey('World', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Sound(Folder):
    pass

class Track_B(Folder):
    pass

class Track_K(Folder):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class World(Folder):
    pass

class DataFile(models.Model): #Abstract
    file_name = models.FilePathField(unique=True)
    folder = models.ForeignKey('Folder', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        abstract = True

class File(DataFile): #Abstract
    key_name = models.CharField(max_length=40)

    class Meta:
        abstract = True

class TextureFile(DataFile):
    pass

class SmsFile(DataFile):
    pass

class SimpleArrayFile(File): #Abstract
    
    class Meta:
        abstract = True

class Dial(models.Model): #Abstract
    key = models.PositiveSmallIntegerField(unique=True)
    val = models.CharField(max_length=40, null=True, blank=True, default=None)

    class Meta:
        abstract = True

class NamedDial(models.Model): #Abstract
    key = models.CharField(max_length=40)
    val = models.CharField(max_length=40, null=True, blank=True, default=None)

    class Meta:
        abstract = True

class SpeedType(Dial):
    pass

class Colour(models.Model):
    red = models.PositiveSmallIntegerField()
    green = models.PositiveSmallIntegerField()
    blue = models.PositiveSmallIntegerField()
    brightness = models.PositiveSmallIntegerField(null=True, blank=True, default=None)

class Position(models.PointField):
    pass

class QDirection(models.Model):
    world_item = models.ForeignKey('WorldItem', on_delete=models.CASCADE, null=True, blank=True, default=None)
    x = models.DecimalField()
    y = models.DecimalField()
    z = models.DecimalField()
    w = models.DecimalField()

class Speed(models.Model):
    speed_type = models.ForeignKey('SpeedType', on_delete=models.CASCADE)
    speed_value = models.DecimalField()

class DecimalTuple(models.Model):
    first = models.DecimalField()
    second = models.DecimalField()

class ArrayEntry(models.Model): #Abstract
    name = models.CharField(max_length=40, null=True, blank=True, default=None)

    class Meta:
        abstract = True

class OrderedArrayEntry(ArrayEntry): #Abstract
    in_id = models.PositiveIntegerField()

    class Meta:
        abstract = True