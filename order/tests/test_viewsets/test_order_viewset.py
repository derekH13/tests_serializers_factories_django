import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory, CategoryFactory
from product.models import Product


class TestOrderViewSet(APITestCase):

    client = APIClient()

    # criando todos os objetos
    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            # passando uma lista ([self.category])
            title="mouse", price=100, category=[self.category]
        )
        # passando uma lista ([self.product])
        self.order = OrderFactory(product=[self.product])
        token = Token.objects.create(user=self.order.user)
        token.save()

    def test_order(self):
        token = Token.objects.get(user__username=self.order.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        # fazendo uma requisição usando o name da url
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"}))

        # espera que a requisição tenha retornado HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # import pdb
        # pdb.set_trace()

        # transforma em objeto
        order_data = json.loads(response.content)

        # faz o caminho para verificar o valor title e espera que tenha o mesmo valor criado no self.product.title
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        # faz o caminho para verificar o valor price e espera que tenha o mesmo valor criado no self.product.price
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    # criando um order
    def test_create_order(self):
        token = Token.objects.get(user__username=self.order.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # factory para pegar informações
        user = UserFactory()
        product = ProductFactory()
        # objeto order
        data = json.dumps({"product_id": [product.id], "user": user.id})

        # post do objeto order
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        # verificação final se foi criado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
