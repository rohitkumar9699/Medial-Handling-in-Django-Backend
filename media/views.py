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
            html += f'''
                <div style="margin-bottom: 20px;">
                    <img src="{file_url}" alt="{media_file.title}" width="300"><br>
                    <strong>File ID:</strong> {media_file.id}<br>
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
            media_file = Media.objects.get(id=file_id)

            if title:
                media_file.title = title
            if description:
                media_file.description = description
            if file:
                media_file.file = file  # Replace the old file with new one
            
            import os

            count = Media.objects.count() + 1  # current count + 1
            original_name = file.name.replace(" ", "_")  # clean spaces just in case
            _, ext = os.path.splitext(original_name)  # get the file extension only
            new_name = f"{count}{ext}"  # just the count plus extension
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