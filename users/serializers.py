from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [validators.UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required = True, 
        write_only = True,
        validators = [validate_password]

    )
    password2 = serializers.CharField(
        required = True, 
        write_only = True,
        validators = [validate_password]

    )

    class Meta:
        model = User
        # Görmek istemediklerim:
        exclude = [
            'last_login',
            'date_joined',
            'groups',
            'user_permissions',
            'is_active',
        ]
        '''
        # Alternatif: Görmek istediklerim.
        fields = [
            'email',
            'password',
            'password2',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'is_staff',
        ]
        '''

    # Override
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message": "Passwords are not same."})
        return attrs

    # Override
    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data) # Insert
        user.set_password(password) # EnCrypt
        user.save() # Update
        return user
        

# ------------------- Customization TokenSerializer ----------------------------
from dj_rest_auth.serializers import TokenSerializer

'''
# RegisterSerializer kullandığımız için buna gerek kalmadı.
class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )
'''

class CustomTokenSerializer(TokenSerializer):

    user = RegisterSerializer(read_only=True)
    
    class Meta(TokenSerializer.Meta):
        fields = ["key", "user"]
