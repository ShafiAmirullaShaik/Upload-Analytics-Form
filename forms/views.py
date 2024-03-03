from django.shortcuts import render
from django.http import JsonResponse
from forms.models import filesData
import pandas as pd


def fileUpload(request):
    try:
        if request.method == 'POST':
            uploadedFile = request.FILES.get('file')
            getExtension = request.POST.get('extension')

            file_name = filesData.objects.filter(filename=uploadedFile.name).first()
            
            if file_name:
                return render(request, 'form.html', {'confirm_replace': True, 'msg': f'Filename "{uploadedFile.name}" already exists..'})
            else:
                insertedData = filesData(filename=uploadedFile, extension=getExtension)
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
        
        if_already_exists = filesData.objects.filter(filename=getname).first()
        
        if if_already_exists:
            return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
        else:
            try:
                new_filename = getname + getExtensionType
                if_already_exists = filesData.objects.filter(filename=new_filename).first()
                if if_already_exists:
                    return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
                new_file = filesData(filename=new_filename, extension = getExtensionType)
                new_file.save()
                return JsonResponse({'reEntername': 'File renamed successfully!!', 'Bool': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def filesList(request):
    getFilesNames = filesData.objects.values_list('filename', flat = True)
    return render(request, 'analyticsForm.html', {'filesListNames' : getFilesNames})
    


extension = ''
def dataset(path): 
    print(path)
    global extension 
    extension = path[path.rfind('.'):] 
    try:
        if extension == ".csv":
            df = pd.read_csv(path)
        elif extension in [".xls",".xlsx",".xlsm",".xlsb"]:
            df = pd.read_excel(path)
        elif extension == ".html":
            df = pd.read_html(path)
        else:
            df = pd.read_json(path)
        return df
    except Exception as e:
        return JsonResponse({'Error' : f'Unable to fetch columns Error:{str(e)}'})


def getColumnList(request):
    filename = request.GET.get('fileNameData')
     
    fileExist = filesData.objects.filter(filename=filename).first()
    if not fileExist:
        return JsonResponse({'Error' : "Invalid File Name."})
    else:
        path = r"C:\Users\shafi\OneDrive\Desktop\Node\esoftAnalytics\files"
        filename = "\\" + filename
        print(filename)
        path = path + filename
        df = dataset(path)
        columnList = df.columns.tolist()
        return JsonResponse({"columns": columnList})

