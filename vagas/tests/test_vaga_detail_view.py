from django.urls import resolve, reverse
from vagas import views

from .test_vaga_base import VagaTestBase


class VagaDetailViewTest(VagaTestBase):
    def test_vaga_detail_view_function_is_correct(self):
        view = resolve(
            reverse('vagas:vaga', kwargs={'pk': 1})
        )
        self.assertIs(view.func.view_class, views.VagaDetail)

    def test_vaga_detail_view_returns_404_if_no_vagas_found(self):
        response = self.client.get(
            reverse('vagas:vaga', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_vaga_detail_template_loads_the_correct_vaga(self):
        needed_title = 'This is a detail page - It load one vaga'

        # Need a vaga for this test
        self.make_vaga(title=needed_title)

        response = self.client.get(
            reverse(
                'vagas:vaga',
                kwargs={
                    'pk': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # Check if one vaga exists
        self.assertIn(needed_title, content)

    def test_vaga_detail_template_dont_load_vaga_not_published(self):
        """Test vaga is_published False dont show"""
        # Need a vaga for this test
        vaga = self.make_vaga(is_published=False)

        response = self.client.get(
            reverse(
                'vagas:vaga',
                kwargs={
                    'pk': vaga.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
