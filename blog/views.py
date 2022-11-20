from django.shortcuts import render
from django.utils import timezone
from .models import Animal


# Create your views here.


def animal_list(request): #Ici on fait en sorte que la vue soit sous la forme d'une liste de billets de blog
    animaux = Animal.objects.all()
    return render(request, 'blog/animal_list.html', {'animaux' : animaux})



