from django.db import models


class Application(models.Model):
    
    title = models.CharField(verbose_name='应用名称',max_length=32)

    def __str__(self):
        return self.title
    
    
class Api(models.Model):
    
    url = models.CharField(verbose_name='API',max_length=255)
    
    app = models.ForeignKey(verbose_name='所属应用',to='Application')

    def __str__(self):
        return self.url
