# class ProfileCreateSerializer(serializers.ModelSerializer):
#    username = serializers.CharField(source='user.username')

#    class Meta:
#        model = Profile
#        fields = [
#        'username',
#        'language',
#        ]

#    def create (self, validated_data):
#     user = get_user_model().objects.create(username=validated_data['username'])
#     user.set_password(User.objects.make_random_password())
#     user.save()

#     profile = Profile.objects.create(user = user)

#     return profile


