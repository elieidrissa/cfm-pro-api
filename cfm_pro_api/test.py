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




class TerritoireFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Territoire.objects.all()
    serializer_class = TerritoireDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TerritoireFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = TerritoireFilter(req.GET, queryset=qs)
        return self.filterset.qs


class TerritoireDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

    class Meta:
        model = Territoire
        fields = "__all__"


class TerritoireFilter(django_filters.FilterSet):
    class Meta:
        model = Territoire
        fields = {
            'name' : LOOKUP_EXPR, 
            'symbol' : LOOKUP_EXPR,
            'symbol' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }