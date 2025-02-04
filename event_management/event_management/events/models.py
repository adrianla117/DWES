from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo personalizado de usuario
class User(AbstractUser):
    ROLES = (
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
    )
    role = models.CharField(max_length=15, choices=ROLES)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# Modelo de Evento
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', limit_choices_to={'role':'organizer'})

    def __str__(self):
        return self.title

# Modelo de Reserva
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', limit_choices_to={'role':'participant'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"

# Modelo de Comentario
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario añadido por {self.user.username} en el evento {self.event.title}"