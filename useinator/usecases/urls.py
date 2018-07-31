from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('profile/', views.profile, name='profile'),
	path('create-usecase/quest/', views.quest, name='quest'),
	#path('create-usecase/quest/<slug:project_id>/', views.quest, name='quest'),
	path('create-usecase/', views.create_usecase, name='create_usecase'),
	path('diagram/', views.diagram, name='diagram')
]
 