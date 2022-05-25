from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack


# Create your tests here.

class SnacksTests(TestCase):
    def setUp(self):
        purchaser = get_user_model().objects.create(username='tester',password='tester')
        Snack.objects.create(name='test sandwhich', purchaser=purchaser, description='Test Description')

    def test_snack_list_page(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_snack_list_template(self):
        url = reverse('snack_list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_list_page_context(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        snacks = response.context['object_list']
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].name, 'test sandwhich')
        self.assertEqual(snacks[0].purchaser.username, 'tester')
        self.assertEqual(snacks[0].description, 'Test Description')

    def test_detail_page_status_code(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        snack = response.context['snack']
        self.assertEqual(snack.name, 'test sandwhich')
        self.assertEqual(snack.description, 'Test Description')
        self.assertEqual(snack.purchaser.username, 'tester')

    def test_404(self):
        url = 'missing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
