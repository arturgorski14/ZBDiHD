from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg


def home(request):
    query = request.GET.get('title')
    all_games = None
    if query:
        all_games = Game.objects.filter(name__icontains=query)
    else:
        all_games = Game.objects.all()

    context = {
        'games': all_games
    }

    return render(request, 'main/index.html', context)


def detail(request, id):
    game = Game.objects.get(id=id)
    reviews = ReviewG.objects.filter(game=id).order_by('-comment')  # idk why '-comment' instead of 'comment'

    average = reviews.aggregate(Avg('rating'))['rating__avg']
    if average is None:
        average = 0
    average = round(average, 2)
    context = {
        'game': game,
        'reviews': reviews,
        'average': average
    }

    return render(request, 'main/details.html', context)


# add games to the database
def add_games(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = GameForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('main:home')
            else:
                form = GameForm()
            return render(request, 'main/addgames.html', {'form': form,
                                                           'controller': 'Add Games'})
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')


# edit the game
def edit_games(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            game = Game.objects.get(id=id)

            if request.method == 'POST':
                form = GameForm(request.POST or None, instance=game)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('main:detail', id)
            else:
                form = GameForm(instance=game)
            return render(request, 'main/addgames.html', {'form': form,
                                                           'controller': 'Edit Games'})
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')


# delete games
def delete_games(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            game = Game.objects.get(id=id)

            game.delete()
            return redirect('main:home')
        # if they are not admin
        else:
            return redirect('main:home')

    # if they are not logged in
    return redirect('accounts:login')


def add_review(request, id):
    if request.user.is_authenticated:
        game = Game.objects.get(id=id)
        if request.method == 'POST':
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                # check if user wrote review for this game
                try:
                    review_wrote_by_user = ReviewG.objects.get(game=game, user=request.user)
                    print(review_wrote_by_user)
                    print(review_wrote_by_user.id)
                    review_wrote_by_user.delete()
                except ReviewG.DoesNotExist:
                    print('ReviewG.DoesNotExist')
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.user = request.user
                data.game = game
                data.save()
                return redirect('main:detail', id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {'form': form})
    else:
        return redirect('accounts:login')


# edit the review
def edit_review(request, game_id, review_id):
    if request.user.is_authenticated:
        game = Game.objects.get(id=game_id)

        review = ReviewG.objects.get(game=game, id=review_id)

        if request.user == review.user or request.user.is_superuser:
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = 'Out of range. Please select rating from 0 to 10.'
                        return render(request, 'main/editreview.html', {'error': error, 'form': form})
                    else:
                        data.save()
                        return redirect('main:detail', game_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {'form': form})
        else:
            return redirect('main:detail', game_id)
    else:
        return redirect('accounts:login')


# delete the review
def delete_review(request, game_id, review_id):
    if request.user.is_authenticated:
        game = Game.objects.get(id=game_id)

        review = ReviewG.objects.get(game=game, id=review_id)

        if request.user == review.user or request.user.is_superuser:
            # grant permission to delete
            review.delete()

        return redirect('main:detail', game_id)
    else:
        return redirect('accounts:login')
