from django.contrib.gis.db import models
from basic import File

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