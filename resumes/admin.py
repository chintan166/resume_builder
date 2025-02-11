from django.contrib import admin
from .models import UserProfile,ResumeTemplate,Resume,ResumeOrder,Contact

class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'preview_image')
# Register your models here.

class ResumeOrderAdmin(admin.ModelAdmin):
    list_display = ("full_name","payment_status")

admin.site.register(UserProfile)
admin.site.register(ResumeTemplate,ResumeTemplateAdmin)
admin.site.register(Resume)
admin.site.register(ResumeOrder,ResumeOrderAdmin)
admin.site.register(Contact)

