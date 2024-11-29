from rest_framework import serializers


class ChatInputSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)

