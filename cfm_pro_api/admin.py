from django.contrib import admin
from .models import ( Negociant, Transporteur, 
                    Minerai, Cooperative, Axe, 
                    Site, Chantier, Lot, Profile)
from django.contrib.auth import get_user_model

# admin.site.register(User) 
admin.site.register(Negociant) 
admin.site.register(Transporteur)
admin.site.register(Minerai)
admin.site.register(Cooperative)
admin.site.register(Axe)
admin.site.register(Site) 
admin.site.register(Chantier)
admin.site.register(Lot)
admin.site.register(Profile)

# customised user model
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    serach_fields = ['nom', 'postnom']
    class Meta:
        model = User

admin.site.register(User, UserAdmin)
