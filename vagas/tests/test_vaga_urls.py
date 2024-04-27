from django.test import TestCase
from django.urls import reverse


class VagaURLsTest(TestCase):
    def test_vaga_home_url_is_correct(self):
        url = reverse('vagas:home')
        self.assertEqual(url, '/')

    def test_vaga_category_url_is_correct(self):
        url = reverse('vagas:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/vagas/category/1/')

    def test_vaga_detail_url_is_correct(self):
        url = reverse('vagas:vaga', kwargs={'pk': 1})
        self.assertEqual(url, '/vagas/1/')

    def test_vaga_search_url_is_correct(self):
        url = reverse('vagas:search')
        self.assertEqual(url, '/vagas/search/')

# RED - GREEN - REFACTOR
