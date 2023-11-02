from rest_framework import serializers
def youtube_url(value):
    if 'youtube.com' not in value:
        raise serializers.ValidationError("Ссылка должна вести на youtube")