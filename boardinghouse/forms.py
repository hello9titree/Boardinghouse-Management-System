from django import forms

from . models import Landlord, Room, Tenant




class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['first_name', 'last_name', 'birthdate', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'capacity', 'price_per_month', 'is_available']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'room', 'move_in_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'move_in_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # This enables the date picker
                'placeholder': 'YYYY-MM-DD'  # Optional: placeholder text
            }),
        }
    # Override the __init__ method to customize the queryset for the room field
    # def __init__(self, *args, landlord, **kwargs):
    #     super(TenantForm, self).__init__(*args, **kwargs)
    #     if landlord is not None:
    #         self.fields['room'].queryset = Room.objects.filter(is_available=True, landlord=landlord)  # Filter by landlord
    #     else:
    #         self.fields['room'].queryset = Room.objects.filter(is_available=True)  # Default to show unoccupied rooms
            
    def __init__(self, *args, landlord=None, tenant=None, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        # Set the queryset for the room field based on the landlord
        if landlord:
            self.fields['room'].queryset = Room.objects.filter(is_available=True, landlord=landlord)
        
        # Set the initial value for the room field based on the tenant
        if tenant is not None:
            if tenant.room:  # Ensure that the tenant has an associated room
                self.fields['room'].initial = tenant.room.id  # Set the initial value to the room's ID
            else:
                # Optional: Handle the case where the tenant does not have a room
                self.fields['room'].initial = None  # or some default value