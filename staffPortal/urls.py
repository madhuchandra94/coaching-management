from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static
from . import views 
urlpatterns = [
    #Staff Registration================
    path('staffreg/',views.StaffRegistration, name = "staffRegistration"),
    path('stafflogin/',views.StaffLoginView, name = "stafflogin"),

    #Staff Administrator===============
    path('staffadministrator/',views.staffAdminView, name = "staffAdministrator"),
    # path('staffadministrator/',views.staffAdminView, name ='staffAdmin'),

    # Counseller Dashboard=============
    path('counsellerDashboard/',views.counsellerDashboard, name="counsellerDashboard"),
    path('counsellor_pannel_student_enquiry',views.counsellor_pannel_student_enquiry, name="counsellor_pannel_student_enquiry"),
    path('add_remark/<int:id>/',views.add_remark, name="add_remark"),
    path('activate_student_enquiry/<int:id>',views.activate_student_enquiry,name="activate_student_enquiry"),
    path('deactivate_student_enquiry/<int:id>',views.deactivate_student_enquiry,name="deactivate_student_enquiry"),
    path('Delete_student_enquiry/<int:id>',views.Delete_student_enquiry,name="Delete_student_enquiry"),
    path('add_remark/<int:id>/',views.add_remark, name = "add_remark"),


    # Employee Table===================
    path('employeetable/',views.employeeTable, name="employeetable"),

    # Student Enquiry Form=============
    path('student-enquiry-form/',views.enquiryForm, name = 'enquiryForm'),

    path("Student-Enquiry-Table/",views.StudentEnquiryTable, name = "studentEnquiryTable"),
    
    path("toggle-enquiry/<int:id>/", views.toggleEnquiryStatus, name="toggleEnquiryStatus"),

    path("update-enquiry/<int:id>/",views.update_Enquiry_Details, name = "updateEnquiry"),
    path("delete-enquiry/<int:id>/",views.delete_Enquiry_Details, name = "deleteEnquiry"),

    path('export-students-excel/', views.export_students_excel, name='export_students_excel'),

    # search Bar for searching Student enquiry data=============
    path('search-student/',views.search_student_enquiry_details, name="searchStudentEnquiry"),

    # TRAINER DASHBOARD ======================================
    path('trainersdashboard/',views.trainersDashboard, name="trainersdashboard"),
    path('classAdd/',views.addingClass, name="classAdd"),
    path('class/edit/', views.edit_class, name='edit_class'),
    path('class/delete/', views.delete_class, name='delete_class'),

    # Counseller DASHBOARD ====================================
]
# Serve media files in development only=================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)