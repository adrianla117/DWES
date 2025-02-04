from django.contrib import admin
from .models import User, Event, Reservation, Comment

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Reservation)
admin.site.register(Comment)