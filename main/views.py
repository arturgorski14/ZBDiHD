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
    reviews = Review.objects.filter(movie=id).order_by('-comment')  # idk why '-comment' instead of 'comment'

    context = {
        'movie': movie,
        'reviews': reviews
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


def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == 'POST':
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect('main:detail', id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {'form': form})
    else:
        return redirect('accounts:login')


# edit the review
def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)

        review = Review.objects.get(movie=movie, id=review_id)

        if request.user == review.user:
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('main:detail', movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {'form': form})
        else:
            return redirect('main:detail', movie_id)
    else:
        return redirect('accounts:login')
