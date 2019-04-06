from django.contrib.gis.db import models
from basic import File, NamedDial, Dial, ArrayEntry, OrderedArrayEntry, Position

class TrackDataBaseFile(File):
    serial = models.IntegerField()
	
class TrackNodeType(Dial):
    pass
	
class TrackNode(OrderedArrayEntry):
    file_name = models.ForeignKey('TrackDataBaseFile', on_delete=models.CASCADE)
    node_type = models.ForeignKey('TrackNodeType', on_delete=models.CASCADE)
		
class TrPin(models.Model): # Abstract
    track_node = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
    world_tile = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
    world_uid = models.IntegerField() # TODO use PolymorphicModel
    is_opposite_end = models.BooleanField()	

    class Meta:
        abstract = True
		
class TrPinBegin(TrPin):
	pass	
	
class TrPinEnd(TrPin):
	pass
		
class TrUidSection(models.Model):
	track_node = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
	world_tile = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
	world_uid = models.IntegerField() # TODO use PolymorphicModel
	world_tile_2 = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
	position = models.PointField(dim=3)
	rotation = models.PointField(dim=3)
	
class TrVectorSection(TrUidSection):
	track_section = models.ForeignKey('G_TrackSection', on_delete=models.CASCADE)
	track_shape = models.ForeignKey('G_TrackShape', on_delete=models.CASCADE)
	flag_1 = models.PositiveSmallIntegerField()
	flag_2 = models.PositiveSmallIntegerField()
	flag_2 = models.CharField(max_length=2)
	
class TrItemRef(models.Model):
	track_section = models.ForeignKey('TrVectorSection', on_delete=models.SET_NULL, null=True, blank=True, default=None)
	track_item_id = models.IntegerField() # TODO use PolymorphicModel
	
class TrackItem(models.Model): # Abstract?
    tritem_id = models.IntegerField() # TODO use PolymorphicModel
    sdata_1 = models.DecimalField(null=True, blank=True, default=None)
    sdata_2 = models.CharField(max_length=8, null=True, blank=True, default=None)
    rdata_1 = models.PointField(dim=3, null=True, blank=True, default=None)
    rdata_2 = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
    pdata_1 = models.PointField(dim=3, null=True, blank=True, default=None)
    pdata_2 = models.ForeignKey('WorldFile', on_delete=models.CASCADE, null=True, blank=True, default=None)
	
    class Meta:
        abstract = True

class SidingItem(TrackItem):
    end_flag = models.BooleanField()
    other = models.ForeignKey('SidingItem', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    name = models.CharField(max_length=40, null=True, blank=True, default=None)

class PlatformItem(SidingItem):
    other = models.ForeignKey('PlatformItem', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    platform_min_waiting_time = models.PositiveSmallIntegerField()
    platform_num_passangers_waiting = models.PositiveSmallIntegerField()

class Station(models.Model):
    name = models.CharField(max_length=40)

class SpeedPostItem(TrackItem):
    is_freight = models.BooleanField()
    is_limit = models.BooleanField()
    is_milepost = models.BooleanField()
    is_mph = models.BooleanField()
    is_passanger = models.BooleanField()
    is_resume = models.BooleanField()
    is_warning = models.BooleanField()
    display_number = models.IntegerField()
    reverse_direction = models.IntegerField()
    show_dot = models.BooleanField()
    show_number = models.BooleanField()
    sig_obj = models.ForeignKey('SignalItem', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    speed_indicator = models.DecimalField()

class SignalItem(TrackItem):
    junction_flag = models.ForeignKey('SignalTypeFlag', on_delete=models.CASCADE)
    way_facing = models.BooleanField()
    flag_1 = models.DecimalField()
    signal_type = models.ForeignKey('SignalType', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class TrSignalDir(OrderedArrayEntry):
    signal_item = models.ForeignKey('SignalItem', on_delete=models.CASCADE)
    track_node = models.ForeignKey('TrackNode', on_delete=models.CASCADE)
    sd_1 = models.PositiveSmallIntegerField()
    link_lr_patch = models.PositiveSmallIntegerField()
    sd_3 = models.PositiveSmallIntegerField()

class SignalTypeFlag(NamedDial):
    pass

class LevelCrItem(TrackItem):
    pass

class PickupItem(TrackItem):
    content = models.DecimalField()
    pickup_type = models.ForeignKey('PickupType', on_delete=models.CASCADE)

class PickupType(NamedDial):
    pass

class HazzardItem(TrackItem):
    pass

class EmptyItem(OrderedArrayEntry):
    pass

class SoundRegionItem(TrackItem):
    sr_data_1 = models.PositiveSmallIntegerField()
    sr_data_2 = models.PositiveSmallIntegerField()
    sr_data_3 = models.DecimalField()