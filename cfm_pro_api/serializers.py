from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *
from phonenumber_field.serializerfields import PhoneNumberField


# -------------------------------------------------------------------------------
# USER AND PROFILE-MODELS
# -------------------------------------------------------------------------------
class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, 
                       default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'sex', 'id_number', 
                  'address', 'address_info', 'profile_img',
                  'email']
        read_only_fields = ['user']


class UserCreateSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(max_length=50)
    postnom = serializers.CharField(max_length=50)
    prenom  = serializers.CharField(max_length=50, allow_null=True)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=6, max_length=120)
    conf_password = serializers.CharField(min_length=6, max_length=120, write_only=True)
    zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all())
    is_AT = serializers.BooleanField(default=False)
    is_COORD = serializers.BooleanField(default=False)
    is_DG = serializers.BooleanField(default=False)
    
    def validate(self, attrs):
        ''' Check form missing of duplicated data'''
        phone_number_exists = User.objects.filter(phone_number=attrs['phone_number']).exists()
        
        if phone_number_exists:
            raise serializers.ValidationError(detail="phone number already exists")
        
        if attrs['password'] != attrs['conf_password']:
            raise serializers.ValidationError(detail="password does not match")
                        
        if not attrs['is_COORD'] and not attrs['is_AT'] and not attrs['is_DG']:
            raise serializers.ValidationError(detail="no user role was specified")
        
        return super().validate(attrs)

    def create(self, validated_data):
        ''' Cretate a new 'User' instance from validated data'''
        # USER
        user = User(
            nom = validated_data['nom'],
            postnom = validated_data['postnom'],
            prenom = validated_data['prenom'],
            phone_number = validated_data['phone_number'],
            zone = validated_data['zone'],
            is_AT = validated_data['is_AT'],
            is_COORD = validated_data['is_COORD'],
            is_DG = validated_data['is_DG'],
        )
        user.set_password(validated_data['password'])
        user.save()
      
        return user
    
    class Meta:
        model = User
        fields = ['nom', 'postnom', 'prenom',
                  'phone_number', 'password', 'conf_password',
                  'zone', 'is_AT', 'is_DG', 'is_COORD']
        # nom and postnom must be unique to one user
        validators = [
            UniqueTogetherValidator(
                queryset= User.objects.all(),
                fields=['nom', 'postnom']
            )
        ]
    

class UserRetrieveSerializer(serializers.ModelSerializer):
    # create a user using the 'UserManager' class
    # nested profile field
    profile = UserProfileSerializer(read_only=True)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "nom" : instance.nom,
            "postnom" : instance.postnom,
            "prenom" : instance.prenom,
            "phone_number" : str(instance.phone_number),
            "zone" : instance.zone.code,
            'profile':  UserProfileSerializer(instance.profile).data,
            "is_AT" : instance.is_AT,
            "is_COORD" : instance.is_COORD,
            "is_DG" : instance.is_DG,
        }

    class Meta:
        model = User
        fields = ['nom', 'postnom', 'prenom',
                  'phone_number', 'profile',]

# -------------------------------------------------------------------------------
# LOT-MODEL
# -------------------------------------------------------------------------------

class LotModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = "__all__"

class LotHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lot
        fields = "__all__"

class LotDetailSerializer(serializers.ModelSerializer):
    # added_by = serializers.ReadOnlyField(source='user.nom')
    def to_representation(self, instance):
        # get data related to the lot
        user = instance.user
        negociant = instance.negociant
        transport = instance.transporteur
        # replace IDs 
        response = super().to_representation(instance)
        response['user'] = user.nom + ' ' + user.postnom
        response['negociant'] = negociant.nom + ' ' + negociant.postnom
        response['minerai'] = instance.minerai.symbol
        response['chantier'] = instance.chantier.name
        response['cooperative'] = instance.cooperative.short_name
        response['transporteur'] = transport.nom +' '+ transport.postnom
        # resulting data
        return response

    class Meta:
        model = Lot
        fields = "__all__"

# -------------------------------------------------------------------------------
# NEGOCIANTS
# -------------------------------------------------------------------------------
class NegociantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Negociant
        fields = "__all__"


class NegociantDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        territoire = instance.birth_place
        groupement = instance.address
        # to avoid errors where 'NoneType' does have 'name' 
        if territoire:
            response['birth_place'] = territoire.name
        if groupement:
            response['address'] = groupement.name
        # resulting data
        return response

    class Meta:
        model = Negociant
        fields = "__all__"

# -------------------------------------------------------------------------------
# TRANSPORTEURS
# -------------------------------------------------------------------------------
class TransporteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporteur
        fields = "__all__"


class TransporteurDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        negociant = instance.negociant
        groupement = instance.address
        # to avoid errors where 'NoneType' does have 'name' 
        if groupement:
            response['address'] = groupement.name
        if negociant:
            response['negociant'] = negociant.nom +' '+ negociant.postnom
        # resulting data
        return response

    class Meta:
        model = Transporteur
        fields = "__all__"

# -------------------------------------------------------------------------------
# MINERAIS
# -------------------------------------------------------------------------------
class MineraiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minerai
        fields = "__all__"

class MineraiDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

    class Meta:
        model = Minerai
        fields = "__all__"

# -------------------------------------------------------------------------------
# COOPERATIVES, SITE, CHANTIERS...
# -------------------------------------------------------------------------------
# COOPS
class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = "__all__"

class AxeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axe
        fields = "__all__"

# AXES
class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"

class SiteDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        axe = instance.axe
        village = instance.village
        if axe:
            response['axe'] = axe.name
        if village:
            response['village'] = village.name
        return response

    class Meta:
        model = Site
        fields = "__all__"

# CHANTIER
class ChantierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chantier
        fields = "__all__"

class ChantierDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        site = instance.site
        if site:
            response['site'] = site.name
        return response

    class Meta:
        model = Chantier
        fields = "__all__"

# -------------------------------------------------------------------------------
# PROVINCES, TERRITORIES AND SUB_TERRITORIES
# -------------------------------------------------------------------------------
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = ['date_added', 'date_updated']

# TERRITOIRES
class TerritoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territoire
        fields = "__all__"

class TerritoireDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        province = instance.province
        if province:
            response['province'] = province.name
        return response

    class Meta:
        model = Territoire
        exclude = ['date_added', 'date_updated']

    
# CHEFFERIES
class ChefferieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chefferie
        fields = "__all__"

class ChefferieDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        territoire = instance.territoire
        if territoire:
            response['territoire'] = territoire.name
        return response

    class Meta:
        model = Chefferie
        exclude = ['date_added', 'date_updated']

# GROUPEMENT
class GroupementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupement
        fields = "__all__"

class GroupementDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        chefferie = instance.chefferie
        territoire = instance.chefferie.territoire
        if chefferie:
            response['chefferie'] = chefferie.name
        if territoire:
            response['territoire'] = territoire.name
        return response

    class Meta:
        model = Groupement
        exclude = ['date_added', 'date_updated']

# VILLAGE
class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        exclude = ['date_added', 'date_updated']

class VillageDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        groupement = instance.groupement
        territoire = instance.groupement.chefferie.territoire
        if groupement:
            response['groupement'] = groupement.name
        if territoire:
            response['territoire'] = territoire.name
        return response

    class Meta:
        model = Village
        exclude = ['date_added', 'date_updated']