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
    i = 0
    lista =[["affamé","Mangeoire","repus"],["repus","Roue","fatigué"],["fatigué","Nid", "endormi"],["endormi","Litière", "affamé"]]
    animal = get_object_or_404(Animal, id_animal=id_animal)
    etat_before = animal.etat
    lieu_before = animal.lieu
    message = ""
    form = MoveForm(request.POST, instance=animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=lieu_before.id_equip)
    if request.method == "POST" and form.is_valid():
      ancien_lieu.disponibilite = "libre"
      ancien_lieu.save()
      form.save(commit=False)
      nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
      while i<4:
        if lista[i][0] == etat_before:
          if nouveau_lieu.id_equip == ancien_lieu.id_equip:
            message = f"Impossible, le {animal.id_animal} est dejà à {ancien_lieu.id_equip}."
            ancien_lieu.disponibilite = "occupé"
            i = 4
          elif nouveau_lieu.id_equip == lista[i][1]:
            if nouveau_lieu.disponibilite == "libre":
              if nouveau_lieu.id_equip == "Litière":
                nouveau_lieu.disponibilite = "libre"
              else:
                nouveau_lieu.disponibilite = "occupé"
              nouveau_lieu.save()
              animal.etat = lista[i][2]
              animal.save()
              form.save()
            else:
              if ancien_lieu.id_equip == "Litière":
                ancien_lieu.disponibilite = "libre"
              else:
                ancien_lieu.disponibilite = "occupé"
              message = f"Le {animal.id_animal} ne peut aller à {nouveau_lieu} pour être {lista[i][2]}."
            i = 4
          elif nouveau_lieu.disponibilite == "occupé":
            message = f"Impossible, le {nouveau_lieu.id_equip} est occupé."
            ancien_lieu.id_disponibilite = "occupé"
            i = 4
          else:
            message = f"Le {animal.id_animal} ne peut aller à {nouveau_lieu} pour être {lista[i][2]}."
            ancien_lieu.disponibilite = "occupé"
            i = 4
        i+=1
      return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': nouveau_lieu, 'form': form, 'message': message})
    else:
      form = MoveForm()
      return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': ancien_lieu, 'form': form, 'message': message})