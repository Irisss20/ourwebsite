from django.forms import ModelForm
from .models import Vacancy, Quiz


class VacForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'

# class Ordering(ModelForm):
#     class Meta:
#         oredering = ['-updated']
        

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

