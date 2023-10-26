from main_app import views
from django.urls import path
#from .views import CriterioAddView, AlternativaAddView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    # AUTH
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.update_profile, name='edit-profile'),
    # esqueci senha
    path('reset-password/', auth_views.PasswordResetView.as_view(),
         name='reset-password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('reset-password/', auth_views.PasswordResetCompleteView.as_view(),
         name='password-reset-complete'),
     # consultas
    path('consultas/', views.consultas, name='consultas'),
    path('consulta-create/', views.consultaCreate, name='consulta-create'),
    path('consulta-details/<int:idConsulta>/', views.consultaDetails, name='consulta-details'),
    path('consulta-delete/<int:idConsulta>/', views.consultaDelete, name='consulta-delete'),
    #pesquisa
    path('search/', views.search_view, name='search'),

]
