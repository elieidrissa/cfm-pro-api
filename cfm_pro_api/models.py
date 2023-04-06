import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin




# options
SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]

# profile img: https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5?s=150

# -------------------------------------------------------------------------------
# TERRITORIES AND SUB_TERRITORIES
# -------------------------------------------------------------------------------
class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'provinces'
    
                            
class Territoire(models.Model):
    '''Territoire/Ville'''
    province = models.ForeignKey(Province, related_name='territoires', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'territoires'


class Chefferie(models.Model):
    '''Chefferie/Secteur/Commune'''
    territoire = models.ForeignKey(Territoire, related_name='chefferies', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chefferies'


class Groupement(models.Model):
    '''Groupement/Quartier'''
    chefferie = models.ForeignKey(Chefferie, related_name='groupements', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'groupements'


class Village(models.Model):
    '''Village/Avenue'''
    groupement = models.ForeignKey(Groupement, related_name='villages', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'villages'

# -------------------------------------------------------------------------------
# USERS
# -------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    '''The user type can be: 
        - is_AG -> [default] simple agent , 
        - is_AT -> agent de terrain, 
        - is_COORD -> coordonnateur, 
        - is_DG -> Directeur General or
        - is_SUPER -> Super User'''
    
    def create_user(self, nom=None, postnom=None, 
                    phone_number=None, password=None,
                    zone=None, **extra_fields):
        '''create a user object '''

        if not nom or not postnom:
            raise ValueError('Nom or postnom not specified')
        
        if not phone_number or not password:
            raise ValueError('Phone number or Password not provided')
        
        if not zone:
            raise ValueError('Zone not specified')
        
        # create a new user object
        user = self.model(
            nom = nom,
            postnom = postnom,
            phone_number = phone_number,
            zone=Zone(pk=zone)
        )

        # hashed password (change password the same way)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
 
    def create_superuser(self, nom=None, postnom=None, 
                    phone_number=None, password=None, 
                    zone=None,**extra_fields):
        '''Save the user as an 'All access' user '''
        user = self.create_user(nom=nom, postnom=postnom, 
                                phone_number = phone_number,
                                password=password,
                                zone=zone, **extra_fields)
        # perms
        user.is_AT = True
        user.is_COORD = True
        user.is_DG = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        # save changes to DB
        user.save(using=self._db)
        
        return user
    

class Zone(models.Model):
    '''Zone where a user works. This helps filter data by regions'''
    name = models.CharField(max_length=50, unique=True)
    territoire = models.OneToOneField(Territoire, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ', ' + self.code

    class Meta:
        db_table = 'zones'
        unique_together = ('territoire', 'code')

    
class User(AbstractBaseUser, PermissionsMixin):
    '''This model represents all users of API with their varying permissions.
        Users of this API roles and their permissions:
      - AG: is allewed to view and edit data saved by his account during the current month 
      - AT: is allowed to view and edit data saved by his account during the current month 
      - COORD: is allowed to view and edit data from all the 'ATs' and edit it
      - DIR: is allowed to view but can't edit all the data form all times
      - SUPER: has unrestricted access to everything'''
    
    # required infos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50, blank=True)
    phone_number = PhoneNumberField(unique=True)
    password = models.CharField(max_length=120)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    # checks for user type and perms
    is_AT = models.BooleanField('Agent de terrain', default=False)
    is_COORD = models.BooleanField('Coordonnateur', default=False)
    is_DG = models.BooleanField('Directeur General', default=False)
    # django defaults
    is_active = models.BooleanField(default=True) # False if user deleted
    is_staff = models.BooleanField('staff status',default=False)
    is_superuser = models.BooleanField('superuser',default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['nom', 'postnom', 'password', 'zone']

    # manager for crud operations on all users
    objects = UserManager()

    def __str__(self):
        return self.nom + ' ' + self.postnom

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.ForeignKey(Territoire, null=True, blank=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)
    id_number = models.CharField(max_length=100, blank=True)
    address = models.ForeignKey(Groupement, null=True, blank=True, on_delete=models.SET_NULL)
    address_info = models.CharField(max_length=200, null=True, blank=True)
    profile_img_url = models.URLField(blank=True, null=True)
    date_signup = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    email_verified = models.BooleanField(default=False) # 'True' if email confirmed
    number_verified = models.BooleanField(default=False) # 'True' if number confirmed
              
    class Meta:
        db_table = 'profiles'
        unique_together = ('user', 'email',)


# -------------------------------------------------------------------------------
# NEGOCIANTS, TRANSPORTEURS AND MINERAI
# -------------------------------------------------------------------------------
class Negociant(models.Model):
    '''All data that can be collected on a 'negociant' at the moment 03/2023'''
    nom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.ForeignKey(Territoire, null=True, blank=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    address = models.ForeignKey(Groupement, null=True, blank=True, on_delete=models.SET_NULL)
    address_info = models.CharField(max_length=200, null=True, blank=True)
    card_number = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom + ' ' + self.postnom

    class Meta:
        db_table = 'negociants'
        unique_together = ('nom', 'postnom',)


class Transporteur(models.Model):
    '''A 'negociant' can be a 'transpoteur' that why the foreign key is here
      but not required'''
    nom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True, blank=True)
    negociant = models.ForeignKey(Negociant, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    authorisation = models.CharField(max_length=30, blank=True, unique=True)
    address = models.ForeignKey(Groupement, null=True, blank=True, on_delete=models.SET_NULL)
    address_info = models.CharField(max_length=200, null=True, blank=True)
    plates = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom + ' ' + self.postnom

    class Meta:
        db_table = 'transporteurs'
        unique_together = ('nom', 'postnom',)

class Minerai(models.Model):
    '''This data will be manualy added to the database and will not come from
    the users since there's only a few choices of minerals.
    The database will at first support the 3Ts and the if there's a need to add
    more in the future the database will be updated'''
    name = models.CharField(max_length=50, unique=True)
    formule = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=30, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name + ', ' + self.symbol

    class Meta:
        db_table = 'minerais'


class Cooperative(models.Model):
    '''This data will be added buy the COORD user'''
    long_name = models.CharField(max_length=150, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    address = models.ForeignKey(Groupement, null=True, blank=True, on_delete=models.SET_NULL)
    address_info = models.CharField(max_length=200, null=True, blank=True,)
    agrement = models.CharField(max_length=30, unique=True, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.short_name

    class Meta:
        db_table = 'cooperatives'

# -------------------------------------------------------------------------------
# SITES
# -------------------------------------------------------------------------------
class Axe(models.Model):
    '''This data will be manualy added to the database'''
    name = models.CharField(max_length=30, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'axes'


class Site(models.Model):
    '''This data will be added buy the COORD user'''
    name = models.CharField(max_length=50, unique=True)
    village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL)
    axe = models.ForeignKey(Axe,  related_name='sites', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sites'

    
class Chantier(models.Model):
    '''This data will be added buy the COORD user'''
    name = models.CharField(max_length=100, unique=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    site = models.ForeignKey(Site,  related_name='chantiers', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chantiers'

# -------------------------------------------------------------------------------
# LOTS
# -------------------------------------------------------------------------------
class Lot(models.Model):
    '''Details:
    - 'date_reg': the date the 'Lot' was registered
    - 'user_id': id of the user submitting the 'Lot'
    - 'date_submit': submission timestamp

    This data is all from the 'AT' level user except for the following fields
    - 'confirm' field: indicates if the 'COORD' has approved of the data
    - 'confirm_date' is the time stamp of the confirmation'''
    user = models.ForeignKey(User,  related_name='lots', on_delete=models.CASCADE)
    date = models.DateField()
    negociant = models.ForeignKey(Negociant, related_name='lots', on_delete=models.CASCADE)
    minerai = models.ForeignKey(Minerai,  related_name='lots', on_delete=models.CASCADE)
    colis = models.IntegerField()
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.TextField()
    atm = models.CharField(max_length=30, blank=True, unique=True)
    chantier = models.ForeignKey(Chantier,  related_name='lots', on_delete=models.CASCADE)
    cooperative = models.ForeignKey(Cooperative,  related_name='lots', on_delete=models.CASCADE)
    transporteur = models.ForeignKey(Transporteur,  related_name='lots', on_delete=models.CASCADE)
    date_submit  = models.DateTimeField(auto_now_add=True)
    confirmed =  models.BooleanField(default=False, blank=True)
    date_confirm = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.negociant.nom + ', ' + self.colis + ', ' + self.poids

    class Meta:
        db_table = 'lots'
        ordering = ['date']
        # check if a 'lot' with the same data in these fields already exist 
        unique_together = ('date', 'negociant', 'minerai', 'colis')









