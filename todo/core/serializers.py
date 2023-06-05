# from rest_framework import serializers
#
# from .models import User
#
#
# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'last_login': {'write_only': True},
#             'date_joined': {'write_only': True},
#         }
#
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         user.set_password(validated_data['password'])
#
#         if user.role == 'admin':
#             user.is_staff = True
#         user.save()
#
#         return user
#
#
# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ('password',)
#
