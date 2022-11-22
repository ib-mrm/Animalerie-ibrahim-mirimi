from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement


def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {"animaux" : animaux, "equipements" : equipements} )


def animal_detail(request, id_animal):
    
    mangeoire = get_object_or_404(Equipement, id_equip='mangeoire')
    roue = get_object_or_404(Equipement, id_equip='roue')
    nid = get_object_or_404(Equipement, id_equip='nid')
    litiere = get_object_or_404(Equipement, id_equip='litiere')
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            if form.data['lieu'] == 'mangeoire':
                if mangeoire.disponibilite == 'occupe':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': "Le mangeoire est plein"})
                elif animal.etat == 'affame' and mangeoire.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'repus'
                    form.save()                  
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupe"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                
                else:
                    if ancien_lieu!= litiere:
                        ancien_lieu.disponibilite = "occupe"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Désolé, {animal} n'a pas faim"})

            elif form.data['lieu'] == 'roue':
                if roue.disponibilite == 'occupe':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Désolé, un animal s'amuse déjà"})            
                elif animal.etat == 'repus' and roue.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'fatigue'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupe"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')   
                else:
                    if ancien_lieu!= litiere:
                        ancien_lieu.disponibilite = "occupe"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Désolé {animal} mange encore"})

            elif form.data['lieu'] == 'nid':
                if nid.disponibilite == 'occupe':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Le nid est plein"})            
                elif animal.etat == 'fatigue' and nid.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'endormis'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupe"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                       
                else:
                    if ancien_lieu!= litiere:
                        ancien_lieu.disponibilite = "occupe"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Désolé {animal} en a encore sous le pied"})

            elif form.data['lieu'] == 'litiere':
                if litiere.disponibilite == 'occupe':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"La litiere est pleine"})              
                elif animal.etat == 'endormis' and litiere.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'affame'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "libre"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                       
                else:
                    if ancien_lieu!= litiere:
                        ancien_lieu.disponibilite = "occupe"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Désolé {animal} ne dort pas"})


                  
        else:
            form = MoveForm()
    else:
        form = MoveForm()

    return render(request, 'blog/animal_detail.html', {'animal': animal, 'lieu': animal.lieu, 'form': form})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    animaux = Animal.objects.all()
    for animal in animaux:
        if animal.lieu == equipement:
            return render(request, 'blog/equipement_detail.html', {"equipement" : equipement, "animal": animal})        
    return render(request, 'blog/equipement_detail.html', {"equipement" : equipement})