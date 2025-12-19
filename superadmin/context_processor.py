from staffPortal.models import StudentEnquiryModel

def unread_enquiry_count(request):
    return{
        "unread_count":StudentEnquiryModel.objects.filter(is_recent=True).count()
    }