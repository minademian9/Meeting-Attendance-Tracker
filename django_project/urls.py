"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meeting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('newmember/', views.newmember, name='newmember'),
    path('export/', views.export, name='export'),
    path('import/', views.data_import, name='import'),
    path('db/', views.download_database, name='download_db'),

    #POST Methods
    path('addattendance/', views.add_attendance, name='addattendance'),
    path('addmember/', views.add_new_member, name='addnewmember'),
    path('importdata/', views.importdata, name='importdata'),

    # ex: /bet/details/
    # path('bets/', views.details, name='details'),
    # path('placebet/', views.addBet, name='placingbet'),
    # path('account/', views.accountView, name='myaccount'),
    # path('mybetslist/', views.userbets, name='viewbetslist'),
    # path('leadershipboard/', views.leaderboardView, name='leadershiptop'),
    # path('allbets/', views.allbets, name='all_bets'),

    # POST urls
    # path('addbet/', views.post_new_bet, name='addingbettoDB'),
    # path('mybet/', views.post_bet_choice, name='addingChoicetoDB'),
    # path('closebet/', views.close_bet, name='addingClosureBettoDB'),

    # Login

    # path('login/',LoginView.as_view(),name="login_url"),
    # path('logout/',LogoutView.as_view(next_page='/'),name="logout"),
]
