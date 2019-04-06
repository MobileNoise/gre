from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class R_TrackSectionFile(File):
    pass

class R_TrackSection(OrderedArrayEntry):
    track_section_file = models.ForeignKey('R_TrackSectionFile', on_delete=models.CASCADE)
    section_curve = models.PositiveSmallIntegerField()
    param_1 = models.DecimalField()
    param_2 = models.DecimalField()
    track_path = models.ForeignKey('R_TrackPath', on_delete=models.CASCADE)
    
class R_TrackPath(OrderedArrayEntry):
    track_section_file = models.ForeignKey('R_TrackSection_File', on_delete=models.CASCADE)