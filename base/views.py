from django.shortcuts import render, redirect  # render - обработка, redirect - перенаправление
from django.contrib import messages  # Для отображения ошибок, предупреждений и тд
from .models import Vacancy, DevGrades, Quiz
from .forms import VacForm 
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


def vacancies(request, pk):  # pk это специальное выражение для обозначения уникальной идентификации каждой записи 
    vacancy = Vacancy.objects.get(id=pk) 
    context = {'vacancy': vacancy}
    return render(request, 'base/vacancy_details.html', context)

@login_required(login_url='/')
def createVac(request):
    form = VacForm()
    if request.method == "POST":
        form = VacForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    context = {'form': form}
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

