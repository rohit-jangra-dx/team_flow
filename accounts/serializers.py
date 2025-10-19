from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser, Profile

class RegisterSerializer(serializers.ModelSerializer):
#    validation at the serializer level
    email = serializers.EmailField(
       required=True,
       validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    ) 
    username = serializers.CharField(
       required=True,
       validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"}
    )
    
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password"]
        read_only_fields = ["id"]
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Profile 
        fields = [
            "email", "username", "full_name", "github_link", 
            "linkedin_profile", "bio"
        ]