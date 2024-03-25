from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage, EmptyPage, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from django.urls import reverse

from finalapp5.forms import MovieForm, UserProfileForm, ReviewForm
from finalapp5.models import Movie, Category


# Create your views here.
def register(request):
    if request.method== 'POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return redirect('/finalapp5')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email Taken")
                return redirect('/finalapp5')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email= email,password=password)


                user.save();
                return redirect('login.html')



        else:
               messages.info(request,"password not matching !")
               return redirect('/finalapp5')


        return redirect('/finalapp5')

    return render(request,"register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in !')
            return redirect('/finalapp5/allProdCat')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login.html')
    else:
        return render(request, 'login.html')

def allProdCat(request, c_slug=None):
    c_page = None
    movies_list = None
    user = request.user
    username = None

    if user.is_authenticated:
        username = user.username
        welcome_message = f"Welcome {username}!"
    else:
        welcome_message = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies_list = Movie.objects.all().filter(category=c_page, available=True)
    else:
        movies_list = Movie.objects.all().filter(available=True)

    paginator = Paginator(movies_list, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'movies': movies, 'username': username, 'welcome_message': welcome_message})




def proDetail(request,c_slug,movie_slug):
    try:
        movie=Movie.objects.get(category__slug=c_slug,slug=movie_slug)
    except Exception as e:
        raise e
    return render (request,'movie.html',{'movie':movie})

def browse(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.release_date = datetime.now()
            movie.save()
            return redirect('allProdCat/')
    else:
        form = MovieForm()
    movies = Movie.objects.all()
    return render(request, 'browse.html', {'form': form, 'movies': movies})
@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form=MovieForm(request.POST or None, request.FILES,instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/finalapp5/allProdCat')
    return render(request,'edit.html',{'form':form,'movie':movie})
from django.shortcuts import render, get_object_or_404

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if not can_delete_movie(request.user, movie):
        return HttpResponseForbidden()
    if request.method == 'POST':
        movie.delete()
        return redirect('/finalapp5/allProdCat')
    return render(request, 'delete.html', {'movie': movie})

def can_edit_movie(user, movie):
    """
    Returns `True` if the given user has permission to edit the given movie, and `False` otherwise.
    """
    return movie.user == user

def can_delete_movie(user, movie):
    """
    Returns `True` if the given user has permission to delete the given movie, and `False` otherwise.
    """
    return movie.user == user
def can_edit_movie(user, movie):
    return user.is_superuser
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('allProdCat/')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('/finalapp5/allProdCat')  # Use named URL pattern
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'movie': movie})

def logout(request):
    # Clear any messages before redirecting
    request.session.pop('msg', None)
    # Logout the user
    auth.logout(request)
    # Redirect to the '/finalapp5/' page
    return redirect('/finalapp5/')

