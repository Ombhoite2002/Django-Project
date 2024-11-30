from django.contrib import admin
from .models import DemoGallery, ImageReview

# Register your models here.

class ImageGalleryInline(admin.TabularInline):
    model = ImageReview
    fk_name = 'image'
    extra = 2

class DemoGalleryAdmin(admin.ModelAdmin):
    list_display = ('name','image','date_added','img_Description','img_Info')
    inlines = [ImageGalleryInline]


admin.site.register(DemoGallery, DemoGalleryAdmin)
