import os
from django import forms
from .models import Document
from .Utils.createMaiMLFile import MaimlUtil

############################################
##  Form class -   File Upload用
############################################
class DocumentForm(forms.ModelForm):
    protocolmodel = forms.CharField
    class Meta:
        model = Document
        fields = ('description', 'upload_maiml', 'upload_tiff', )
        widgets = {
            'description' : forms.TextInput(attrs={'placeholder': 'use for system'}),
            }

############################################
##  Form class -   TIFF File Upload用
############################################
class TiffUploadForm(forms.Form):
    upload_maiml_id = forms.UUIDField(required=True, widget=forms.TextInput(
            attrs={ 
                'disabled': 'disabled', 
            }
        ))
    ## petri-net graph data
    #petri_data = forms.JSONField(required=True)
    petri_data = forms.JSONField()
    upload_tiff = forms.FileField()

    def save(self,upload_maiml_id_data):
        path = MaimlUtil.get_osfilepath(upload_maiml_id_data, 1)
        os.makedirs(path, exist_ok=True)
        upload_file = self.files['upload_tiff']
        savepath = os.path.join(path, upload_file.name)
        savefile = open(os.path.join(path, upload_file.name),'wb+')
        for chunk in upload_file.chunks():
            savefile.write(chunk)
        return savepath

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

###############################################
##   Form class -  File Update用
###############################################
class MaimlUpdateForm(forms.Form):
    # 更新するMaiMLファイルのUUID
    upload_maiml_id = forms.UUIDField(required=True, widget=forms.TextInput(
            attrs={ 
                'disabled': 'disabled', 
            }
        ))
    # maimlデータ
    maiml_dict = forms.JSONField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)