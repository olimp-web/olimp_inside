from rest_framework import serializers
from .models import MacModelUser
from accounts.models import UserAccount


class API_Serializer(serializers.Serializer):
    mac_address = serializers.CharField(max_length=100)
    # user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    user_id = serializers.IntegerField()

    # class Meta:
    #     model = MacModelUser;
    #     fields = ('mac_adress',)

    def create(self, validated_data):
        return MacModelUser.objects.create(**validated_data)

