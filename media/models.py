from django.db import models

class Media(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Students(models.Model):
    roll = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=10)
    semester = models.PositiveSmallIntegerField()
    section = models.CharField(max_length=5)
    number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.roll}"



class Marks(models.Model):
    roll = models.ForeignKey('Students', to_field='roll', on_delete=models.CASCADE)
    daa = models.PositiveIntegerField(null=True, blank=True)
    java = models.PositiveIntegerField(null=True, blank=True)
    python = models.PositiveIntegerField(null=True, blank=True)
    cpp = models.PositiveIntegerField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Marks for {self.roll.roll}"
