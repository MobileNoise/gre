from django.contrib.gis.db import models
from basic import File, NamedDial, ArrayEntry, OrderedArrayEntry, Position

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