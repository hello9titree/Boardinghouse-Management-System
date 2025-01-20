import uuid
from django.db import models

class  Landlord(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='landlords/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Custom UUID field
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='rooms')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Automatically set is_available to False if capacity is equal to number of tenants in room
        # Count the number of tenants in this room
        tenant_count = self.tenants.count() # This gets the number of tenants related to this room
        
        # Automatically set is_occupied based on the number of tenants and capacity
        if tenant_count >= self.capacity:
            self.is_available = False
        else:
            self.is_available = True
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"RoomID: {self.id}, Room {self.room_number}, Capacity: {self.capacity}, Price/month: {self.price_per_month}, Landlord: {self.landlord}, Available: {'Available' if self.is_available else 'Not Available'}"

    
    
    
class Tenant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='tenants')
    move_in_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    