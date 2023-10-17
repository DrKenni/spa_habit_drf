from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.tg_chat_id = validated_data.get('tg_chat_id', instance.tg_chat_id)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'
