from django.shortcuts import render
from django.http import JsonResponse
from forms.models import fileData
import pandas as pd


def fileUpload(request):
    try:
        if request.method == 'POST':
            uploadedFile = request.FILES.get('file')
            getExtension = request.POST.get('extension')

            file_name = fileData.objects.filter(filename=uploadedFile.name).first()
            
            if file_name:
                return render(request, 'form.html', {'confirm_replace': True, 'msg': f'Filename "{uploadedFile.name}" already exists..'})
            else:
                path = r"C:\Users\USER\Desktop\Forms\Upload&Analytics\Upload-Analytics-Form\files"
                filename = "\\" + uploadedFile
                path = path + filename
                insertedData = fileData(filename=path, extension=getExtension)
                insertedData.save()
                return render(request, 'form.html', {'msg': f'Filename "{uploadedFile.name}" uploaded successfully!', 'analyticsPage' : 'Go for analysis'})
        else:
            return render(request, 'form.html')
    except Exception as e:
        return JsonResponse({'error': str(e)})
    


def replace_filename(request):
    if request.method == 'GET':
        getname = request.GET.get('getNewName')
        getExtensionType = request.GET.get('getExtension')
        
        if_already_exists = fileData.objects.filter(filename=getname).first()
        
        if if_already_exists:
            return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
        else:
            try:
                path = r"C:\Users\USER\Desktop\Forms\Upload&Analytics\Upload-Analytics-Form\files"
                filename = "\\" + getname
                path = path + filename
                new_filename = path + getExtensionType
                if_already_exists = fileData.objects.filter(filename=new_filename).first()
                if if_already_exists:
                    return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
                new_file = fileData(filename=new_filename, extension = getExtensionType)
                new_file.save()
                return JsonResponse({'reEntername': 'File renamed successfully!!', 'Bool': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def filesList(request):
    getFilesNames = fileData.objects.values_list('filename', flat = True)
    return render(request, 'analyticsForm.html', {'filesListNames' : getFilesNames})
    


extension = ''

def dataset(path):
    global extension
    extension = path[path.rfind('.'):]

    try:
        if extension == ".csv":
            df = pd.read_csv(path)
            print(df)
        elif extension in [".xls", ".xlsx", ".xlsm", ".xlsb"]:
            df = pd.read_excel(path)
            print(df)
        elif extension == ".html":
            df = pd.read_html(path)
        else:
            df = pd.read_json(path)
        return df
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def getColumnList(request):
    filename = request.GET.get('fileNameData')

    fileExist = fileData.objects.filter(filename=filename).first()
    if not fileExist:
        return JsonResponse({'Error': "Invalid File Name."})
    else:
        path = r"C:\Users\USER\Desktop\Forms\Upload&Analytics\Upload-Analytics-Form\files"
        filename = "\\" + filename
        path = path + filename
        df = dataset(path)

        if df is not None:
            columnList = df.columns.tolist()
            return JsonResponse({"columns": columnList})
        else:
            return JsonResponse({'Error': 'Unable to fetch columns.'})