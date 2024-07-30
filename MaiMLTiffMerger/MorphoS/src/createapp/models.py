from django.db import models
import os
from .Utils.staticClass import staticVal

########################
###  master class
########################
## Maiml type
class Maimltype(models.Model):
    model_type = models.IntegerField(verbose_name="Model type", default=0) 
    type_name = models.TextField(verbose_name="Model Name", blank=False)
    # protocolFileRootType/maimlRootType
    def __str__(self):
        return str(self.type_name)

#######################################
## util method - create path of files
#######################################
def path_branch(instance, filename):
    root_ext_pair = os.path.splitext(filename)  # ファイルパス＋ファイル名と拡張子を分割
    #print(instance.upload_maiml_id)
    newfileid = instance.upload_maiml_id
    # input or outputディレクトリ変更
    if root_ext_pair[0].split()[-1] == '.outputdocs':
        dir = f'outputdocs/{newfileid}'
    else:
        dir = f'inputdocs/{newfileid}'
    # PDF・CSV・その他でパスを変更する場合
    if root_ext_pair[1] == '.maiml':
        path = os.path.join(dir+'/MaiML/', filename)
    elif root_ext_pair[1] == '.xml':
        path = os.path.join(dir+'/XML/', filename)
    else:
        path = os.path.join(dir+'/Others/', filename)
    return path


#################################################
##  Model class -save maiml and tiff files 
#################################################
class Document(models.Model):
    upload_maiml_id = models.UUIDField(primary_key=True, default=staticVal.upload_maiml_id)
    description = models.CharField(max_length=255, blank=True)
    # File repository PATH
    upload_maiml = models.FileField(upload_to = path_branch)
    upload_tiff = models.FileField(upload_to = path_branch, blank=True)
    # uploaded date
    register_at = models.DateTimeField(auto_now_add=True)

    MaiMLtype = models.ForeignKey(
        Maimltype,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="protocolFileRootType")

    ''' for admin '''
    def __str__(self):
        return str(self.upload_maiml_id)

