from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from finalapp5.models import Movie
from django.db.models import Q


# Create your views here.

def SearchResult(request):
    movies=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movies=Movie.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        return render(request,'search.html',{'query':query,'movies':movies})

