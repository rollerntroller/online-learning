from django.urls import path, include
from django.contrib.auth import views as auth_views
from learningportal.views import ContentDetailView, WatchListItemListView, Homepage, ContactCreate, MessageReceived, \
    SignUpView, ContentCreate, deleteFromWatchlist, UserContentList, SelectedUserContentList, addToWatchList, about

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    #path('user/login/', auth_views.LoginView.as_view()),
    path('user/watchlist/', WatchListItemListView.as_view(), name='watchlist-list'), #for user to view his watchlist
    path('user/<int:id>/content/', SelectedUserContentList.as_view(), name='selectedusercontent-list'), #for user to view uploads of himself or other users
    path('user/content/', UserContentList, name='usercontent-list'), #for user to view own uploads
    path('user/watchlist/delete/<slug:slug>/', deleteFromWatchlist, name="watchlist-delete"), #url used to delete an item from the user's watchlist
    path('user/watchlist/add/<slug:slug>/', addToWatchList, name="watchlist-add"), #url used to add items to user's watchlist
    path('user/signup/', SignUpView.as_view(), name='signup'), #basic registration page
    path('contact/', ContactCreate.as_view(), name='contactus-create'), #basic contact us page
    path('create/', ContentCreate.as_view(), name='content-create'),  #basic new post page. both for videos and rich text
    path('about/', about, name='about'), #basic about us page
    path('contactus/thankyou/', MessageReceived.as_view(), name='message_received'), #page to be viewed after contact form is sent
    path('learn/<slug:slug>/', ContentDetailView.as_view(), name='content-detail'), #view posts
]