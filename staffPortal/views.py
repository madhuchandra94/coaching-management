from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import staffRegistrationModel, Country, State, City, StudentEnquiryModel, TrainersClassSchedule
from superadmin.models import roleModel, loginModel, studentCourses
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db.models import Q
import pandas as pd
# from staffPortal.models import Country, City, State
# Create your views here.


# import csv
# # Import countries
# with open('staffPortal/dataset/countries.csv' , encoding='utf-8', errors='ignore') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         Country.objects.create(name=row['name'])

# # Import states
# with open('staffPortal/dataset/states.csv' , encoding='utf-8', errors='ignore') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         country = Country.objects.get(id=row['country_id'])
#         State.objects.create(name=row['name'], country=country)

# # Import cities
# with open('staffPortal/dataset/cities.csv' , encoding='utf-8', errors='ignore') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         state = State.objects.get(id=row['state_id'])
#         City.objects.create(name=row['name'], state=state)




# =====================
# Staff Registration
# =====================

def StaffRegistration(request):
    # countries = Country.objects.all()  # define outside POST

    if request.method=="POST":
        # personal Details
        name = request.POST.get('name').strip()
        f_h = request.POST.get('f_h').strip()
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')

        # contact details
        email = request.POST.get('email').strip().lower()
        mobile = request.POST.get('mobile').strip()
        address = request.POST.get('address')
        country_id = request.POST.get('country')
        
        state_id = request.POST.get('state')
        state = State.objects.get(id=state_id)

        city_id = request.POST.get('city')
        city = City.objects.get(id=city_id)

        pincode = request.POST.get('pincode','').strip()

        # account security
        password = request.POST.get('password')
        con_password = request.POST.get('con_password')

        # address = request.POST.get('address', '').strip()
        # if not address:
        #     messages.error(request, "Address is required")
        #     return redirect("staffRegistration")
        # print(request.POST)
        # print(request.POST.get('address'))
        # print(f"The Address is :{address}")

        
        # Designation
        role_id = request.POST.get('role')
        role_instance = roleModel.objects.get(id=role_id) if role_id else None 

        # Document Upload
        adhar_upload = request.FILES.get('adhar_upload')
        pan_upload = request.FILES.get('pan_upload')
        
        # Educational details
        highest_qualification = request.POST.get('qualification')
        specialization = request.POST.get('specialization')
        passing_year = request.POST.get('passing_year')
        college = request.POST.get('college_university')
        percentage = request.POST.get('percentage_cgpa')

        # Professional Details
        work_status = request.POST.get('work_status')
        company_name = request.POST.get('Company_name')
        job_title = request.POST.get('Post_Name')
        experience = request.POST.get('Total_Experience')
        notice_period = request.POST.get('Notice_period')

        salary = request.POST.get('Salary')
        if salary in ("", None):
            salary = 0
        else:
            try: 
                salary = int(salary)
            except ValueError:
                raise ValueError("Salary Must Be a Number")



        salary_slip = request.FILES.get('salary_slip')

        agree_value = bool(request.POST.get('agree'))
        
    
        # -------------------
        # Validations
        # -------------------
        if staffRegistrationModel.objects.filter(email=email).exists():
            messages.warning(request, "This email is already registered!")
            return redirect("staffRegistration")
        
        if password != con_password:
            messages.warning(request, "Passwords do not match!")
            return redirect("staffRegistration")

        if not password or len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters long")  
            return redirect("staffRegistration")

        try:
            country = Country.objects.get(id=country_id)
        except (Country.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select a valid country")
            return redirect("staffRegistration")
        
        try:
            state = State.objects.get(id=state_id)
        except (State.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select a valid state")
            return redirect("staffRegistration")

        try:
            city = City.objects.get(id=city_id)
        except (City.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select a valid city")
            return redirect("staffRegistration")


        # Hash password Before Save
        hashed_password = make_password(password)

        # Create User or Saving the details in the Database
        staffRegistrationModel.objects.create(
            # personal Details
            name=name,
            f_h=f_h,
            dob=dob,
            gender=gender,

            # contact Details
            email=email,
            mobile=mobile,
            address=address,
            country=country,
            state=state,
            city=city,
            pincode=pincode,
            
            # Account Security
            password=hashed_password,
            # confirm_password=hashed_password,
            
            # Designation
            role = role_instance,

            # Educational Details
            highest_qualification=highest_qualification,
            specialization=specialization,
            passing_year=passing_year,
            college=college,
            percentage=percentage,

            #Professional details
            work_status=work_status,
            company_name=company_name,
            job_title=job_title,
            total_experience= experience,
            notice_period=notice_period,
            salary = salary,
            salary_slip=  salary_slip,
            
            # document Upload
            adhar=adhar_upload,
            pan=pan_upload,
            agree=agree_value
        )

        messages.success(request, "User Registered Successfully. Please log in.")
        return redirect("stafflogin")
    
    # For GET request - Load data
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    role = roleModel.objects.all()
    all_record = staffRegistrationModel.objects.all()

    return render(request, 'staffPortal/Registration.html',{'country':country, 
                                                            "state":state, 
                                                            "city":city, 
                                                            'role':role, 
                                                            'data':all_record})


# ==================================================================
# Staff Login
# ==================================================================

def StaffLoginView(request):
    if request.method=="POST":

        # Getting Email and Password from Login Form
        email = request.POST.get("email").strip().lower()
        password = request.POST.get('password').strip()
                             
        try:
            # Get Staff By Email
            staff = staffRegistrationModel.objects.get(email=email)

            # check if is_active True or False
            if not staff.is_active:
                messages.error(request, "Your Account is Not Active Yet. Please Contact admin !")
                return redirect('stafflogin')

            # Role Check : Only Administrator can login to Enquiry form
            if staff.role.role == "Administrator":
    
                # checking and Comparing Hashed Password
                if check_password(password, staff.password):

                    # Creating Sessions
                    request.session['staff_id'] = staff.id
                    request.session['staff_email'] = staff.email
                    request.session['staff_role']  = staff.role.role

                    messages.success(request, 'Login Successfull as Administrator')
                    return redirect('staffAdministrator')
                else:
                    messages.error(request, "Invalid Password")
                    return redirect("stafflogin")
            else:
                messages.error(request,'Only Administrator Can Login Here!')
                return redirect('stafflogin')
            
        except staffRegistrationModel.DoesNotExist:
            messages.error(request, "Email Not Found")
            return redirect('stafflogin')
 
    return render(request, 'staffPortal/stafflogin.html')


# ====================================================================
# Staff Admin Dashboard
# ====================================================================

def staffAdminView(request):
    enquiry_data = StudentEnquiryModel.objects.all()  # fetch all records
    courses = studentCourses.objects.all() # fetch all courses
    return render(request, 'staffPortal/staffAdministrator.html',{
        'Administrator':request.session.get('email'),
        'enquiry_data':enquiry_data, 
        'courses':courses})


# ====================================================================
# Employee Table
# ====================================================================

def employeeTable(request):
    all_record = staffRegistrationModel.objects.all()
    return render(request, 'staffPortal/staffRecord.html',{'data':all_record})



# ====================================================================
# Student Enquiry Form 
# ===================================================================


def enquiryForm(request):
    if request.method == "POST":
         # Personal Detials
         stu_name = request.POST.get('student_name')
         stu_f_h = request.POST.get('f/h_name')
         stu_dob = request.POST.get('DOB')
         stu_gender = request.POST.get('gender')

         # contact details
         stu_email = request.POST.get("email")
         stu_mobile = request.POST.get("number", "").strip()
         stu_address = request.POST.get("address")

         country_id = request.POST.get("country")

         state_id = request.POST.get('state')
        #  stu_state = State.objects.get(id=state_id)

         city_id = request.POST.get('city')
        #  stu_city = City.objects.get(id=city_id)

         stu_pincode = request.POST.get("pincode")

         # Educational Details
         stu_educational_status = request.POST.get("edu_status")
         stu_school = request.POST.get("school")
         stu_course = request.POST.get("course")
         stu_college = request.POST.get("college_university")
         stu_branch = request.POST.get("branch")
         stu_passing_year = request.POST.get("passing_year")
         stu_percentage = request.POST.get("percentage_cgpa", "").strip()


         # Professional / WORK EXPERIENCE
         stu_work_status = request.POST.get("work")
         stu_company =  request.POST.get("c_name")
         stu_experience = request.POST.get("total_exp")
         stu_notice_period = request.POST.get("notice_period")
         stu_job_title = request.POST.get('designation')
         stu_salary = request.POST.get("salary", "").strip()

         # Documents upload
         stu_salary_slip = request.FILES.get("salary_slip")
         stu_adhar = request.FILES.get('adhar')

         # Student Course
         course_id = request.POST.get("intrested_course")
         if course_id:
             stu_intrested_course = studentCourses.objects.get(id = course_id)

         # Administrator Name for Taking Enquiry
         Enquiry_person_id = request.POST.get('Enquiry_person_name')
         if Enquiry_person_id:
             Enquiry_person_name = staffRegistrationModel.objects.get(id=Enquiry_person_id)
         #agree 
         agree = bool(request.POST.get("agree"))


         #=====================
         # Validation
         #=====================
         if StudentEnquiryModel.objects.filter(email=stu_email).exists():
            messages.warning(request, "This email is already Registered!")
            return redirect('enquiryForm')

         if StudentEnquiryModel.objects.filter(mobile=stu_mobile).exists():
             messages.warning(request, "This Mobile Number is already Registered!")
             return redirect("enquiryForm")
        # checking length of mobile number and mobile is in digit formate        
         if not stu_mobile.isdigit() or len(stu_mobile) !=10:
             messages.error(request, "Mobile number must be 10 digits")
             return redirect('enquiryForm')

        #percentage numeric check
         if stu_percentage:
            try:
                stu_percentage = float(stu_percentage)
            except ValueError:
                messages.error(request, "Percentage/CGPA must be a numeric Value")
                return redirect('enquiryForm')
         else:
             stu_percentage = None # if left empty

        # Salary Integer Check
         if stu_salary:
            try:
                stu_salary = int(stu_salary)
            except ValueError:
                messages.error(request, "Salary must be Number")
                return redirect('enquiryForm')
         else:
             stu_salary = 0 # default if empty

         try:
             stu_country = Country.objects.get(id=country_id)
         except(Country.DoesNotExist):
             messages.error(request,"Please Select a valid country")
             return redirect("enquiryForm")

         try:
             stu_state= State.objects.get(id=state_id)
         except(State.DoesNotExist):
             messages.error(request, "Please Select a valid State")
             return redirect('enquiryForm')

         try:
             stu_city = City.objects.get(id=city_id)
         except(City.DoesNotExist, ValueError, TypeError):
             messages.error(request, 'Please Select a valid city')
             return redirect('enquiryForm')

        # Saving to DB----------------------------
         # Create User or Saving the details in the Database
         StudentEnquiryModel.objects.create(
             # Personal Details
             name = stu_name,
             f_h = stu_f_h,
             dob = stu_dob,
             gender = stu_gender,

             # Course Detials
             course = stu_intrested_course,

             # Contact details
             email = stu_email,
             address= stu_address,
             mobile = stu_mobile,
             country = stu_country,
             state = stu_state,
             city = stu_city,
             pincode = stu_pincode,

             # Educational Details
             highest_qualification = stu_educational_status,
             school_name = stu_school,
             course_name = stu_course,
             college_name = stu_college,
             branch_name = stu_branch,
             passing_year = stu_passing_year,
             percentage = stu_percentage,

             # Professional / Work Experience
             work_status = stu_work_status,
             company_name = stu_company,
             total_experience = stu_experience,
             job_title = stu_job_title,
             notice_period = stu_notice_period,
             salary = stu_salary,

            # # Administrator Name for Taking Enquiry
            Enquiry_person = Enquiry_person_name,

             # Documents upload
             salary_slip=stu_salary_slip,
             adhar = stu_adhar,


             # agree
             agree = agree,
             is_recent=True,
         )
         messages.success(request,"Student Registered Successfully.")
         return redirect("staffAdministrator")

    # for GET REQUEST - LOAD DATA
    course_obj = studentCourses.objects.all()
    country_obj = Country.objects.all()
    state_obj = State.objects.all()
    city_obj = City.objects.all()
    all_record = StudentEnquiryModel.objects.all()
    employeeDetails = staffRegistrationModel.objects.all()

    return render(request,"staffPortal/EnquiryForm.html", {'country':country_obj, 
                                                        'state':state_obj,
                                                        'city':city_obj,
                                                        'courses':course_obj,
                                                        'data': all_record,
                                                        'employee':employeeDetails})



#==================================================================
# Enquiry Table
#==================================================================

def StudentEnquiryTable(request):
    enquiry_data = StudentEnquiryModel.objects.all().order_by('-id')
    return render(request,"staffPortal/staffAdministrator.html",{'enquiry_data':enquiry_data})





#==================================================================
# Toggle Meeting Status Active status or Deactive Status
#==================================================================

def toggleEnquiryStatus(request,id):
    Enquiry = get_object_or_404(StudentEnquiryModel, id=id)
    Enquiry.directors_meeting = not Enquiry.directors_meeting
    Enquiry.save()
    status = "Yes" if Enquiry.directors_meeting else "No"
    messages.success(request, f"{Enquiry.name} has been {status} Succesfully.")
    return redirect('staffAdministrator')




#===================================================================
# Update Student Enquiry Details
#===================================================================


def update_Enquiry_Details(request, id):
    #getting old record
    staff = get_object_or_404(StudentEnquiryModel, id=id)

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





#=====================================================================
# Deleting Student Enquiry Details
#=====================================================================

def delete_Enquiry_Details(request, id):
    instance = get_object_or_404(StudentEnquiryModel, pk=id)
    instance.delete()
    messages.success(request,"Enquiry Details Deleted Successfully")
    
    all_details = staffRegistrationModel.objects.all().order_by('-id')
    return render(request, 'superadmin/adminPage.html',{'employees':all_details})
    # return redirect('staffAdministrator')



#=====================================================================
# Search Student 
#=====================================================================
# showing data with query selector
def search_student_enquiry_details(request):
    query = request.GET.get('q') # Take search input from url
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
        context = {"enquiry_data":enquiry_data}
        return render(request, 'staffPortal/staffAdministrator.html',context) # showing table with searching data
    else:
        # showing all table if there is no search
        enquiry_data = StudentEnquiryModel.objects.all()
    
        context = {"enquiry_data":enquiry_data, 'query':query}
        return render(request, 'staffPortal/staffAdministrator.html',context) # showing table with searching data



#=====================================================================
# Trainer Dashboard
#=====================================================================
def trainersDashboard(request):
    classes = TrainersClassSchedule.objects.all().order_by('-startingDate', 'startingTime')
    context = {'classes':classes}
    return render(request,'staffPortal/Trainer_dashboard.html',context)

def addingClass(request):
    if request.method == "POST":
        trainerObj = TrainersClassSchedule()
        trainerObj.className = request.POST['class_name']
        trainerObj.startingTime = request.POST['class_starting_Time']
        trainerObj.endingTime = request.POST['class_Ending_Time']
        trainerObj.startingDate = request.POST['class_Starting_Date']
        trainerObj.save()
        messages.success(request,"Class Added Successfully")
        return redirect('trainersdashboard')
    else:
        return render(request,'staffPortal/Trainer_dashboard.html')

# def edit_class(request):
#     """
#     Update a TrainersClassSchedule object. Expects POST with:
#       - eid (id)
#       - class_name
#       - class_starting_Time
#       - class_Ending_Time
#       - class_Starting_Date
#     Redirects to 'trainerdashboard' after success/error.
#     """
#     if request.method != "POST":
#         messages.error(request, "Invalid request method for editing class.")
#         return redirect('trainerdashboard')
    
#     class_id = request.POST.get('eid')
#     if not class_id:
#         messages.error(request, "Class id missing.")
#         return redirect('trainerdashboard')
#     # fetch instance or 404
#     try:
#         cls = get_object_or_404(TrainersClassSchedule, id =int(class_id))
#     except (ValueError,TypeError):
#         messages.error(request, "Invalid class id")
#         return redirect("trainersdashboard")
#     # read fields from POST; use .get() to avoid KeyError
#     class_name = request.POST.get('class_name','').strip()
#     starting_time = request.POST.get('class_starting_Time','').strip()
#     ending_time = request.POST.get('class_Ending_Time',"").strip()
#     starting_date = request.POST.get('class_Starting_Date','').strip()

#      # Basic validation (expand as needed)
#     if not class_name:
#         messages.error(request, "Class name cannot be empty.")
#         return redirect('trainerdashboard')

#     # assign and save
#     cls.className = class_name
#     cls.startingTime = starting_time
#     cls.endingTime = ending_time
#     cls.startingDate = starting_date
#     cls.save()
#     messages.success(request,"class Updated successfully")
#     return redirect("trainersdashboard")

def delete_class(request):
    """
    Show confirmation (GET). Perform deletion on POST and redirect.
    """
    class_id = request.GET.get('eid')
    
    if not class_id:
        messages.error(request,"Invalid class Id")
        return redirect("delete_class")
    try:
        cls = get_object_or_404(TrainersClassSchedule, id=class_id)
        cls.delete()
        messages.success(request,"class deleted successfully")
    except TrainersClassSchedule.DoesNotExist:
        messages.error(request, "class Not Found.")

    return redirect('trainersdashboard')


def edit_class(request):
    """
    Manual edit (no ModelForm).
    - GET ?eid=<id> -> show manual edit form
    - POST -> update instance (expects hidden 'eid' in POST)
    """
    if request.method == "GET":
        class_id = request.GET.get('eid')
        if not class_id:
            messages.error(request, "No class id provided.")
            return redirect('trainerdashboard')

        cls = get_object_or_404(TrainersClassSchedule, id=class_id)
        # Render manual edit template (no ModelForm)
        return render(request, 'staffPortal/Trainer_dashboard.html', {'cls': cls})

    # POST -> perform update
    if request.method == "POST":
        class_id = request.POST.get('eid')
        if not class_id:
            messages.error(request, "Missing class id.")
            return redirect('trainersdashboard')

        # Safely fetch instance
        try:
            cls = get_object_or_404(TrainersClassSchedule, id=int(class_id))
        except (ValueError, TypeError):
            messages.error(request, "Invalid class id.")
            return redirect('trainersdashboard')

        # Read posted values (use .get to avoid KeyError)
        class_name = request.POST.get('class_name', '').strip()
        starting_time = request.POST.get('class_starting_Time', '').strip()
        ending_time = request.POST.get('class_Ending_Time', '').strip()
        starting_date = request.POST.get('class_Starting_Date', '').strip()

        # Basic validation
        if not class_name:
            messages.error(request, "Class name cannot be empty.")
            return redirect(f"{request.path}?eid={cls.id}")

        # Assign and save
        cls.className = class_name
        cls.startingTime = starting_time
        cls.endingTime = ending_time
        cls.startingDate = starting_date
        cls.save()

        messages.success(request, "Class updated successfully.")
        return redirect('trainersdashboard')




#=====================================================================
# Converting Table into Excel File
#=====================================================================
# views.py

def export_students_excel(request):
    # Fetch all data from your model
    students = StudentEnquiryModel.objects.all().values()

    # Convert QuerySet → DataFrame
    df = pd.DataFrame(students)

    # Create Excel response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="students_data.xlsx"'

    # Write data to Excel file in memory
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    return response


# ============================== Counseller Dashboard ========================

def counseller_pannel_student_enquiry(request):
    return render(request, 'staffPortal/counseller.html')

def counsellerDashboard(request):
    data = StudentEnquiryModel.objects.filter(remark__isnull=True, is_recent=True)
    unread_count = StudentEnquiryModel.objects.filter(remark__isnull=True).count()

    context = {
        "recent_enquiry": True,
        "show_student_enquiry": False,
        "unread_count": unread_count,
        "data": data,
    }
    return render(request, "staffPortal/counseller.html", context)


def counsellor_pannel_student_enquiry(request):
    data = StudentEnquiryModel.objects.filter(remark__isnull=False, is_recent=False)

    context = {
        "recent_enquiry": False,
        "show_student_enquiry": True,
        "data": data
    }
    return render(request, "staffPortal/counseller.html", context)


def activate_student_enquiry(request,id):
    student_enquiry = get_object_or_404(StudentEnquiryModel,id=id)
    student_enquiry.directors_meeting = True
    student_enquiry.save()
    Data = StudentEnquiryModel.objects.all()
    return redirect("counsellerDashboard")


def deactivate_student_enquiry(request,id):
    student_enquiry = get_object_or_404(StudentEnquiryModel,id=id)
    student_enquiry.directors_meeting = False
    student_enquiry.save()
    Data = StudentEnquiryModel.objects.all()
    return redirect("counsellerDashboard")

def Delete_student_enquiry (request,id):   
    try:
        student_emquiry = StudentEnquiryModel.objects.get(pk=id)
        student_emquiry.delete()
    except StudentEnquiryModel.DoesNotExist:
        messages.error(request,"student_enquiry Does not exist")
    return redirect("counsellerDashboard")

def add_remark(request, id):
    enquiry = get_object_or_404(StudentEnquiryModel, id=id)

    if request.method == "POST":
        remark_text = request.POST.get("remark")
        enquiry.remark = remark_text
        # enquiry.is_read = True
        enquiry.is_recent = False
        enquiry.save()
        return redirect('counsellerDashboard')  # go back to recent enquiries
    
