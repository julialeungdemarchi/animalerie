from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

def firstpage(request):
    animals = Animal.objects.filter()
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/firstpage.html', {'animals': animals, 'equipements': equipements})

def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals})

def equipement_list(request):
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/equipement_list.html', {'equipements': equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    form=MoveForm()
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if form.is_valid():
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()
        form.save()
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()
        return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': ancien_lieu, 'form': form})