from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages

def character_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/character_list.html', {'characters': characters, 'equipements':equipements})
    
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    equipement = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    form = MoveForm(request.POST, instance=character)
    all_equipments = Equipement.objects.all()
    if form.is_valid():
        ancien_lieu = equipement
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()

        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        
        if nouveau_lieu.disponibilite == "occupé":
            ancien_lieu.disponibilite = "occupé"
            character.lieu = ancien_lieu
            ancien_lieu.save()
            character.save()
            messages.error(request, "Cet emplacement est déjà occupé.")
            return render(request, 'blog/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'all_equipments': all_equipments})
        else:
            nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            character.lieu = nouveau_lieu
            character.save()
            if character.etat == "Fatigué" and character.lieu.id_equip == "Grotte":
                character.etat = "Affamé"
            elif character.etat == "Affamé" and character.lieu.id_equip == "Mangeoire":
                character.etat = "Ennuyé"
            elif character.etat == "Ennuyé" and character.lieu.id_equip == "Coquillage":
                character.etat = "Engourdi"
            elif character.etat == "Engourdi" and character.lieu.id_equip == "Tourbillon":
                character.etat = "Fatigué"
            else:
                messages.error(request, f"{character.id_character} n'a pas envie d'aller dans l'emplacement choisi.")
                return render(request, 'blog/character_detail.html', {'character': character, 'etat': character.etat, 'form': form, 'all_equipments': all_equipments})
            
            character.save()
            return redirect('character_detail', id_character=id_character)
    else:
        # Add this line to fetch all occupied locations
        occupied_locations = Equipement.objects.filter(disponibilite="occupé")
        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'occupied_locations': occupied_locations, 'all_equipments': all_equipments})



def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    return render(request, 'blog/equipement_detail.html', {'equipement': equipement})
