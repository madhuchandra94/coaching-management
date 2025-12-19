from django.contrib import admin
from .models import staffRegistrationModel, Country, State, City, StudentEnquiryModel,TrainersClassSchedule
from django.utils.html import format_html

# Register your models here.


    # -----------------------------
    # Display Aadhar as thumbnail
    # -----------------------------

def adhar_file(self, obj):
    if obj.adhar:
        return format_html("<a> href='{}' target='_blank'>view Aadhaar</a>",obj.adhar.url)
    return "No Adhar"
adhar_file.short_description = 'Aadhar'



    # -----------------------------
    # Display PAN as thumbnail
    # -----------------------------

def pan_file(self, obj):
    if obj.pan:
        return format_html("<a> href='{}' target='_blank'>view PAN</a>",obj.pan.url)
    return "No PAN"
pan_file.short_description = 'PAN'


# -----------------------------
# Display SALARY SLIP as thumbnail
# -----------------------------

def salary_slip_file(self, obj):
    if obj.salary_slip:
        return format_html("<a> href='{}' target='_blank'>view Salary Slip</a>",obj.salary_slip.url)
    return "No Salary Slip"
salary_slip_file.short_description = 'SALARY_SLIP'




# admin.site.register(staffRegistrationModel)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(StudentEnquiryModel)
admin.site.register(TrainersClassSchedule)
