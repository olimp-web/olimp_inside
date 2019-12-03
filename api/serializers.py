from rest_framework import serializers
from .models import MacModelUser
from accounts.models import UserAccount
from visits.models import Visit


class VisitSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='get_full_name')

    class Meta:
        model = UserAccount
        fields = ['id', 'fullname']


class VisitDataSerializer(serializers.ModelSerializer):
    profile = VisitSerializer(source='user')

    class Meta:
        model = Visit
        fields = ['profile', 'enter_timestamp', 'leave_timestamp']


class API_Serializer(serializers.Serializer):
    mac_address = serializers.CharField(max_length=100)
    # user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    user_id = serializers.IntegerField()

    # class Meta:
    #     model = MacModelUser;
    #     fields = ('mac_adress',)

    def create(self, validated_data):
        return MacModelUser.objects.create(**validated_data)


class MACAddressSerializer(serializers.ModelSerializer):
    mac_address = serializers.RegexField(max_length=100, regex=MacModelUser.PATTERN)
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                              queryset=UserAccount.objects.filter(is_active=True))

    class Meta:
        model = MacModelUser
        fields = ('mac_address', 'user')
