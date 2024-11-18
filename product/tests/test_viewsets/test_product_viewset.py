import json

from django.urls import reverse
# import token models
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from order.factories import UserFactory
from product.factories import ProductFactory, CategoryFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    # criando um objeto
    def setUp(self):
        self.user = UserFactory()
        # cria um token
        token = Token.objects.create(user=self.user)
        # salvando o token gerado
        token.save()
        # objeto product
        self.product = ProductFactory(
            title='rtx gpu 1',
            price=1000,
        )

    def test_get_all_product(self):
        # esta criando um token para o usuario criado eu self.user
        token = Token.objects.get(user__username=self.user.username)
        # adicionando informações para o self.client
        # colocando o token no authorization para ter a permição de fazer a requisição
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # usando o self.client para fazer requisição usando o basename
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        # verifica se a rquisição deu certo
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # transforma a response em objeto
        product_data = json.loads(response.content)

        self.assertEqual(product_data["results"]
                         [0]['title'], self.product.title)
        self.assertEqual(product_data["results"]
                         [0]['price'], self.product.price)
        self.assertEqual(product_data["results"]
                         [0]['active'], self.product.active)

    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        category = CategoryFactory()
        # criação do objeto
        data = json.dumps({
            'title': 'notebook',
            'price': 2000,
            'category_id': [category.id]
        })

        # utilizando o delf.cliente que ja esta com authorization token
        # fazendo um post, data é as informações que esta sendo enviada
        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        # verificando se a requisição deu certo
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # faz um get de um objeto com title='notbook'
        created_product = Product.objects.get(title='notebook')

        self.assertEqual(created_product.title, 'notebook')
        self.assertEqual(created_product.price, 2000)
        self.assertEqual(created_product.active, True)
