from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

def home(request):
    all_movies = Movie.objects.all()

    context = {
        'movies': all_movies
    }

    return render(request, 'main/index.html', context)


def detail(request, id):
    movie = Movie.objects.get(id=id)

    context = {
        'movie': movie
    }

    return render(request, 'main/details.html', context)


# add movies to the database
def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = MovieForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('main:home')
            else:
                form = MovieForm()
            return render(request, 'main/addmovies.html', {'form': form,
                                                           'controller': 'Add Movies'})
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')


# edit the movie
def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)

            if request.method == 'POST':
                form = MovieForm(request.POST or None, instance=movie)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('main:detail', id)
            else:
                form = MovieForm(instance=movie)
            return render(request, 'main/addmovies.html', {'form': form,
                                                           'controller': 'Edit Movies'})
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')


# delete movies
def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)

            movie.delete()
            return redirect('main:home')
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')