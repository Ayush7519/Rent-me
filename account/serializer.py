from rest_framework import serializers
from .models import User
from rnt.utils import Util
# user registrtion serializer.
class UserRegistration_Serializer(serializers.ModelSerializer):
    # here we validate the password of the user to register him or her
    password2 = serializers.CharField(
        style={"input_type": "password", "write_only": True}
    )

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and conform password doesnot match "
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# userlogin serializer.
class UserLogin_Serializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]

# login user profile serializer.
class UserProfile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# user password change serializer.
class UserPasswordChange_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                {"msg": "Password and Confirm password doesnot matches..."}
            )
        user.set_password(password)
        user.save()
        # email send after the password is changed.
        data = {
            "subject": "Django Mail",
            "body": "Hii"
            + " "
            + user.name
            + " "
            + "Your Password Has Been Changed !!!",
            "to_email": user.email,
        }
        Util.send_email(data)
        return attrs
