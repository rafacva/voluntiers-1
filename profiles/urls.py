from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/vaga/new/',
        views.DashboardVaga.as_view(),
        name='dashboard_vaga_new'
    ),
    path(
        'dashboard/vaga/delete/',
        views.DashboardVagaDelete.as_view(),
        name='dashboard_vaga_delete'
    ),
    path(
        'dashboard/vaga/<int:id>/edit/',
        views.DashboardVaga.as_view(),
        name='dashboard_vaga_edit'
    ),
]
