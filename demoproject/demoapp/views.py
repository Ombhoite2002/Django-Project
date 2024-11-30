from django.shortcuts import render
from .models import DemoGallery
from django.shortcuts import get_object_or_404

def demohome(request):
    photos = DemoGallery.objects.all()
    return render(request,'demoapp\demohome.html',{'photos':photos})

def img_info(request,photo_id):
    photo = get_object_or_404(DemoGallery,pk=photo_id)
    return render(request,'demoapp\img_info.html',{'photo':photo})
