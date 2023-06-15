from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SkinDiseasesClassification(models.Model):
    skin_image           = models.ImageField(upload_to='skin_process/')
    skin_classification  = models.CharField(_("skin En Classification") ,max_length=225 )
    skin_classification_ar  = models.CharField(_("skin Ar Classification") ,max_length=225 ,blank = True)
    skin_accuracy        = models.CharField(_('skin_accuracy') ,max_length=225)
    
    class Meta:
        verbose_name_plural = _('Skin Diseases Classification')
        
    def __str__(self):
        return f"Image ( {self.id} ) , it classify to ( {self.skin_classification} ) , with accuracy ( {self.skin_accuracy} % )"

class SkinDiseasesInfo(models.Model):
    title      = models.CharField(_("En Title") ,max_length=255)
    definition = models.TextField(_("En definition"))
    causes     = models.TextField(_("En causes"))
    treatment  = models.TextField(_("En treatment"))
    
    title_ar      = models.CharField(_("Ar Title") ,max_length=255 ,blank = True)
    definition_ar = models.TextField(_("Ar definition") ,blank = True)
    causes_ar     = models.TextField(_("Ar causes") ,blank = True)
    treatment_ar  = models.TextField(_("Ar treatment") ,blank = True)
    
    class Meta:
        verbose_name_plural = _('Skin Diseases Info')
        
    def __str__(self):
        return self.title
