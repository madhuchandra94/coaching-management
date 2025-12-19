from django.shortcuts import render, redirect, get_object_or_404
from .models import loginModel, roleModel, studentCourses
from staffPortal.models import staffRegistrationModel, Country, State, City,StudentEnquiryModel
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import never_cache 
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.db.models import Q



# Create your views here.



#=========================
#Home Page 
#=========================
def homePage(request):
    return render(request,'home/home_page.html')

#=========================
#Admin Login Page View Function
#=========================
def LoginPageView(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        try:
            user = loginModel.objects.get(email=email, password=password)
            # Set session
            request.session['user_id'] = user.id
            request.session['user_email']=user.email

            messages.success(request, "Welcome Admin ")
            return redirect('adminpage')  
        
        except loginModel.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'superadmin/login.html')


#=========================
#Admin Page View Function
#=========================

@never_cache
def AdminPageView(request):
    if request.session.get('user_id'):   # session missing
        unread_count = StudentEnquiryModel.objects.filter(is_recent=True).count()
        all_data = roleModel.objects.all().order_by('-id')
        employee_record = staffRegistrationModel.objects.all().order_by('-id')
        student_courses = studentCourses.objects.all().order_by('-id')
        enquiry_data = StudentEnquiryModel.objects.all()  # fetch all records

        # ================================
        # ADDED FUNCTIONALITY FOR ADMIN:
        # ================================

        # SAME LOGIC AS COUNSELLOR DASHBOARD
        recent_enquiry_data = StudentEnquiryModel.objects.filter(
            remark__isnull=True,
            is_recent=True
        ).order_by('-id')

        student_enquiry_data = StudentEnquiryModel.objects.filter(
            remark__isnull=False,
            is_recent=False
        ).order_by('-id')

        # PANEL CONTROL
        open_panel = request.GET.get("open")

        context = {
            # "unread_count":unread_count,
            'data': all_data,
            'employees': employee_record,
            'courses': student_courses,
            'enquiry_data': enquiry_data,

            # ADDED ONLY – DO NOT BREAK ANYTHING
            "recent_enquiry": (open_panel == "recent_enquiry"),
            "recent_enquiry_data": recent_enquiry_data,

            "show_student_enquiry": (open_panel == "student_enquiry"),
            "student_enquiry_data": student_enquiry_data,

            "open": open_panel,  # to handle employee search panel
        }

        
        return render(request, 'superadmin/adminPage.html',context)
    else:
        return redirect("loginPage")

#=========================
#Log Out button view Function
#=========================

def LogOut(request):
    
    # Clear all session data
    request.session.flush()
    messages.success(request,"You have been logged out")
    return redirect('loginPage')


#=========================
# Adding New Role in a Table 
#=========================

def CreateRole(request):
    show_table = False # default Table is hide
    if request.method == "POST":
        role_name = request.POST.get('role')

        if role_name:
            if roleModel.objects.filter(role=role_name).exists():
                messages.warning(request, "This role already exists!")
            else:
                roleModel.objects.create(role=role_name)
                print(f"Role Name:-{role_name} Added")
                messages.success(request, 'New Role has Succesfully been Added!')
                show_table = True
                # url = reverse('adminpage') + '?showTable=1'
            all_data = roleModel.objects.all().order_by('-id')
            # return render(request, 'superadmin/adminPage.html/?open=roles',{'data':all_data, 'show_table':show_table})
            return redirect(reverse('adminpage') + '?open=roles')
    
    # for Get Request
    all_data = roleModel.objects.all().order_by('-id')
    return render(request, 'superadmin/adminPage.html',{'data':all_data, 'show_table':show_table})


#=========================
#Showing Role Table in Admin Page
#=========================


def showRoleTable(request):
    all_data = roleModel.objects.all().order_by('-id')
    return render(request,'superadmin/adminPage.html',{'data':all_data})
    

#=========================
# Upadting Role Data 
#=========================

def updateRoleData(request, id):
    instance = get_object_or_404(roleModel, pk=id)

    if request.method == "POST":
        role = request.POST.get('role')   # get updated role value
        if role:
            instance.role = role
            instance.save()
            messages.success(request, "Role Updated Successfully")
            # return redirect('adminpage')
            return redirect(reverse('adminpage') + "?open=roles")
        else:
            messages.error(request,"Role Cannot be empty")
        # return redirect('adminpage')   # back to admin page
        return redirect(reverse('adminpage') + "?open=roles")
     
    # for GET - render admin page but send edit_role
    all_data = roleModel.objects.all().order_by('-id')

   
   # If GET request → show form with pre-filled value
    # return render(request, 'superadmin/adminPage.html', {'data':all_data, 'instance' : instance})
    
    # If user somehow GETs this URL directly:
    return redirect(reverse('adminpage') + "?open=roles")
#=========================
# Deleting Role Data
#=========================

def deleteRoleData(request,id):
    instance = get_object_or_404(roleModel, pk=id)
    instance.delete()
    messages.success(request, 'User Deleted Successfully')
    all_data = roleModel.objects.all().order_by("-id")

    # return render(request, 'superadmin/adminPage.html',{'data':all_data})

    # Redirect to admin page and keep ROLES PANEL open 
    return redirect(reverse('adminpage') + "?open=roles")




#===========================
# Adding or Creating Student Course
# ==========================
def createCourse(request):
    show_table = False # Default Table is Hidden

    if request.method == "POST":
        course_name = request.POST.get('course')   # coming from form field name

        if course_name:
            if studentCourses.objects.filter(course=course_name).exists():
                messages.warning(request, "This Class already exists!")
            else:
                studentCourses.objects.create(course=course_name)
                print(f"Course Name:- {course_name} Added")
                messages.success(request, 'New Course has successfully been added!')
                show_table = True

        return redirect('/adminpage/?open=courses') # Redirect after POST(avoids resumbmission)    

    # For GET request
    all_courses = studentCourses.objects.all().order_by('-id')
    return render(request, 'superadmin/adminPage.html',
                      {'courses': all_courses, 
                       'show_table': show_table})



#=========================
# Upadting Course Data 
#=========================

def updateCourseData(request, id):
    instance = get_object_or_404(studentCourses, pk=id)

    if request.method == "POST":
        course_name = request.POST.get('course')
        if course_name:
            instance.course = course_name   
            instance.save()
            messages.success(request, "Course Updated Successfully")
        else:
            messages.error(request, "Course cannot be empty")
        # return redirect('adminpage')

    all_courses = studentCourses.objects.all().order_by('-id')
    # return render(request, 'superadmin/adminPage.html', {'courses': all_courses})
    return redirect('/adminpage/?open=courses')


#=========================
# Deleting Course Data
#=========================

def deleteCourseData(request, id):
    instance = get_object_or_404(studentCourses, pk=id)
    instance.delete()
    messages.success(request, 'Course deleted successfully')

    all_courses = studentCourses.objects.all().order_by('-id')
    # return render(request, 'superadmin/adminPage.html', {'courses': all_courses})
    return redirect('/adminpage/?open=courses')




#=========================
#Showing Employee Details in Table
#=========================

def employeeTable(request):
    employees = staffRegistrationModel.objects.all().order_by('-id')
    return render(request,'superadmin/employeeTable.html',{'employees':employees})
        


#=========================
# Toggle Staff Active status or Deactive Status
#=========================


def toggleEmployeeStatus(request,id):
    employee = get_object_or_404(staffRegistrationModel, id=id)
    employee.is_active = not employee.is_active
    employee.save()
    status = "Activated" if employee.is_active else "Deactivated"
    messages.success(request, f"{employee.name} has been {status} Succesfully.")
    return redirect('adminpage')



#========================
# Update Employee Details
#=======================


def update_employee_details(request, id):
    #getting old record
    staff = get_object_or_404(staffRegistrationModel, id=id)

    if request.method == "POST":

        # Personal Details
        staff.name = request.POST.get('name')
        staff.f_h = request.POST.get('f_h')
        staff.dob = request.POST.get('dob')
        staff.gender= request.POST.get('gender')

        # Account Security
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('con_password')
        
        if new_password:
            if new_password == confirm_password:
                staff.password = make_password(new_password)
            else:
                messages.error(request, "password do not match!")
                return redirect('adminpage', id=id)

        # Designation
        role_id = request.POST.get('role')
        staff.role = roleModel.objects.get(id=role_id) if role_id else None

        # contact details
        staff.email = request.POST.get('email')
        staff.mobile = request.POST.get('mobile')
        staff.address = request.POST.get('address').strip()

        # country/state/id
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        city_id = request.POST.get('city')
        
        country = Country.objects.get(id=country_id) if country_id else None
        staff.country = country

        state = State.objects.get(id=state_id) if state_id else None
        staff.state = state

        city = City.objects.get(id=city_id) if city_id else None 
        staff.city = city
        
        staff.pincode = request.POST.get('pincode','')


        # Educational Details
        staff.highest_qualification = request.POST.get("qualification")
        staff.specialization = request.POST.get('specialization')
        staff.passing_year = request.POST.get('passing_year')
        staff.college = request.POST.get("college_university")
        staff.percentage = request.POST.get('percentage_cgpa')

        #professional Details
        staff.work_status = request.POST.get('work_status')
        staff.company_name = request.POST.get('company_name')
        staff.job_title  = request.POST.get('Post_Name')
        staff.total_experience = request.POST.get('Total_Experience')
        staff.notice_period = request.POST.get('Notice_period')

        salary = request.POST.get('Salary')
        if salary in ("", None):
            staff.salary = 0
        else:
            try:
                staff.salary = int(salary)
            except ValueError:
                raise ValueError("Salary Must Be a Number")

        # Documents upload 
        staff.adhar = request.POST.get('adhar')
        staff.pan = request.POST.get('pan')
            
        # file uploads (update only if new file uploaded)
        if request.FILES.get('adhar_upload'):
            staff.adhar = request.FILES['adhar_upload']
        
        if request.FILES.get('pan_upload'):
            staff.pan = request.FILES['pan_upload']
        
        if request.FILES.get('salary_slip'):
            staff.salary_slip = request.FILES['salary_slip']
        
        #checkbox 
        staff.agree = bool(request.POST.get("agree"))

        # save updated record
        staff.save()
        messages.success(request, 'Staff Details Updated Successfully ')
        return redirect('adminpage')

    # For get Values show old data in staffregistration form
    country= Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    role = roleModel.objects.all()
    # employee_data = staffRegistrationModel.objects.all()
    return render (request, 'staffPortal/Registration.html',{
                                                            'staff':staff,
                                                            # 'data':employee_data,
                                                              'country':country,
                                                              'state':state, 
                                                              'city':city,
                                                              'role':role })    


#================================
# Deleting Employee Details
#================================

def delete_employee_details(request, id):
    instance = get_object_or_404(staffRegistrationModel, pk=id)
    instance.delete()
    messages.success(request,"Employee Details Deleted Successfully")
    
    all_details = staffRegistrationModel.objects.all().order_by('-id')
    return redirect(request, 'superadmin/adminPage.html',{'employees':all_details})



#=====================================================================
# Search Employee details 
#=====================================================================
# showing data with query selector
def search_Employee_details(request):
    query = request.GET.get('q') # Take search input from url
    if query:
        # enquiry_data = StudentEnquiryModel.objects.filter(
        #     Q(name__icontains = query)|
        #     Q(email__icontains = query)
        # )
        
        # Start with empty Q object
        search_filter = Q()
        
        # Loop through all fields of the model
        for field in staffRegistrationModel._meta.get_fields():
            # Only search in text-based fields
            if field.get_internal_type() in ["CharField", "TextField", "EmailField"]:
                search_filter |= Q(**{f"{field.name}__icontains": query})
        
        # Apply the combined filter
        employees = staffRegistrationModel.objects.filter(search_filter)
    else:
        # showing all table if there is no search
        employees = staffRegistrationModel.objects.all()
    
    context = {"employees":employees, 'query':query, "open": "employees"}
    return render(request, 'superadmin/adminPage.html',context) # showing table with searching data



#=====================================================================
# Search Student 
#=====================================================================
# showing data with query selector
def search_student_enquiry(request):
    query = request.GET.get('query') # Take search input from url
    if query:
        # enquiry_data = StudentEnquiryModel.objects.filter(
        #     Q(name__icontains = query)|
        #     Q(email__icontains = query)
        # )
        
        # Start with empty Q object
        search_filter = Q()
        
        # Loop through all fields of the model
        for field in StudentEnquiryModel._meta.get_fields():
            # Only search in text-based fields
            if field.get_internal_type() in ["CharField", "TextField", "EmailField"]:
                search_filter |= Q(**{f"{field.name}__icontains": query})
        
        # Apply the combined filter
        enquiry_data = StudentEnquiryModel.objects.filter(search_filter)
    else:
        # showing all table if there is no search
        enquiry_data = StudentEnquiryModel.objects.all()
    
    context = {"enquiry_data":enquiry_data, 'query':query}
    return render(request, 'superadmin/adminPage.html',{"enquiry_data":enquiry_data, 'query':query}) # showing table with searching data




# ============================== Counseller Dashboard ========================


def admin_student_enquiry_table(request):
    data = StudentEnquiryModel.objects.filter(remark__isnull=True, is_recent=True)
    unread_count = StudentEnquiryModel.objects.filter(remark__isnull=True).count()

    context = {
        "recent_enquiry": True,
        "show_student_enquiry": False,
        # "unread_count": unread_count,
        "data": data,
    }
    # return render(request, "superadmin/adminPage.html", context)
    return redirect('/adminpage/?open=student_enquiry')


# Recent Student Enquiry data
def admin_student_recent_enquiry(request):
    data = StudentEnquiryModel.objects.filter(remark__isnull=False, is_recent=False)

    context = {
        "recent_enquiry": False,
        "show_student_enquiry": True,
        "data": data
    }
    return render(request, "superadmin/adminPage.html", context)


def admin_activate_student_enquiry(request,id):
    student_enquiry = get_object_or_404(StudentEnquiryModel,id=id)
    student_enquiry.directors_meeting = True
    student_enquiry.save()
    Data = StudentEnquiryModel.objects.all()
    # return redirect("admin_student_enquiry_table")
    return redirect('/adminpage/?open=student_enquiry')



def admin_deactivate_student_enquiry(request,id):
    student_enquiry = get_object_or_404(StudentEnquiryModel,id=id)
    student_enquiry.directors_meeting = False
    student_enquiry.save()
    Data = StudentEnquiryModel.objects.all()
    # return redirect("admin_student_enquiry_table")
    return redirect('/adminpage/?open=student_enquiry')


def admin_Delete_student_enquiry (request,id):   
    try:
        student_emquiry = StudentEnquiryModel.objects.get(pk=id)
        student_emquiry.delete()
    except StudentEnquiryModel.DoesNotExist:
        messages.error(request,"student_enquiry Does not exist")
    # return redirect("admin_student_enquiry_table")
    return redirect('/adminpage/?open=student_enquiry')



def admin_add_remark(request, id):
    enquiry = get_object_or_404(StudentEnquiryModel, id=id)

    if request.method == "POST":
        remark_text = request.POST.get("remark")
        enquiry.remark = remark_text
        # enquiry.is_read = True
        enquiry.is_recent = False
        enquiry.save()
        # return redirect('admin_student_enquiry_table')  # go back to recent enquiries
        return redirect('/adminpage/?open=student_enquiry')

    

