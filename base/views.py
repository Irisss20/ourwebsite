from django import forms
from django.shortcuts import get_object_or_404, render, redirect  # render - обработка, redirect - перенаправление
from django.contrib import messages  # Для отображения ошибок, предупреждений и тд
from .models import Vacancy, DevGrades, Quiz
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

def show_devs(request, d_slug):
    devs = get_object_or_404(DevGrades, slug=d_slug)
    vacancies = Vacancy.objects.filter(devgrade_id=devs.pk)
    vacancy_count = vacancies.count()  # Функция count() считает автоматически количество объектов

    context = {
     'devs': devs.pk,
     'vacancies': vacancies,
     'vacancy_count': vacancy_count  
    }
    return render(request, 'base/home_page.html', context)

def vacancies(request, pk):  # pk это специальное выражение для обозначения уникальной идентификации каждой записи 
    vacancy = Vacancy.objects.get(id=pk) 
    context = {'vacancy': vacancy}
    return render(request, 'base/vacancy_details.html', context)

@login_required(login_url='/')
def createVac(request):
    vac_form = VacForm()

    if request.method == "POST":
        vac_form = VacForm(request.POST)
        if vac_form.is_valid():
            vac_form.save()
            return redirect('home_page')

    context = {'vac_form': vac_form}
    return render(request, 'base/create_vacancy.html', context)

def dynamic_form(request):
    # Initial form
    quiz = Quiz.objects.all()
    field_form = VacForm()

    # Add dynamically generated fields based on the GET parameter
    num_dynamic_fields = int(request.GET.get('num_dynamic_fields', 0))
    for i in range(num_dynamic_fields):
        field_name = f'dynamic_field_{i}'
        field_form.fields[field_name] = forms.CharField()

    if request.method == 'POST':
        field_form = QuizForm(request.POST)
        if field_form.is_valid():
            field_form.save()

    context = {'field_form': field_form}
    return render(request, 'base/create_vacancy.html', context)

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

@login_required(login_url='/')
def createQuiz(request, pk):
    quiz_form = Quiz.objects.all()

    # if request.method = 'POST':
    context = {'quiz_form': quiz_form}
    return render(request, 'base/create_quiz.html', context)

