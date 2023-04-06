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



# # FILTERS IMPLEMENTATION

# class VillageFilterListView(ListAPIView):
#     '''This view is used to SEARCH through negociants'''
#     queryset = Village.objects.all()
#     serializer_class = VillageDetailSerializer
#     pagination_class = CustomPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = VillageFilter

#     def get_queryset(self):
#         req = self.request
#         qs = self.queryset
#         self.filterset = VillageFilter(req.GET, queryset=qs)
#         return self.filterset.qs


# class VillageDetailSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         return response

#     class Meta:
#         model = Village
#         fields = "__all__"


# class VillageFilter(django_filters.FilterSet):
#     class Meta:
#         model = Village
#         fields = {
#             'name' : LOOKUP_EXPR, 
#             'territoire__name' : LOOKUP_EXPR,
#             'date_added' : ('exact', 'lte', 'gte'),
#             'date_updated' : ('exact', 'lte', 'gte'),
#         }