from django.contrib.gis.db import models
from .basic import File, Dial

class ShapeFile(File):
    file_definition = models.ForeignKey('ShapeDefinitionFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    file_thm = models.ForeignKey('ShapeTHMFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class ShapeDefinitionFile(File):
    ref_name = models.CharField(max_length=40)
    ESD_Detail_Level = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    ESD_Alternative_Texture = models.ForeignKey('AlternativeTextureDial', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    ESD_No_Visual_Obstruction = models.BooleanField(null=True, blank=True, default=None)
    ESD_Software_DLev = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    ESD_SubObj = models.BooleanField(null=True, blank=True, default=None)

    bb_min = models.PointField(null=True, blank=True, default=None, dim=3)
    bb_max = models.PointField(null=True, blank=True, default=None, dim=3)

    @property
    def ESD_Bounding_Box(self):
        return (self.bb_min, self.bb_max)

class ShapeTHMFile(File):
    pass

class ImageFile(File):
    shape_file = models.ManyToManyField('ShapeFile', related_name='images', null=True, blank=True, default=None)
    texture_file = models.ForeignKey('TextureFile', on_delete=models.CASCADE)

class AlternativeTextureDial(Dial):
    pass