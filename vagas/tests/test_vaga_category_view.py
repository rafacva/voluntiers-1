from django.urls import resolve, reverse
from vagas import views

from .test_vaga_base import VagaTestBase


class VagaCategoryViewTest(VagaTestBase):
    def test_vaga_category_view_function_is_correct(self):
        view = resolve(
            reverse('vagas:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func.view_class, views.VagaListViewCategory)

    def test_vaga_category_view_returns_404_if_no_vagas_found(self):
        response = self.client.get(
            reverse('vagas:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_vaga_category_template_loads_vagas(self):
        needed_title = 'This is a category test'
        # Need a vaga for this test
        self.make_vaga(title=needed_title)

        response = self.client.get(reverse('vagas:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one vaga exists
        self.assertIn(needed_title, content)

    def test_vaga_category_template_dont_load_vagas_not_published(self):
        """Test vaga is_published False dont show"""
        # Need a vaga for this test
        vaga = self.make_vaga(is_published=False)

        response = self.client.get(
            reverse('vagas:vaga', kwargs={'pk': vaga.category.id})
        )

        self.assertEqual(response.status_code, 404)
