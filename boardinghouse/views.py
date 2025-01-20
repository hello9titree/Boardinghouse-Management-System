from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from . models import Landlord, Room, Tenant
from . forms import LandlordForm, RoomForm, TenantForm


# HOME INDEX
def index(request):
    return render(request, "boardinghouse/index.html")

# LANDLORDS
def landlord_home(request, landlord_id):
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    rooms = landlord.rooms.all
    tenants = Tenant.objects.filter(room__landlord=landlord)
    
    context = {
        'landlord': landlord,
        'rooms': rooms,
        'tenants': tenants,
    }
    return render(request, "boardinghouse/landlord_index.html", context)

def landlord_list(request):
    landlords = Landlord.objects.all()
    context = {
        "landlords": landlords
    }
    return render(request, "boardinghouse/landlord_list.html", context)

def add_landlord(request):
    if request.method == "POST":
        form = LandlordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boardinghouse:landlord_list')
    else:
        form = LandlordForm()
    
    context = {
        'form': form
    }     
    return render(request, 'boardinghouse/add_landlord.html', context)


# ROOMS
def add_room(request, landlord_id):
    # Get the landlord object or return a 404 if not found
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)  # Create a Room instance but don't save to the database yet
            room.landlord = landlord  # Set the landlord for this room
            room.save()  # Now save the Room instance to the database
            return redirect('boardinghouse:landlord_home', landlord_id)  # Redirect to a room listing page or any other page
    else:
        form = RoomForm()
    context = {
        'form': form,
        'landlord': landlord
    }
    return render(request, "boardinghouse/add_room.html", context)

def edit_room(request, landlord_id, room_id):
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    room = get_object_or_404(Room, pk=room_id)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('boardinghouse:landlord_home', landlord_id)
    context = {
        'room': room,
        'form': form,
        'landlord': landlord,
    }
    return render(request, 'boardinghouse/edit_room.html', context)

def delete_room(request, landlord_id, room_id):
    # Fetch the landlord to ensure the room belongs to them
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    
    # Fetch the room associated with the landlord
    room = get_object_or_404(Room, pk=room_id, landlord=landlord)

    if request.method == 'POST':
        room.delete()  # Delete the room
        return redirect('boardinghouse:landlord_home', landlord_id=landlord.id)  # Redirect to the room list of the landlord

    context = {
        'room': room, 
        'landlord': landlord,
        }
    return render(request, 'boardinghouse/delete_room.html', context)


# TENANTS
def add_tenant(request, landlord_id):
    landlord = get_object_or_404(Landlord, pk=landlord_id) # Get the landlord by ID
    if request.method == 'POST':
        form = TenantForm(request.POST, landlord=landlord) # Pass the landlord to the form
        if form.is_valid():
            form.save()
            return redirect('boardinghouse:landlord_home', landlord.id) #redirect to landlord home
    else:
        form = TenantForm(landlord=landlord) # Pass the landlord when creating the form
    
    context = {
        'form': form,
        'landlord': landlord,
    }
    return render(request, 'boardinghouse/add_tenant.html', context)

def edit_tenant(request, landlord_id, tenant_id):
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant, landlord=landlord, tenant=tenant)  # Pass the tenant instance to the form
        if form.is_valid():
            form.save()
            return redirect('boardinghouse:landlord_home', landlord.id)  # Redirect to landlord home
    else:
        form = TenantForm(instance=tenant, landlord=landlord)  # Pass the tenant instance when creating the form

    context = {
        'form': form,
        'landlord': landlord,
        'tenant': tenant,
    }
    return render(request, "boardinghouse/edit_tenant.html", context)

def delete_tenant(request, landlord_id, tenant_id):
    # Fetch the landlord to ensure the room belongs to them
    landlord = get_object_or_404(Landlord, pk=landlord_id)
    
    # Fetch the room associated with the landlord
    tenant = get_object_or_404(Tenant, pk=tenant_id)

    if request.method == 'POST':
        tenant.delete()  # Delete the room
        return redirect('boardinghouse:landlord_home', landlord_id=landlord.id)  # Redirect to the room list of the landlord

    context = {
        'landlord': landlord,
        'tenant': tenant,
        }
    return render(request, 'boardinghouse/delete_tenant.html', context)