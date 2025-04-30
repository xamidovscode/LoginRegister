from datetime import datetime, timedelta

from django.utils.translation import round_away_from_one
from rest_framework import serializers
from users import models
import random


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=True, write_only=True)
    phone = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):

        phone = attrs['phone']
        current_date = datetime.now()

        user = models.CustomUser.objects.filter(
            phone=phone
        ).first()

        if user:

            code_verify = user.code_verifies.filter(
                expire_date__gte=current_date
            ).first()

            if code_verify:
                raise serializers.ValidationError(
                    {"phone": "Sizga kod yuborilgan"}
                )

        return attrs

    def create(self, validated_data):
        full_name = validated_data.get("full_name")
        phone = validated_data.get("phone")
        password = validated_data.get("password")

        user = models.CustomUser.objects.filter(phone=phone).first()

        if user:

            user.full_name = full_name
            user.password = password
            user.save()

            self.create_verify_code(user)

            return user

        else:

            user = models.CustomUser.objects.create_user(
                phone=phone, password=password, full_name=full_name
            )
            self.create_verify_code(user)

            return user

    @staticmethod #DRY
    def create_verify_code(user):
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        code_verifies = user.code_verifies.filter().first()
        expire_date = datetime.now() + timedelta(seconds=120)

        if not code_verifies:
            models.CodeVerification.objects.create(
                user=user, code=code, expire_date=expire_date
            )
        else:
            code_verifies.code = code
            code_verifies.expire_date = expire_date
            code_verifies.save()


class CodeVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=255, required=True, write_only=True
    )
    phone = serializers.CharField(
        max_length=255, required=True, write_only=True
    )


    def create(self, validated_data):
        phone = validated_data.get("phone")
        code = validated_data.get("code")

        code_verification = models.CodeVerification.objects.filter(
            code=code, user__phone=phone,
        )

        if not code_verification.exists():
            """
            Kodlarni tenglikga tekshirish
            """
            raise serializers.ValidationError(
                {"code": "Kod xato kiritildi"}
            )

        if code_verification.filter(
                expire_date__lte=datetime.now()
        ).exists():
            """
            Kod eskirmaganligiga tekshirish
            """
            raise serializers.ValidationError(
                {"code": "Kod eskirgan"}
            )

        if code_verification.first():
            user = code_verification.first().user
            user.status = "active"
            user.save()

        return validated_data



class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, required=True, write_only=True
    )
    phone = serializers.CharField(
        max_length=255, required=True, write_only=True
    )

    def create(self, validated_data):
        phone = validated_data.get("phone")
        password = validated_data.get("password")

        user = models.CustomUser.objects.filter(
            phone=phone, status="active"
        ).first()

        if not user:
            raise serializers.ValidationError(
                {"phone": "Foydalanuvchi topilmadi"}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"phone": "Parol xato kiritildi"}
            )

        return user


