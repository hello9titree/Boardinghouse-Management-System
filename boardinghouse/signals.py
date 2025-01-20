from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Landlord, Tenant, Room

@receiver(post_save, sender=Room)
def update_room_availability(sender, instance, created, **kwargs):
    if created:
        # This block runs only when a new Room instance is created
        # You can safely access instance.tenants here if needed
        tenant_count = instance.tenants.count()
        
        # Update availability based on tenant count
        instance.is_available = tenant_count < instance.capacity
        instance.save()  # Save the updated availability status

@receiver(post_save, sender=Tenant)
def update_room_available_status_on_tenant_save(sender, instance, **kwargs):
    room = instance.room
    room.save()  # This will trigger the save method in the Room model

@receiver(post_delete, sender=Tenant)
def update_room_available_status_on_tenant_delete(sender, instance, **kwargs):
    room = instance.room
    room.save()  # This will trigger the save method in the Room model