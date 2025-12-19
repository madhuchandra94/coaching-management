from django.urls import path
from . import views 

urlpatterns = [
    path('adminpage/',views.AdminPageView, name = 'adminpage'),
    path('adminlogin/',views.LoginPageView, name = 'loginPage'),

    path('createrole/',views.CreateRole, name = "CreateRole"),
    path('showroletable/',views.showRoleTable, name= 'showRoleTable'),
    path('role/update/<int:id>',views.updateRoleData, name = "update"),
    path('role/delete/<int:id>',views.deleteRoleData, name = 'delete'),
    
    path('logOut/',views.LogOut, name = 'logOut'),
    
    path('admin-employeetable/',views.employeeTable, name = 'employeeTable'),
    path('toggle-employee/<int:id>',views.toggleEmployeeStatus,name="toggleEmployee"),
    path('employee-update/<int:id>',views.update_employee_details, name ='employee_update'),
    path('employee-delete/<int:id>',views.delete_employee_details, name="employee_delete"),
    
    path('studentcourse/',views.createCourse, name = 'createCourse'),
    path('studentcourse/update/<int:id>/', views.updateCourseData, name='updateCourse'),
    path('studentcourse/delete/<int:id>/', views.deleteCourseData, name='deleteCourse'),
        
    # search Bar for searching Student enquiry data
    path('seach-student/',views.search_student_enquiry, name="searchEnquiry"),

    # search Bar for searching Student enquiry data
    path('seach-employee/',views.search_Employee_details, name="searchEmployee"),

    # Counsellor Dashboard
    # path('admincounsellerDashboard/',views.admin_counsellerDashboard, name="admincounsellerDashboard"),
    path('admin_student_enquiry_table',views.admin_student_enquiry_table, name="admin_student_enquiry_table"),
    path('admin_student_recent_enquiry',views.admin_student_recent_enquiry, name="admin_student_recent_enquiry"),
    path('admin_add_remark/<int:id>/',views.admin_add_remark, name="admin_add_remark"),
    path('admin_activate_student_enquiry/<int:id>',views.admin_activate_student_enquiry,name="admin_activate_student_enquiry"),
    path('admin_deactivate_student_enquiry/<int:id>',views.admin_deactivate_student_enquiry,name="admin_deactivate_student_enquiry"),
    path('admin_Delete_student_enquiry/<int:id>',views.admin_Delete_student_enquiry,name="admin_Delete_student_enquiry"),
    path('admin_add_remark/<int:id>/',views.admin_add_remark, name = "admin_add_remark"),

]