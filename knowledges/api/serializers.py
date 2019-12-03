from rest_framework import serializers

from knowledges.models import Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='label', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Article
        fields = '__all__'
