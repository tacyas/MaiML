###################################
##  views class
###################################
import os, time, shutil, zipfile, json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from .models import Document, Maimltype
from .forms import DocumentForm, TiffUploadForm, MaimlUpdateForm

from .Utils.staticClass import staticVal, maimlelement, messagesList
from .Utils.createMaiMLFile import MaimlUtil, ReadWriteMaiML, UpdateMaiML
from .Utils.createPNML import MaimlUtilforPNML


###############################################
##    class for URI  Top
##     URL/top/  -->  top.html(file list)
###############################################
class ListDL():
    ## 登録済みのMaiMLファイルのリストを表示
    def displayTop(request):
        #Documentリストを設定
        file_list = Document.objects.all()

        return render(request, 'top.html', {'file_list': file_list})
    
    ## ZIP DOWNLOAD
    def download_zip(request, upload_maiml_id):
        docment_obj = get_object_or_404(Document, pk=upload_maiml_id)

        response = HttpResponse(content_type='application/zip')
        file_zip = zipfile.ZipFile(response, 'w')
        maiml_dirname, maiml_filename = os.path.split(docment_obj.upload_maiml.name)
        tiff_dirname, tiff_filename = os.path.split(docment_obj.upload_tiff.name)
        file_zip.writestr(maiml_filename, docment_obj.upload_maiml.file.read())
        file_zip.writestr(tiff_filename, docment_obj.upload_tiff.file.read())

        # Content-Dispositionでダウンロードの強制
        response['Content-Disposition'] = 'attachment; filename="files.zip"'

        return response

###############################################
##    class for URI  File Upload
##     URL/upload/  -->  fileupload.html  -->
###############################################
class DocumentUpload():
    ### "save uploaded files(MaiML&TIFF)" or "save upload files(MaiML) and draw pnml"
    def modelform_upload(request):
        if request.method == 'POST':
            try:
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        tiff_file_path = request.FILES['upload_tiff']
                    except KeyError:
                        form.errors.update({'':'Please select TIFF file.'})
                        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                        return render(request, 'fileupload.html', {'form': form})
                    if not request.FILES['upload_tiff'].name.split('.')[-1] == 'tif':
                        form.errors.update({'':'Please select TIFF file.'})
                        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                        return render(request, 'fileupload.html', {'form': form})
                    if not request.FILES['upload_maiml'].name.split('.')[-1] == 'maiml':
                        form.errors.update({'':'Please select MaiML file.'})
                        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                        return render(request, 'fileupload.html', {'form': form})
                    
                    try:
                        form.save()      # DB, mediaディレクトリにMaiML/Tiffファイルを保存
                    except Exception:
                        messages.add_message(request, messages.ERROR, messagesList.registrationError)
                        return render(request, 'fileupload.html', {'form':form})
                    
                    # Read MaiML data
                    document_obj = Document.objects.get(upload_maiml_id = staticVal.upload_maiml_id) # デフォルトのUUID値
                    maiml_file_path = document_obj.upload_maiml.path
                    tiff_file_path = document_obj.upload_tiff.path
                    readWriteMaiML_class = ReadWriteMaiML()
                    maimldict = readWriteMaiML_class.readFile(maiml_file_path) 

                    ### maimldictのUUIDで新規作成 
                    document_uuid = UpdateMaiML.getUUID(maimldict)
                    document_obj_new = document_obj
                    document_obj_new.upload_maiml_id = document_uuid
                    ## path変更 & ファイルのコピー
                    maimlnewpath = MaimlUtil.path_branch(document_uuid, document_obj.upload_maiml.name)
                    shutil.copy2(f'{settings.MEDIA_ROOT}/{document_obj.upload_maiml.name}', f'{settings.MEDIA_ROOT}/{maimlnewpath}')
                    tiffnewpath = MaimlUtil.path_branch(document_uuid, document_obj.upload_tiff.name)
                    shutil.copy2(f'{settings.MEDIA_ROOT}/{document_obj.upload_tiff.name}', f'{settings.MEDIA_ROOT}/{tiffnewpath}')
                    document_obj_new.upload_maiml = maimlnewpath
                    document_obj_new.upload_tiff = tiffnewpath

                    document_obj_new.MaiMLtype = Maimltype(1)
                    document_obj_new.save()
                    
                    ### デフォルトデータを更新＆削除
                    try:
                        del_maiml_name = document_obj.upload_maiml.name + 'delete'
                        del_tiff_name = document_obj.upload_tiff.name + 'delete'
                        new_data = {
                            'upload_maiml' : del_maiml_name,
                            'upload_tiff' : del_tiff_name
                        }
                        Document.objects.filter(upload_maiml_id = staticVal.upload_maiml_id).update(**new_data)
                        Document.objects.filter(upload_maiml_id = staticVal.upload_maiml_id).delete()
                        
                        if(os.path.isfile(maiml_file_path)):
                            os.remove(maiml_file_path)
                        if(os.path.isfile(tiff_file_path)):
                            os.remove(tiff_file_path)
                    except Exception as e:
                        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ','デフォルトデータ削除時エラー',e)
                        messages.add_message(request, messages.ERROR, messagesList.registrationError)
                        return render(request, 'fileupload.html', {'form':form})

                    if "toupdate" in request.POST: # アップロードボタン押下時
                        new_maimldict = {}
                        ## protocolからdataとevenlLogを作成したDict(UUID4も作成)
                        updatemaiml = UpdateMaiML()
                        new_maimldict = updatemaiml.createFullMaimlDict(maimldict)
                        new_maimluuid = new_maimldict[maimlelement.maiml][maimlelement.document][maimlelement.uuid]
                        # Read TIFF data
                        utils = MaimlUtil()
                        try:
                            tiffdict = utils.readTIFF(document_uuid, new_maimluuid, form.cleaned_data['upload_tiff'])
                        except Exception as e:
                            print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ','Errors occurred in utils.readTIFF.')
                            messages.add_message(request, messages.ERROR, messagesList.readTiffError)
                            return render(request, 'fileupload.html', {'form':form})
                        try:
                            ## TIFF データとマージ
                            new_maimldict = updatemaiml.margeFullMaimlDict(new_maimldict, tiffdict)
                        except Exception as e:
                            print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ','Errors occurred in updatemaiml.margeFullMaimlDict.')
                            messages.add_message(request, messages.WARNING, messagesList.invalidFiles)
                            return render(request, 'fileupload.html', {'form':form})

                        # create input form
                        initial_values = {
                            'upload_maiml_id':document_uuid, 
                            'upload_tiff':form.cleaned_data['upload_tiff'], 
                            'maiml_dict':json.dumps(new_maimldict, cls=DjangoJSONEncoder),
                            }
                        updateform = MaimlUpdateForm(initial_values)
                        
                        return render(request, 'updateform.html', {'form': updateform})
                else:
                    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                    form.protocolmodel = 0
                    return render(request, 'fileupload.html', {'form': form})
            except:
                Document.objects.filter(upload_maiml_id = staticVal.upload_maiml_id).delete()
                shutil.rmtree(settings.MEDIA_ROOT + f'/inputdocs/{staticVal.upload_maiml_id}')
                return render(request, '500.html', {'form': form})
        else:
            form = DocumentForm()
            form.protocolmodel = 0
            return render(request, 'fileupload.html', {'form': form})
    
    def upload_tiff(request, upload_maiml_id=""):
        if request.method == 'POST':
            form = TiffUploadForm(request.POST, request.FILES)
            if form.is_valid():
                upload_maiml_id_data = request.POST['upload_maiml_id']
                file_obj = request.FILES['upload_tiff']
                # mediaディレクトリにTiffファイルを保存
                tiff_savepath = form.save(upload_maiml_id_data)
                
                pnml_position_data = request.POST['petri_data']
                #ペトリネット図の座標情報をファイルに保存
                positionfilepath = settings.MEDIA_ROOT +'/pnml/' + upload_maiml_id_data + '.position'
                try:
                    f = open(positionfilepath, 'w', encoding='UTF-8')
                    f.write(pnml_position_data)
                except:
                    pass
                
                # Read MaiML data
                document_obj = Document.objects.get(upload_maiml_id = upload_maiml_id_data)
                document_obj.upload_tiff = str(tiff_savepath).replace(settings.MEDIA_ROOT+'/', '')
                document_obj.save()

                maiml_file_path = document_obj.upload_maiml.path
                readWriteMaiML_class = ReadWriteMaiML()
                maimldict = readWriteMaiML_class.readFile(maiml_file_path) 
                new_maimldict = {}
                ## protocolからdataとevenlLogを作成したDict(UUID4も作成)
                updatemaiml = UpdateMaiML()
                new_maimldict = updatemaiml.createFullMaimlDict(maimldict)
                new_maimluuid = new_maimldict[maimlelement.maiml][maimlelement.document][maimlelement.uuid]
                        
                # Read TIFF data
                utils = MaimlUtil()
                tiffdict = utils.readTIFF(upload_maiml_id_data, new_maimluuid, file_obj)

                ## TIFF データとマージ
                new_maimldict = updatemaiml.margeFullMaimlDict(new_maimldict, tiffdict) 
                # create input form
                initial_values = {
                    'upload_maiml_id':upload_maiml_id_data, 
                    'maiml_dict':json.dumps(new_maimldict, cls=DjangoJSONEncoder),
                    }
                updateform = MaimlUpdateForm(initial_values)
                return render(request, 'updateform.html', {'form': updateform})
            else:
                print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                form.protocolmodel = 0
                return render(request, 'tifffileupload.html', {'form': form})
        else:
            # maiml-uuidからペトリネット図用のデータを生成する
            # Read MaiML data
            document_obj = Document.objects.get(upload_maiml_id = upload_maiml_id)
            maiml_file_path = document_obj.upload_maiml.path
            readWriteMaiML_class = ReadWriteMaiML()
            maimldict = readWriteMaiML_class.readFile(maiml_file_path)
            petrinetdata = []
            pnmldatapath = settings.MEDIA_ROOT +'/pnml/' + upload_maiml_id + '.position'
            if os.path.isfile(pnmldatapath):
                f = open(pnmldatapath, 'r', encoding='UTF-8')
                petrinetdata = eval(f.read())
                f.close()
            else:
                ## maiml_dict --> petrinet graph data
                maimlUtilforPNML = MaimlUtilforPNML()
                petrinetdata = maimlUtilforPNML.makepnmlgraphdata(maimldict)
            default_data = {'upload_maiml_id':upload_maiml_id,
                            'petri_data':json.dumps(petrinetdata, cls=DjangoJSONEncoder),}
            form = TiffUploadForm(default_data)
            form.errors.clear()
            return render(request, 'tifffileupload.html', {'form': form})

#############################################
##    class for URI  Data Update
##     URL/update/  -->   URL/Top
#############################################
class DocumentUpdate():
    #ファイルを読み込み項目を抽出しupdateフォームの画面を表示
    def update_maiml(request):
        if request.method == 'POST':
            # requestのformからMaiMLの編集情報を取得する
            form = MaimlUpdateForm(request.POST)
            
            if not form.is_valid():
                print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),'  ',"form.errors:::",form.errors)
                return render(request, 'updateform.html', {'form': form,})
            ## MaiMLファイルを更新
            else:
                ## requestのJSONをDictに変換
                full_data_dict = form.cleaned_data['maiml_dict']
                ## DocumentのUUIDを取得
                olduuid = form.cleaned_data['upload_maiml_id']
                doc_obj = Document.objects.get(upload_maiml_id = olduuid)

                ## full_data_dictからUUIDを取得してディレクトリを作る
                newuuid = full_data_dict[maimlelement.maiml][maimlelement.document][maimlelement.uuid]

                tiff_file_path = doc_obj.upload_tiff.path
                # 新しいTiffの保存先
                tiff_file_name = doc_obj.upload_tiff.name
                tiff_new_path = settings.MEDIA_ROOT+'/'+MaimlUtil.path_branch(newuuid, tiff_file_name.replace('inputdocs', 'outputdocs'))
                # TIFF 複製
                try:
                    os.makedirs(os.path.dirname(tiff_new_path), exist_ok=False)
                except FileExistsError:
                    pass
                shutil.copy2(tiff_file_path, tiff_new_path)

                # resultのコンテンツとしてTiifのinsertionを追加する
                updatemaiml = UpdateMaiML()
                full_data_dict = updatemaiml.addinsertion(full_data_dict, tiff_file_path)

                ## create new MaiML file
                # 新しいMaimlの保存先
                maiml_file_name = doc_obj.upload_maiml.name
                maiml_new_path = settings.MEDIA_ROOT+'/'+MaimlUtil.path_branch(newuuid, maiml_file_name.replace('inputdocs', 'outputdocs'))
                try:
                    os.makedirs(os.path.dirname(maiml_new_path), exist_ok=True)
                except FileExistsError:
                    pass

                WM = ReadWriteMaiML()
                out_filepath, setuuid = WM.writecontents(full_data_dict, maiml_new_path)

                ## new MaiML fileを(Document model)に登録
                newdescription = 'system updated file:'+ os.path.basename(maiml_file_name)
                maiml_new_path = str(maiml_new_path).replace(settings.MEDIA_ROOT+'/', '')
                tiff_new_path = str(tiff_new_path).replace(settings.MEDIA_ROOT+'/', '')
                protocol_type = Maimltype.objects.get(model_type = 1)
                Document.objects.create(
                    upload_maiml_id = setuuid,
                    description = newdescription, 
                    upload_maiml = maiml_new_path,
                    upload_tiff = tiff_new_path,
                    MaiMLtype = protocol_type,
                    )
                
                #doc_objのtiffファイルを削除
                doc_obj.upload_tiff = ""
                doc_obj.save()
                return redirect('createapp:top')
        else:
            return render(request, 'top.html')