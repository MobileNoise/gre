from django.contrib.gis.db import models
from basic import File, NamedDial, Dial, ArrayEntry, OrderedArrayEntry, Position

class WorldFile(File):
    tile_x = models.IntegerField()
    tile_y = models.IntegerField()

class ViewDbSphere(OrderedArrayEntry):
    file_name = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
    parent_sphere = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
    position = Position(dim=3)
    radius = models.DecimalField()

class StaticFlag(NamedDial):
    pass

class CollideFlag(Dial):
    pass

class TrItemIdList(models.Model): # Abstract
    flag = models.PositiveSmallIntegerField()
    
    class Meta:
        abstract = True

class WorldItem(models.Model): # Abstract
    world_file = models.ForeignKey('WorldFile', on_delete=models.CASCADE)
    uid = models.IntegerField()
    static_flag = models.ForeignKey('StaticFlag', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    qdirection = models.ForeignKey('QDirection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    view_db_sphere = models.ForeignKey('ViewDbSphere', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    position = Position(dim=3, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    static_detail_level = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    collide_flag = models.ForeignKey('CollideFlag', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        unique_together = ('world_file', 'uid',)

class WorldMaterialItem(WorldItem):
    file_name = models.ForeignKey('ShapeFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class WorldTextureItem(WorldItem):
    file_name = models.ForeignKey('ImageFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Siding(WorldItem):
    siding_data = models.CharField(max_length=8)
    begin = models.ForeignKey('SidingItem', on_delete=models.CASCADE)
    beginflag = models.PositiveSmallIntegerField()
    end = models.ForeignKey('SidingItem', on_delete=models.CASCADE)
    endflag = models.PositiveSmallIntegerField()

class Platform(WorldItem):
    platform_data = models.CharField(max_length=8)
    begin = models.ForeignKey('PlatformItem', on_delete=models.CASCADE)
    beginflag = models.PositiveSmallIntegerField()
    end = models.ForeignKey('PlatformItem', on_delete=models.CASCADE)
    endflag = models.PositiveSmallIntegerField()

class CarSpawner(WorldItem):
    car_frequency = models.PositiveSmallIntegerField()
    car_av_speed = models.PositiveSmallIntegerField()
    begin = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
    beginflag = models.PositiveSmallIntegerField()
    end = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
    endflag = models.PositiveSmallIntegerField()

class TrackObj(WorldMaterialItem):
    section_idx = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
    elevation = models.DecimalField()

class Dyntrack(TrackObj):
    p1 = models.ForeignKey('R_TrackSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    p2 = models.ForeignKey('R_TrackSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    p3 = models.ForeignKey('R_TrackSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    p4 = models.ForeignKey('R_TrackSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    p5 = models.ForeignKey('R_TrackSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Speedpost(WorldMaterialItem):
    speed_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    speed_text_size = models.PointField(null=True, blank=True, default=None, dim=3)
    speed_sign_shape = models.TextField(null=True, blank=True, default=None)
    milepost_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    milepost_text_size = models.PointField(null=True, blank=True, default=None, dim=3)

class SpeedPostItemId(TrItemIdList):
    speedpost = models.ForeignKey('Speedpost', on_delete=models.CASCADE)
    speed_post_item = models.ForeignKey('SpeedPostItem', on_delete=models.CASCADE)

class Signal(WorldMaterialItem):
    signal_sub_obj = models.ForeignKey('SingalSubObj', on_delete=models.CASCADE)

class SignalSubObj(NamedDial):
    pass

class SignalUnitId(TrItemIdList):
    signal = models.ForeignKey('Signal', on_delete=models.CASCADE)
    signal_item = models.ForeignKey('SignalItem', on_delete=models.CASCADE)

class Static(WorldMaterialItem):
    pass

class LevelCr(WorldMaterialItem):
    warning_time = models.DecimalField()
    minimum_distance = models.DecimalField()
    crash_probability = models.PositiveSmallIntegerField()
    data = models.CharField(max_length=30)
    initial_timing = models.DecimalField()
    serious_timing = models.DecimalField()
    anim_timing = models.DecimalField()

    @property
    def level_cr_parameters(self):
        return (self.warning_time, self.minimum_distance)

    @property
    def level_cr_timing(self):
        return (self.initial_timing, self.serious_timing, self.anim_timing)

class LevelCrId(TrItemIdList):
    level_cr = models.ForeignKey('LevelCr', on_delete=models.CASCADE)
    level_cr_item = models.ForeignKey('LevelCrItem', on_delete=models.CASCADE)

class Transfer(WorldTextureItem):
    pass

class Pickup(WorldMaterialItem):
    max_speed = models.DecimalField()
    min_speed = models.DecimalField()
    pickup_t = models.ForeignKey('PickupTypeD', on_delete=models.CASCADE)
    infinite = models.BooleanField()
    anim_type = models.ForeignKey('PickupAnimType', on_delete=models.CASCADE)
    anim_duration = models.DecimalField()
    capacity = models.DecimalField()
    fill_rate = models.DecimalField()

    @property
    def speed_range(self):
        return (self.min_speed, self.max_speed)

    @property
    def pickup_type(self):
        return (self.pickup_t, self.infinite)

    @property
    def pickup_anim_data(self):
        return (self.anim_type, self.anim_duration)

    @property
    def pickup_capacity(self):
        return (self.capacity, self.fill_rate)


class PickupTypeD(Dial):
    pass

class PickupAnimType(Dial):
    pass

class PickupId(TrItemIdList):
    pickup = models.ForeignKey('Pickup', on_delete=models.CASCADE)
    pickup_item = models.ForeignKey('PickupItem', on_delete=models.CASCADE)

class Forest(WorldTextureItem):
    width = models.DecimalField()
    height = models.DecimalField()
    min_scale = models.DecimalField()
    max_scale = models.DecimalField()
    population = models.DecimalField()
    min_tree_size = models.DecimalField()
    max_tree_size = models.DecimalField()

    @property
    def area(self):
        return (self.width, self.height)

    @property
    def scale_range(self):
        return (self.min_scale, self.max_scale)

    @property
    def tree_size(self):
        return (self.min_tree_size, self.max_tree_size)

class Hazzard(WorldMaterialItem):
    hazard_item = models.ForeignKey('HazzardItem', on_delete=models.CASCADE)