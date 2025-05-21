
# Django Media Upload and Processing API

This project provides a simple Django-based API for uploading, viewing, updating, and deleting media files, as well as processing large CSV files containing student and marks data.

## Features

- Upload media files (images, PDFs, Excel, CSV, etc.) with metadata
- View a specific media file by ID
- List all uploaded media files with previews
- Update existing media files and metadata
- Delete media files by ID
- Upload large CSV files containing student and marks data, compute averages, and retrieve information

## Endpoints

### 1. Upload Media
- **URL**: `/upload/`
- **Method**: POST
- **Form Data**:
  - `title`: Title of the media file (required)
  - `description`: Description of the media file (required)
  - `file`: The file to be uploaded (required)

### 2. View Media File by ID
- **URL**: `/view/<file_id>/`
- **Method**: GET

### 3. List All Media Files
- **URL**: `/media-list/`
- **Method**: GET

### 4. Update Media File
- **URL**: `/update/`
- **Method**: POST
- **Form Data**:
  - `id`: ID of the file to update (required)
  - `title`: New title (optional)
  - `description`: New description (optional)
  - `file`: New file (optional)

### 5. Delete Media File
- **URL**: `/delete/`
- **Method**: POST
- **Body (JSON)**:
  - `id`: ID of the file to delete (required)

### 6. Process Large Files (Student and Marks Data)
- **URL**: `/process-csv/`
- **Method**: POST
- **Form Data**:
  - `student_file`: CSV file with student data (required)
  - `marks_file`: CSV file with marks data (required)
  - `roll`: Optional roll number to fetch specific student results

## Models Required

### Media
```python
class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
```

### Students
```python
class Students(models.Model):
    roll = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=50)
    semester = models.IntegerField()
    section = models.CharField(max_length=10)
    number = models.CharField(max_length=15)
```

### Marks
```python
class Marks(models.Model):
    roll = models.ForeignKey(Students, on_delete=models.CASCADE)
    daa = models.FloatField()
    java = models.FloatField()
    python = models.FloatField()
    cpp = models.FloatField()
    average = models.FloatField()
```

## Notes
- CSRF is disabled using `@csrf_exempt` for demonstration purposes. For production, enable proper CSRF protection.
- Pandas is used to handle and process CSV files.

## Requirements

- Django
- pandas

## Installation

```bash
pip install django pandas
```

## Run the server

```bash
python manage.py runserver
```

## Author

Generated with ❤️ by Rohit Kumar based on your Django Project.
