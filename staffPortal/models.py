from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
import os,time
from superadmin.models import studentCourses

# Create your models here.

#========================
# Changing Adhar Name accordin to the Employee Name
#========================

def adhar_upload_path(instance,adhar):
    # Getting FIle Extension(.jpg, .pdf etc.)
    # ext = os.path.splitext(adhar.name)[1]  # Is is not working
    ext = adhar.split(".")[-1]

    # sligify the staff name(ramove spaces/special charactere) OR clean employee name
    name = slugify(instance.name)

    # Add timestamp so files don’t overwrite each other
    timestamp = int(time.time())

    # New filename → madhu-adhar-123456.jpg
    filename = f"{name}-adhar-{timestamp}.{ext}"
    return os.path.join('adhar',filename)

#==========================
# Changing PAN Name accordin to the Employee Name
#==========================

def pan_upload_path(instance, pan):
    # ext = os.path.splitext(pan.name)[1] # Is is not working
    ext = pan.split(".")[-1]

    # slugify the staff name(remove spaces/special character)
    name = slugify(instance.name)

    # adding time stamp so the same name file won't affect each other
    timestamp = int(time.time())

    # New filename → madhu-pan-123456.jpg
    filename = f"{name}-pan{timestamp}.{ext}"
    return os.path.join('pan',filename)


#====================================
# Uploading Salary Slip 
#===================================


def salary_slip_upload_path(instance,salary_slip):
    # Getting FIle Extension(.jpg, .pdf etc.)
    # ext = os.path.splitext(adhar.name)[1]  # Is is not working
    ext = salary_slip.split(".")[-1]

    # sligify the staff name(ramove spaces/special charactere) OR clean employee name
    name = slugify(instance.name)

    # Add timestamp so files don’t overwrite each other
    timestamp = int(time.time())

    # New filename → madhu-adhar-123456.jpg
    filename = f"{name}-salary_slip-{timestamp}.{ext}"
    return os.path.join('salary_slip',filename)




# Country - state- city Hierarchy
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class staffRegistrationModel(models.Model):
    
    # Personal Details
    name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    f_h = models.CharField(max_length=50)
    email = models.EmailField(unique=True) 
    dob = models.DateField(blank=True, null= True)
    gender = models.CharField(max_length=10)

    # Account Security
    password = models.CharField(max_length=100)
    # confirm_password = models.CharField(max_length=100)

    # Designation
    role = models.ForeignKey("superadmin.roleModel", on_delete=models.CASCADE, null=True, blank=True)

    # Contact Details
    address = models.CharField(max_length=500, null=True, blank=True)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message="phone must be 10 digits")])
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city  = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length = 6, validators=[RegexValidator(r'^\d{6}$', message="pin code must be 6 digits ")])
    
    # Documents upload
    adhar = models.FileField(upload_to=adhar_upload_path, blank=False)
    pan = models.FileField(upload_to=pan_upload_path, blank=False)
    
    #  Educational Details 
    highest_qualification= models.CharField(max_length=100,null=True, blank=True, default="")
    specialization = models.CharField(max_length=100,null=True, blank=True, default="")
    passing_year = models.CharField(max_length=4,validators=[RegexValidator(r'^\d{4}$', message="Year must be in 4 digits")],null=True,blank=True,default=None)

    college= models.CharField(max_length=150,null=True, blank=True, default="")
    percentage = models.FloatField(null=True, blank=True, default=None)

    # Professional Details
    work_status = models.CharField(max_length=12,null=True, blank=True, default="")
    company_name = models.CharField(max_length=60,null=True, blank=True, default="")
    job_title = models.CharField(max_length=50,null=True, blank=True, default="")
    total_experience = models.CharField(max_length=20, null=True, blank=True, default="")
    notice_period = models.CharField(max_length=20, null=True, blank=True,default="")
    salary = models.IntegerField( null=True, blank=True,default=0)
    salary_slip = models.FileField(upload_to=salary_slip_upload_path, blank=False, null=True)
     
    agree = models.BooleanField(default=False,help_text="Must agree to terms & conditions")
    is_active =  models.BooleanField(default=False, help_text = "Control Staff login access")

    def __str__(self):
        return self.name



# ================================
# Staff Login Model
#=================================

class loginModel(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    

# ================================
# Student Enquiry Model
#=================================


class StudentEnquiryModel(models.Model):
    
    # Personal Details
    name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    f_h = models.CharField(max_length=50)
    dob = models.DateField(blank=True, null= True)
    gender = models.CharField(max_length=10)

    # course Name
    course = models.ForeignKey(studentCourses, on_delete=models.SET_NULL, null=True, blank=True)

    # Contact Details
    email = models.EmailField(unique=True) 
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message="phone must be 10 digits")])
    address = models.CharField(max_length=500, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city  = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length = 6, validators=[RegexValidator(r'^\d{6}$', message="pin code must be 6 digits ")])
    
    #  Educational Details 
    highest_qualification= models.CharField(max_length=100,null=True, blank=True, default="")
    school_name = models.CharField(max_length=100,null=True, blank=True, default="")
    course_name = models.CharField(max_length=100,null=True, blank=True, default="")
    college_name= models.CharField(max_length=150,null=True, blank=True, default="")
    branch_name = models.CharField(max_length=100,null=True, blank=True, default="")
    passing_year = models.CharField(max_length=4,validators=[RegexValidator(r'^\d{4}$', message="Year must be in 4 digits")],null=True,blank=True,default=None)
    percentage = models.FloatField(null=True, blank=True, default=None)

    # Professional Details
    work_status = models.CharField(max_length=12,null=True, blank=True, default="")
    company_name = models.CharField(max_length=60,null=True, blank=True, default="")
    total_experience = models.CharField(max_length=20, null=True, blank=True, default="")
    job_title = models.CharField(max_length=50,null=True, blank=True, default="")
    notice_period = models.CharField(max_length=20, null=True, blank=True,default="")
    salary = models.IntegerField( null=True, blank=True,default=0)
     
    # Documents upload
    adhar = models.FileField(upload_to=adhar_upload_path, blank=False)
    salary_slip = models.FileField(upload_to=salary_slip_upload_path, blank=False, null=True)

    # Enquiry Person/Administrator  Name
    Enquiry_person = models.ForeignKey(staffRegistrationModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    agree = models.BooleanField(default=False,help_text="Must agree to terms & conditions")
    directors_meeting =  models.BooleanField(default=False, help_text = "Meeting with director")

    remark = models.TextField(max_length=500, null=True, blank=True)
    is_recent = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ================================
# Trainers Class Model
#=================================

class TrainersClassSchedule(models.Model):
    className = models.CharField(max_length=50)
    startingTime = models.TimeField(null=True)
    endingTime = models.TimeField(null=True)
    startingDate = models.DateField(null=True)

    def __str__(self):
        return self.className
