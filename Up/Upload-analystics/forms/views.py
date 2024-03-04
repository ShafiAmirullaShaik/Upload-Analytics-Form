from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from forms.models import testingUploadModel
import pandas as pd
import os
import json

def fileUpload(request):
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES.get('file')
            extension = request.POST.get('extension')
            data_source = request.POST.get('datasource')
            userDataSource = request.POST.get('userDataSource')
 
            # Check if a file with the same name already exists
            existing_file = testingUploadModel.objects.filter(filename=uploaded_file.name).first()
 
            if existing_file:
                return render(request, 'form.html', {'confirm_replace': True, 'msg': f'Filename "{uploaded_file.name}" already exists.'})
            else:
                path = f'C:\\Users\\USER\Desktop\\Forms\\Up\\Upload-analystics\\files\\'
                file_path = os.path.join(path, str(uploaded_file))
 
                # Save the file information to the database
               
                inserted_data = testingUploadModel(filename=uploaded_file, dataSource=userDataSource, filePath=file_path)
                inserted_data.save()
               
 
                # Save the file to the desired path
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
 
                return render(request, 'form.html', {'msg': f'Filename "{uploaded_file.name}" uploaded successfully!', 'analyticsPage': 'Go for analysis'})
        else:
            return render(request, 'form.html')
    except Exception as e:
        return JsonResponse({'error': str(e)})
   
# def replace_filename(request):
#         getname = request.GET.get('getNewName')
#         datasource = request.GET.get('datasource')
#         getExtension = request.GET.get('getExtension')
#         print(datasource)
#         print(getExtension)
 
#         if_already_exists = testingUploadModel.objects.filter(filename=getname, dataSource=datasource).first()
 
 
#         if if_already_exists:
#             return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
#         else:
#             try:
#                 new_filename = getname
#                 if_already_exists = testingUploadModel.objects.filter(filename=new_filename).first()
 
#                 if if_already_exists:
#                     return JsonResponse({'reEntername': 'This renamed file already exists with DataSource!!', 'Bool': True})
 
#                 # Set the file path (adjust as needed)
#                 original_filepath = f'C:\\Users\\USER\Desktop\\Forms\\Up\\Upload-analystics\\files\\{getname + getExtension}'
#                 filepath = f'C:\\Users\\USER\Desktop\\Forms\\Up\\Upload-analystics\\files\\{new_filename + getExtension}'
 
#                     # Read the content of the existing file
#                 with open(original_filepath, 'rb') as source:
#                     content = source.read()
 
#                 # Create a new object and save it to the database
#                 new_file = testingUploadModel(filename=new_filename, dataSource=datasource, filePath = filepath)
#                 new_file.save()
 
#                 # # Save the content to the new file
#                 # with open(filepath, 'wb') as destination:
#                 #     destination.write(content)
 
#                 # Save the file to the desired path
#                 with open(filepath, 'wb+') as destination:
#                     # Assuming getname and getExtensionType are file content (adjust as needed)
#                     destination.write(getname.encode())
#                     destination.write(datasource.encode())
#                     destination.write(filepath.encode())
#                     destination.write(content)
 
#                 return JsonResponse({'reEntername': 'File renamed successfully!!', 'Bool': False})
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)      
    
def replace_filename(request):
    getname = request.GET.get('getNewName')
    datasource = request.GET.get('datasource')
    getExtension = request.GET.get('getExtension')
 
    if_already_exists = testingUploadModel.objects.filter(filename=getname, dataSource=datasource).first()
 
    if if_already_exists:
        return JsonResponse({'reEntername': 'This renamed file already exists!!', 'Bool': True})
    else:
        try:
            new_filename = f'{getname}.{getExtension}'
            if_already_exists = testingUploadModel.objects.filter(filename=new_filename).first()
 
            if if_already_exists:
                return JsonResponse({'reEntername': 'This renamed file already exists with DataSource!!', 'Bool': True})
 
            # Set the file paths (adjust as needed)
            original_filepath = f'C:\\Naveen\\Esoft Analytics\\Works\\Upload-Analytics-Form-1\\files\\Solved_Tickets.xlsx'
            destination_filepath = f'C:\\Naveen\\Esoft Analytics\\Works\\Upload-Analytics-Form-1\\files\\{new_filename}'
 
            print(original_filepath)
            print(destination_filepath)
 
            # Read the content of the existing file
            with open(original_filepath, 'rb') as source:
                content = source.read()
 
            # Create a new object and save it to the database
            new_file = testingUploadModel(filename=new_filename, dataSource=datasource, filePath=destination_filepath)
            new_file.save()
 
            # Save the file content to the desired path
            with open(destination_filepath, 'wb') as destination:
                destination.write(content)
 
            return JsonResponse({'reEntername': 'File renamed successfully!!', 'Bool': False})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
 
def filesList(request):
    getFilesNames = testingUploadModel.objects.values_list('filename', flat = True)
    return render(request, 'analyticsForm.html', {'filesListNames' : getFilesNames})
   
 
 
def dataset(path):
    extension = path[path.rfind('.'):]

    try:
        if extension == ".csv":
            df = pd.read_csv(path)
        elif extension in [".xls", ".xlsx", ".xlsm", ".xlsb"]:
            df = pd.read_excel(path)
        elif extension == ".html":
            df = pd.read_html(path)
        else:
            df = pd.read_json(path)
        
        return df
    except Exception as e:
        return JsonResponse({'Error': f'Unable to fetch columns Error: {str(e)}'})
 
 

# Mani
def list_datasources(request):
    try:
        datasources = testingUploadModel.objects.values_list("dataSource", flat=True).distinct()
        return render(request,'analyticsForm.html',{'datasources':datasources})
    except Exception as e:
        return HttpResponseServerError(f'Unable to fetch datasources. Error: {str(e)}')
   
def list_files(request):
    try:
        datasourcename=request.GET.get('fileNameData')
        list_of_files=testingUploadModel.objects.filter(dataSource=datasourcename).values_list('filename', flat=True)
        files=[]
        for i in list_of_files:
            files.append(i)
        return JsonResponse({'files':files})
    except Exception as e:
        return HttpResponseServerError(f'Unable to fetch list of files. Error:{str(e)}')
    

def getColumnList(request):
    filename = request.GET.get('fileNameData')

    file_path = testingUploadModel.objects.filter(filename=filename).first()
    file_path = file_path.filePath
   
    if not os.path.exists(file_path):
        return JsonResponse({'Error': 'File not found.'})
 
    try:
        
        df = dataset(file_path)
        print(df)
        columnList = df.columns.tolist()
        return JsonResponse({"columns": columnList})
    except Exception as e:
        return JsonResponse({'Error': f'Error fetching columns: {str(e)}'})
 

def CreateDataFrame(request):
    try:
        if request.method == 'POST' :
            data = json.loads(request.body.decode('utf-8'))
            columns = data.get('columns')
            filename = data.get('filename')
            if not columns and not filename:
                return  HttpResponseBadRequest("Invalid File Name.")
            else:
                path = testingUploadModel.objects.filter(filename=filename).first()
                path = path.filePath
                df = dataset(path) #dataset() function returns dataframe by taking file path
                newDf = df[columns]
                return render(request,'test.html')
        else:
            return HttpResponseServerError(f'Not a post method:{str(e)}')
 
    except Exception as e:
        return HttpResponseServerError(f'Unable to fetch columns Error:{str(e)}')
    