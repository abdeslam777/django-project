from django.contrib import admin
from .models import Offer , OfferApplication 
# Register your models here.


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title','supervisor' ,'is_active']

@admin.register(OfferApplication)
class OfferApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'offer', 'applied_at']

# admin.site.register(Watchlist)


