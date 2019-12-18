from django.shortcuts import render
from django.http import JsonResponse
from .models import *


# Create your views here.


def getAnnounce(request):
    announcements = announcement.objects.values(*["id", "content", "createdTime", "title"])
    results = sorted(announcements, key=lambda announceObj: announceObj['id'], reverse=True)

    return JsonResponse({'results': results}, safe=False)

