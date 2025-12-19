from django.contrib import admin
from .models import loginModel, roleModel, studentCourses
from staffPortal.models import staffRegistrationModel
from django.utils.html import format_html

# Register your models here.
#===================
# Register loginModel and roleModel normally
#===================

admin.site.register(loginModel)
admin.site.register(roleModel)
admin.site.register(studentCourses)

#==================
#  Register staffRegistrationModel with all fields
#==================

@admin.register(staffRegistrationModel)
class StaffAdmin(admin.ModelAdmin):
    # -----------------------------
    # Display Aadhar as thumbnail
    # -----------------------------
    def adhar_thumb(self, obj):
        if obj.adhar:
            return format_html('<img src="{}" width="80" style="border-radius:5px;" />', obj.adhar.url)
        return "-"
    adhar_thumb.short_description = 'Aadhar'

    # -----------------------------
    # Display PAN as thumbnail
    # -----------------------------
    def pan_thumb(self, obj):
        if obj.pan:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.pan.url)
        return "-"
    pan_thumb.short_description = 'PAN'

    # Show all model fields dynamically
    dynamic_fields = [field.name for field in staffRegistrationModel._meta.fields if field.name != 'password']
    
    # Replace 'adhar' and 'pan' with custom thumbnail methods
    list_display = dynamic_fields + ['adhar_thumb', 'pan_thumb']

    # Make is_active editable in the list view
    list_editable = ('is_active',)
    
    # Optional: allow search by name, email, mobile
    search_fields = ('name', 'email', 'mobile')
    
    # Optional: filter by role, is_active, gender, country, state, city
    list_filter = ('role', 'is_active', 'gender', 'country', 'state', 'city')


    # -----------------------------
    # Custom display for role (ForeignKey)
    # -----------------------------
    def role_display(self, obj):
        return obj.role.role if obj.role else '-'
    role_display.short_description = 'Role'

