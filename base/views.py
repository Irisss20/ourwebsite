from django import forms
from django.shortcuts import get_object_or_404, render, redirect  # render - обработка, redirect - перенаправление
from django.contrib import messages  # Для отображения ошибок, предупреждений и тд
from .models import QuizAdditionalField, Vacancy, DevGrades, Quiz
from .forms import QuizForm, VacForm 
from django.contrib.auth.decorators import login_required  # С этим можно настроить доступ, приватность 
from django.db.models import Q  # Для поиска 



def  Home(request):  
    q = request.GET.get('q') if request.GET.get('q') is not None else ''  # Временная q будет содержать значение параметра 'q' из запроса, если таковой присутствует, иначе она будет равна пустой строке. Это часто используется для обработки поисковых запросов или других параметров веб-страницы.
    vacancies = Vacancy.objects.filter(
                                Q(devgrade__name__icontains=q) |
                                Q(name__icontains=q) or
                                Q(employer__icontains=q)
                                )  # Параметр __icontains считывает прописные и строчные символы по заданоому имени, немного различается, нежели __contains
    devgrades = DevGrades.objects.all()
    vacancy_count = vacancies.count()  # Функция count() считает автоматически количество объектов
    context = {'devgrades': devgrades, 'vacancy_count': vacancy_count, 'vacancies': vacancies}  # Для вывода в фронт сайта
    return render(request, 'base/home_page.html', context)

def about_us(request):
    return render(request, 'base/about_us.html')

def news(request):
    return render(request, 'base/news.html')

def show_devs(request, d_slug):
    devs = get_object_or_404(DevGrades, slug=d_slug)
    vacancies = Vacancy.objects.filter(devgrade=devs.pk)
    vacancy_count = vacancies.count()  # Функция count() считает автоматически количество объектов

    context = {
     'devs': devs.pk,
     'vacancies': vacancies,
     'vacancy_count': vacancy_count,
    }
    return render(request, 'base/home_page.html', context)

def vacancies(request, pk):  # pk это специальное выражение для обозначения уникальной идентификации каждой записи 
    vacancy = Vacancy.objects.get(id=pk) 
     
    context = {'vacancy': vacancy}
    return render(request, 'base/vacancy_details.html', context)

def vacancies_list(request):
    vac_list = Vacancy.objects.all()
    
    context ={'vac_list': vac_list}
    return render(request, 'navbar.html', context)

@login_required(login_url='/login')
def createVac(request):
    vac_form = VacForm()

    if request.method == "POST":
        vac_form = VacForm(request.POST)
        if vac_form.is_valid():
            vac_form.save()
            return redirect('create_quiz')

    context = {'vac_form': vac_form}
    return render(request, 'base/create_vacancy.html', context)

def createQuiz(request):
    quiz_form = QuizForm()

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz_instance = quiz_form.save()

            for key, value in request.POST.items():
                if key.startswith('additional_field_'):
                    field_name = key[len('additional_field_'):]
                    QuizAdditionalField.objects.create(quiz=quiz_instance, field_name=field_name, value=value)
                    quiz_form.save()
            return redirect('home_page')

    else:
        additional_field_form = QuizForm()
        
    context ={
        'quiz_form': quiz_form,
        'additional_field_form': additional_field_form,
        }
    return render(request, 'base/create_quiz.html', context)

def show_quiz(request, pk):
    # if request.method == 'GET':
    vacancy = Vacancy.objects.get(id=pk)
    quiz = Quiz.objects.filter(vacancy=vacancy)


    context = {
        'quiz': quiz,
    }
    return render(request, 'base/quiz.html', context)


# def dynamic_form(request):
#     # Initial form
#     field_form = Quiz.objects.all()
#     vac_form = VacForm()

#     # Add dynamically generated fields based on the GET parameter
#     num_dynamic_fields = int(request.GET.get('num_dynamic_fields', 0))
#     for i in range(num_dynamic_fields):
#         field_name = f'dynamic_field_{i}'
#         field_form.fields[field_name] = forms.CharField()

#     if request.method == 'POST':
#         field_form = QuizForm(request.POST)
#         if field_form.is_valid():
#             field_form.save()

#     context = {'field_form': field_form}
#     return render(request, 'base/create_vacancy.html', context)

@login_required(login_url='/')
def updateVac(request, pk):
    vacancy = Vacancy.objects.get(id=pk)
    form = VacForm(instance=vacancy)

    if request.method == 'POST':
        form = VacForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    context = {'form': form}
    return render(request, 'base/vacancy_form.html', context)

@login_required(login_url='/')
def deleteVac(request,pk):
    vacancy = Vacancy.objects.get(id=pk)

    if request.method == 'POST':
        vacancy.delete()
        return redirect('home_page')
    return render(request, 'base/delete_valid.html', {'obj': vacancy})

def info_view(request):
    # Ваш код для обработки запроса и формирования ответа
    return render(request, 'base/info_page.html')