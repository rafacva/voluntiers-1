from unittest.mock import patch

from django.urls import resolve, reverse
from vagas import views

from .test_vaga_base import VagaTestBase


class VagaHomeViewTest(VagaTestBase):
    def test_vaga_home_view_function_is_correct(self):
        view = resolve(reverse('vagas:home'))
        self.assertIs(view.func.view_class, views.VagaListViewHome)

    def test_vaga_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('vagas:home'))
        self.assertEqual(response.status_code, 200)

    def test_vaga_home_view_loads_correct_template(self):
        response = self.client.get(reverse('vagas:home'))
        self.assertTemplateUsed(response, 'vagas/pages/home.html')

    def test_vaga_home_template_shows_no_vagas_found_if_no_vagas(self):
        response = self.client.get(reverse('vagas:home'))
        self.assertIn(
            '<h1>No vagas found here 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_vaga_home_template_loads_vagas(self):
        # Need a vaga for this test
        self.make_vaga()

        response = self.client.get(reverse('vagas:home'))
        content = response.content.decode('utf-8')
        response_context_vagas = response.context['vagas']

        # Check if one vaga exists
        self.assertIn('Vaga Title', content)
        self.assertEqual(len(response_context_vagas), 1)

    def test_vaga_home_template_dont_load_vagas_not_published(self):
        """Test vaga is_published False dont show"""
        # Need a vaga for this test
        self.make_vaga(is_published=False)

        response = self.client.get(reverse('vagas:home'))

        # Check if one vaga exists
        self.assertIn(
            '<h1>No vagas found here 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_vaga_home_is_paginated(self):
        self.make_vaga_in_batch(qtd=8)

        with patch('vagas.views.PER_PAGE', new=3):
            response = self.client.get(reverse('vagas:home'))
            vagas = response.context['vagas']
            paginator = vagas.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_vaga_in_batch(qtd=8)

        with patch('vagas.views.PER_PAGE', new=3):
            response = self.client.get(reverse('vagas:home') + '?page=12A')
            self.assertEqual(
                response.context['vagas'].number,
                1
            )
            response = self.client.get(reverse('vagas:home') + '?page=2')
            self.assertEqual(
                response.context['vagas'].number,
                2
            )
            response = self.client.get(reverse('vagas:home') + '?page=3')
            self.assertEqual(
                response.context['vagas'].number,
                3
            )
