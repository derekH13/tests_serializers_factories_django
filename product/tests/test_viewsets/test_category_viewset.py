import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='GPU')

    def test_get_all_category(self):
        # requsição de no basename category-list
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # passando para json
        category_data = json.loads(response.content)
        # confere se o title do category criado é igual au que foi feito antes
        self.assertEqual(category_data["results"]
                         [0]['title'], self.category.title)

    def test_create_category(self):
        data = json.dumps({
            'title': 'CPU',
        })

        # fazendo um post no basname category-list, enviando o data no request
        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # fazendo um get em procurando um title = 'CPU'
        created_category = Category.objects.get(title='CPU')

        self.assertEqual(created_category.title, 'CPU')
