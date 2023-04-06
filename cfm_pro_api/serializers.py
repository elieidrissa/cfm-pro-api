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
                  'address', 'address_info', 'profile_img_url',
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
        response['transporteur'] = transport.nom + ' ' + transport.postnom
        # resulting data
        return response

    class Meta:
        model = Lot
        fields = "__all__"

# -------------------------------------------------------------------------------
# ADDITIONAL-MODELS
# -------------------------------------------------------------------------------

class NegociantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Negociant
        fields = "__all__"


class TransporteurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transporteur
        fields = "__all__"


class MineraiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minerai
        fields = "__all__"


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = "__all__"


class AxeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axe
        fields = "__all__"


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class ChantierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chantier
        fields = "__all__"

# -------------------------------------------------------------------------------
# TERRITORIES AND SUB_TERRITORIES
# -------------------------------------------------------------------------------

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"

class TerritoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territoire
        fields = "__all__"

class ChefferieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chefferie
        fields = "__all__"

class GroupementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupement
        fields = "__all__"

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = "__all__"