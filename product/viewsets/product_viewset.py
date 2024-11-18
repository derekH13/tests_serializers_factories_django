from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    # adicionando as duas classes de autentificação (esta no setting)
    # BasicAuthentication uma autentificação simples
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    # faz uma interceptação da resquest para verificar se o user esta autorizado ou não (atraves do tokken autenfication)
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # para definir a ordenação pelo id
        return Product.objects.all().order_by("id")
