from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    path("", views.quotes, name='quotes'),
    path("all/", views.quotes, name='quotes'),
    path("<int:quote_id>/", views.quote_by_id, name='quote_by_id'),
    path("<str:author>/", views.quote_by_author, name='quote_by_author'),
    path("api/quotes/", views.QuotesView.as_view(), name="api_quotes"),
    path("api/quotes/<int:quote_id>/", views.delete_quote, name="api_quotes_delete"),
]
