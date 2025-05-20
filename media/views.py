from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from .models import Media


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if not title:
            return HttpResponse('Title is required', status=400)
        if not description:
            return HttpResponse('Description is required', status=400)
        if not file:
            return HttpResponse('File is required', status=400)
        
        import os

        count = Media.objects.count() + 1  # current count + 1
        original_name = file.name.replace(" ", "_")  # clean spaces just in case
        _, ext = os.path.splitext(original_name)  # get the file extension only
        new_name = f"{count}{ext}"  # just the count plus extension
        file.name = new_name


        media_file = Media(title=title, description=description, file=file)
        media_file.save()

        return HttpResponse('File uploaded successfully!', status=201)


class ViewView(View):
    def get(self, request, file_id):
        try:
            media_file = Media.objects.get(id=file_id)
            file_url = media_file.file.url

            html = f"""
                <h1>Media File Details</h1>
                <div style="margin-bottom: 20px;">
                    <img src="{file_url}" alt="{media_file.title}" width="300"><br>
                    <strong>File ID:</strong> {media_file.id}<br>
                    <strong>Title:</strong> {media_file.title}<br>
                    <strong>Description:</strong> {media_file.description}<br>
                    <a href="{file_url}" download>Download File</a>
                </div>
                <hr>
            """
            return HttpResponse(html)
        except Media.DoesNotExist:
            return HttpResponse('File not found', status=404)


class ListMediaView(View):
    def get(self, request):
        all_media = Media.objects.all().order_by('-created_at')
        html = "<h1>All Uploaded Media Files</h1><hr>"

        for media_file in all_media:
            file_url = media_file.file.url
            file_name = media_file.title or file_url.split('/')[-1]
            ext = file_url.lower().split('.')[-1]

            if ext in ["jpg", "jpeg", "png", "gif"]:
                content = f'<img src="{file_url}" alt="{file_name}" width="300">'
            elif ext == "pdf":
                content = f'<iframe src="{file_url}" width="100%" height="500px"></iframe>'
            elif ext in ["xls", "xlsx", "csv"]:
                content = f'<p>Excel/CSV file: <a href="{file_url}" target="_blank">Download/View</a></p>'
            else:
                content = f'<p>File: <a href="{file_url}" target="_blank">Download/View</a></p>'

            html += f'''
                <div style="margin-bottom: 20px;">
                    {content}
                    <br><strong>File ID:</strong> {media_file.id}<br>
                    <strong>Title:</strong> {media_file.title}<br>
                    <strong>Description:</strong> {media_file.description}<br>
                    <a href="{file_url}" download>Download File</a>
                </div>
                <hr>
            '''

        return HttpResponse(html)   



@method_decorator(csrf_exempt, name='dispatch')
class UpdateView(View):
    def post(self, request):
        file_id = request.POST.get('id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if not file_id:
            return HttpResponse("File ID is required", status=400)

        try:
            media_file = Media.objects.filter(id=file_id).first()
            if not media_file:
                return HttpResponse("You have ebtered the wrong ID", status=404)

            if title:
                media_file.title = title
            if description:
                media_file.description = description
            if file:
                media_file.file = file  # Replace the old file with new one
            
            import os

            
            original_name = file.name.replace(" ", "_")  # clean spaces just in case
            _, ext = os.path.splitext(original_name)  # get the file extension only
            new_name = f"{file_id}_{ext}"  # just the count plus extension
            file.name = new_name

            media_file.save()
            return HttpResponse("File updated successfully!", status=200)

        except Media.DoesNotExist:
            return HttpResponse("File not found", status=404)


import json
@method_decorator(csrf_exempt, name='dispatch')
class DeleteView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            file_id = data.get('id')
        except (json.JSONDecodeError, AttributeError):
            return HttpResponse('Invalid JSON', status=400)

        if not file_id:
            return HttpResponse('File ID is required', status=400)

        try:
            media_file = Media.objects.get(id=file_id)
            media_file.delete()
            return HttpResponse('File deleted successfully!', status=200)
        except Media.DoesNotExist:
            return HttpResponse('File not found', status=404)
        



import pandas as pd

from django.http import JsonResponse
from .models import Marks, Students

@method_decorator(csrf_exempt, name='dispatch')
class LargeFilePricessingView(View):
    def post(self, request):
        student_file = request.FILES.get('student_file')
        marks_file = request.FILES.get('marks_file')
        user_roll = request.POST.get('roll')

        if not student_file:
            return JsonResponse({'error': 'No file student_file'}, status=400)
        if not marks_file:
            return JsonResponse({'error': 'No file marks_file'}, status=400)

        try:
            # Load CSVs into pandas DataFrames
            df_students = pd.read_csv(student_file)
            df_marks = pd.read_csv(marks_file)

            # Clean column names
            df_students.columns = df_students.columns.str.strip()
            df_marks.columns = df_marks.columns.str.strip()

            # Calculate average
            df_marks['Average'] = df_marks[['DAA', 'JAVA', 'PYTHON', 'C++']].mean(axis=1)

            # Save/update students
            for _, row in df_students.iterrows():
                Students.objects.update_or_create(
                    roll=row['roll'],
                    defaults={
                        'name': row.get('name', ''),
                        'email': row.get('email', ''),
                        'branch': row.get('branch', ''),
                        'semester': row.get('semester', 1),
                        'section': row.get('section', ''),
                        'number': row.get('number', ''),
                    }
                )
            
            # Save/update marks
            for _, row in df_marks.iterrows():
                student_obj = Students.objects.filter(roll=row['roll']).first()
                print(student_obj)
                if not student_obj:
                    continue  # Skip if no matching student

                Marks.objects.update_or_create(
                    roll=student_obj,
                    defaults={
                        'daa': row.get('DAA'),
                        'java': row.get('JAVA'),
                        'python': row.get('PYTHON'),
                        'cpp': row.get('C++'),
                        'average': row.get('Average'),
                    }
                )

            # Return data for specific roll if provided
            is_valid_roll = Students.objects.filter(roll=user_roll).exists()
            if user_roll and is_valid_roll:
                marks = Marks.objects.filter(roll=user_roll).values(
                    'roll', 'daa', 'java', 'python', 'cpp', 'average'
                ).first()

                if not marks:
                    return JsonResponse({'error': 'Roll number not found'}, status=404)

                details = Students.objects.filter(roll=user_roll).values(
                    'roll', 'name', 'email', 'branch', 'semester', 'section', 'number'
                ).first()
                return JsonResponse({'message': 'Data uploaded successfully','details' : details, 'marks': marks})
            else:
                return JsonResponse({'message': 'Data uploaded successfully but Roll number not found'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
