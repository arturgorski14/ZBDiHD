from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:id>/', views.detail, name='detail'),
    path('addgames/', views.add_games, name='add_games'),
    path('editgames/<int:id>/', views.edit_games, name='edit_games'),
    path('deletegames/<int:id>', views.delete_games, name='delete_game'),
    path('addreview/<int:id>', views.add_review, name='add_review'),
    path('editreview/<int:game_id>/<int:review_id>', views.edit_review, name='edit_review'),
    path('deletereview/<int:game_id>/<int:review_id>', views.delete_review, name='delete_review'),
]
