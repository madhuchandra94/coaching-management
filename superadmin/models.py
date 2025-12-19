from django.db import models

# Create your models here.

class loginModel(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class roleModel(models.Model):
    role = models.CharField(max_length=60)

    def __str__(self):
        return self.role
    
class studentCourses(models.Model):
    course = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.course