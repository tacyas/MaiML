from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ListDL, DocumentUpload, DocumentUpdate

app_name = 'createapp'

urlpatterns = [
    path("", ListDL.displayTop, name='top'), 
    path("top/", ListDL.displayTop, name='top'), 
    path("download/<slug:upload_maiml_id>/", ListDL.download_zip, name='zipdownload'),  # list UI --> zip download
    path("download/", ListDL.download_zip, name='zipdownload'),  # list UI --> zip download
    path("upload/", DocumentUpload.modelform_upload, name='fileupload'),  # file upload class --> input data UI
    path("update/", DocumentUpdate.update_maiml, name='updateform'),  # input data UI -->  update data class 
    path("fromidupload/<slug:upload_maiml_id>/", DocumentUpload.upload_tiff, name='fromidupload'),  # list UI --> file upload UI
    path("fromidupload/", DocumentUpload.upload_tiff, name='fromidupload'),  # list UI --> file upload UI
] #+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)