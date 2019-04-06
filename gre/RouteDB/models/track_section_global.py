
from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

class G_TrackSectionFile(File):
    pass

class G_TrackSectionInfo(models.Model):
    prev_idx = models.PositiveIntegerField()
    section_file = models.ForeignKey('G_TrackSectionFile', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, default=None)

class G_TrackSectionEntry(OrderedArrayEntry): # Abstract
    section_file = models.ForeignKey('G_TrackSectionFile', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class G_TrackSection(G_TrackSectionEntry):
    gauge = models.DecimalField()
    length = models.DecimalField()
    radius = models.DecimalField()
    angle = models.DecimalField()

    @property
    def section_size(self):
        return (self.gauge, self.length)

    @property
    def section_curve(self):
        return (self.radius, self.angle)

## Track Shapes ##

class G_TrackShape(G_TrackSectionEntry):
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    num_paths = models.PositiveSmallIntegerField()
    main_route = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    clearance_dist = models.DecimalField()

class G_TrackShapeSection(models.Model): # Abstract
    track_shape = models.ForeignKey('G_TrackShape', on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

class G_SectionIdx(G_TrackShapeSection):
    path_start_offset = models.PointField(null=True, blank=True, default=None, dim=3)
    path_direction = models.DecimalField()
    section_idx = models.ManyToManyField('G_TrackSection', related_name='g_track_shape_sections')
    tunnel_shape = models.BooleanField(null=True, blank=True, default=None)
    road_shape = models.BooleanField(null=True, blank=True, default=None)

class G_SectionSkew(G_TrackShapeSection):
    preceding_path_direction = models.DecimalField()

class G_XoverPt(G_TrackShapeSection):
    pt = models.PointField(null=True, blank=True, default=None, dim=3)