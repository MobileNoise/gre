from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.

### BASIC ###

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

### SHAPE FILE ###

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

### SIGNAL CONFIG ###

class SignalConfigFile(File):
    pass

class SignalConfigArrayEntry(ArrayEntry):  # Abstract
    sigcfg = models.ForeignKey('SignalConfigFile', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class SignalConfigOrderedArrayEntry(OrderedArrayEntry): # Abstract
    sigcfg = models.ForeignKey('SignalConfigFile', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class LightTexture(SignalConfigArrayEntry):
    img = models.ForeignKey('ImageFile', on_delete=models.CASCADE)
    draw_param_1 = models.DecimalField()
    draw_param_2 = models.DecimalField()
    draw_param_3 = models.DecimalField()
    draw_param_4 = models.DecimalField()

class LightTab(SignalConfigArrayEntry):
    colour = models.ForeignKey('Colour', on_delete=models.CASCADE)
    
class SignalType(SignalConfigArrayEntry):
    fn_type = models.ForeignKey('SignalFnType', on_delete=models.CASCADE)
    light_tex = models.ForeignKey('LightTexture', on_delete=models.CASCADE)
    flash_duration_on = models.DecimalField()
    flash_duration_off = models.DecimalField()
    num_clear_ahead = models.PositiveSmallIntegerField()

class SignalTypeArrayEntry(OrderedArrayEntry): # Abstract
    sig_type = models.ForeignKey('SignalType', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class SignalLight(SignalTypeArrayEntry):
    position = Position(dim=3)
    radius = models.DecimalField()

class SignalDrawState(SignalTypeArrayEntry):
    pass

class SignalDrawLight(OrderedArrayEntry):
    sig_draw_state = models.ForeignKey('SignalDrawState', on_delete=models.CASCADE)
    signal_light = models.ForeignKey('SignalLight', on_delete=models.CASCADE)
    signal_flag = models.ForeignKey('SignalFlag', on_delete=models.CASCADE, null=True, blank=True, default=None)

class SignalAspect(SignalTypeArrayEntry):
    aspect_type = models.ForeignKey('SignalAspectType', on_delete=models.CASCADE)
    draw_state = models.ForeignKey('SignalDrawState', on_delete=models.CASCADE)
    speed = models.ForeignKey('Speed', on_delete=models.CASCADE, null=True, blank=True, default=None)
    signal_flag = models.ForeignKey('SignalFlag', on_delete=models.CASCADE, null=True, blank=True, default=None)

class SignalShape(SignalConfigArrayEntry):
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class SignalSubObject(OrderedArrayEntry):
    signal_shape = models.ForeignKey('SignalShape', on_delete=models.CASCADE)
    desc = models.CharField(max_length=40, null=True, blank=True, default=None)
    signal_subtype = models.ForeignKey('SignalSubtype', on_delete=models.CASCADE)
    signal_sub_s_type = models.ForeignKey('SignalType', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class SubJnLinkIf(models.Model):
    signal_shape = models.ForeignKey('SignalShape', on_delete=models.CASCADE)
    signal_source_subobject = models.ForeignKey('SignalSubObject', on_delete=models.CASCADE)
    signal_target_subobject = models.ForeignKey('SignalSubObject', on_delete=models.CASCADE)

class SignalGroup(SignalConfigOrderedArrayEntry):
    pass

class SignalGroupEntry(OrderedArrayEntry):
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    
class SignalGantrySet(SignalConfigOrderedArrayEntry):
    pass

class SignalGantryInfo(models.Model):
    gantry_set = models.ForeignKey('SignalGantrySet', on_delete=models.CASCADE)

    bb_min = models.PointField(null=True, blank=True, default=None, dim=3)
    bb_max = models.PointField(null=True, blank=True, default=None, dim=3)

    @property
    def gantry_size(self):
        return (self.bb_min, self.bb_max)

class SignalFnType(NamedDial):
    pass

class SignalFlag(NamedDial):
    pass

class SignalAspectType(NamedDial):
    pass

class SignalSubType(NamedDial):
    pass

### SIGNAL SCRIPT ###

class SignalScriptFile(File):
    pass

class Script(models.Model): # Abstract
    name = models.CharField(max_length=40)
    text = models.TextField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

class SignalScript(Script):
    script_file = models.ForeignKey('SignalScriptFile', on_delete=models.CASCADE)
   
class SignalScriptsInSignalConfig(models.Model):
    script_file = models.ForeignKey('SignalScriptFile', on_delete=models.CASCADE)
    config_file = models.ForeignKey('SignalConfigFile', on_delete=models.CASCADE)

### GLOBAL TRACK SECTION ###

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

### ROUTE TRACK SECTION ###

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


### CARSPAWN ###

class CarSpawnFile(SimpleArrayFile):
    pass

class CarSpawnerItem(models.Model):
    spawner_file = models.ForeignKey('CarSpawnerFile', on_delete=models.CASCADE)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    separation_dist = models.IntegerField()

### FOREST ###

class ForestFile(SimpleArrayFile):
    pass

class F_Forest(models.Model):
    forest_file = models.ForeignKey('ForestFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    width = models.DecimalField()
    height = models.DecimalField()
    min_scale = models.DecimalField()
    max_scale = models.DecimalField()

    @property
    def area(self):
        return (self.width, self.height)

    @property
    def scale_range(self):
        return (self.min_scale, self.max_scale)

### GANTRY ###

class GantryFile(File):
    pass

class GantrySet(models.Model):
    gantry_file = models.ForeignKey('GantryFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    style = models.ForeignKey('GantryStyle', on_delete=models.CASCADE)
    separation_dist = models.IntegerField()

class GantryStyle(NamedDial):
    pass

class GantryTableEntry(models.Model):
    gantry_set = models.ForeignKey('GantrySet', on_delete=models.CASCADE)
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    distance = models.IntegerField()

### SPEEDPOST ###

class SpeedPostFile(File):
    speed_warning_sign_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    restricted_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    end_restricted_shape = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)

class SpeedPostSet(models.Model):
    speedpost_file = models.ForeignKey('SpeedPostFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    speed_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    speed_text_size = models.PointField(null=True, blank=True, default=None, dim=3)
    milepost_digit_tex = models.ForeignKey('TextureFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    milepost_text_size = models.PointField(null=True, blank=True, default=None, dim=3)

class PostShape(models.Model): #Abstract
    shape_file = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class SpeedPostParam(models.Model): #Abstract
    text_start_offset = models.PointField(dim=3)
    text_orientation = models.DecimalField()

    class Meta:
        abstract = True

class SpeedSignShape(PostShape):
    pass

class SpeedSignParam(SpeedPostParam):
    speed_sign_shape = models.ForeignKey('SpeedSignShape', on_delete=models.CASCADE)

class MilepostShape(PostShape):
    pass

class MilepostParam(SpeedPostParam):
    milepost_shape = models.ForeignKey('MilepostShape', on_delete=models.CASCADE)

### DEER ###

class DeerFile(File):
    file_name = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    distance = models.DecimalField()
    speed = models.DecimalField()
    idle_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    idle_key2 = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_left = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_right = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    success_scarper_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)

### SPOTTER ###

class SpotterFile(File):
    file_name = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    workers = models.ForeignKey('ShapeFile', on_delete=models.CASCADE)
    distance = models.DecimalField()
    speed = models.DecimalField()
    idle_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    idle_key2 = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_left = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    surprise_key_right = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)
    success_scarper_key = models.ForeignKey('DecimalTuple', on_delete=models.CASCADE)

### SOUND SOURCE ###

class SSourceFile(File):
    pass

class SoundSource(models.Model):
    ssource_file = models.ForeignKey('SSourceFile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    file_name = models.ForeignKey('SmsFile', on_delete=models.SET_NULL, null=True, blank=True, default=None)

### TELEPOLE ###

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

### WORLD FILE ###

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
    pickup_t = models.ForeignKey('PickupType', on_delete=models.CASCADE)
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


class PickupType(Dial):
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

class Hazard(WorldMaterialItem):
    hazard_item = models.ForeignKey('HazardItem', on_delete=models.CASCADE)

### TRACK DB ###

class TrackDataBaseFile(File):
    serial = models.IntegerField()
	
class TrackNodeType(Dial):
    pass
	
class TrackNode(OrderedArrayEntry):
    file_name = models.ForeignKey('TrackDataBaseFile', on_delete=models.CASCADE)
	type = models.ForeignKey('TrackNodeType', on_delete=models.CASCADE)
		
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
	sdata_1 = 
	
	class Meta:
        abstract = True

class SidingItem(TrackItem):
    pass

class PlatformItem(TrackItem):
    pass

class SpeedPostItem(TrackItem):
    pass

class SignalItem(TrackItem):
    pass

class LevelCrItem(TrackItem):
    pass

class PickupItem(TrackItem):
    pass

class HazardItem(TrackItem):
    pass

### MARKERS ###

class MarkerFile(File):
    pass