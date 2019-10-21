from rest_framework.viewsets import ModelViewSet

from .serializers import ArticleSerializer, Article


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
