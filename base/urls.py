from django.urls import path
from . import views
from users import views as users_views
urlpatterns =[
    path('', views.Home, name='home_page'),
    path('login_u', users_views.u_login, name='loginPage'),
    path('reg_us', users_views.register, name='register'),
    path('us_prof', users_views.profile, name='profile'),
    # path('logout/', users_views.logout.as_view(template_name='users/userlogout.html'), name='logout'),
    path('logout', users_views.logout, name='logout'),
    # path('logout', users_views.logout, name='logout'),
    path('create-v', views.createVac, name='create_vacancy'),
    path('create-q', views.createQuiz, name='create_quiz'),
    path('delete-v/<int:pk>', views.deleteVac, name='delete_vacancy'),
    path('upd-v/<int:pk>', views.updateVac, name='update_vacancy'),
    path('v-dtls/<int:pk>', views.vacancies, name='vacancy_details'),
    path('quiz/<int:pk>', views.show_quiz, name='quiz'),
    path('developers/<slug:d_slug>', views.show_devs, name='devs'),
]