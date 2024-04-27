from django.urls import resolve, reverse
from vagas import views

from .test_vaga_base import VagaTestBase


class VagaSearchViewTest(VagaTestBase):
    def test_vaga_search_uses_correct_view_function(self):
        resolved = resolve(reverse('vagas:search'))
        self.assertIs(resolved.func.view_class, views.VagaListViewSearch)

    def test_vaga_search_loads_correct_template(self):
        response = self.client.get(reverse('vagas:search') + '?q=teste')
        self.assertTemplateUsed(response, 'vagas/pages/search.html')

    def test_vaga_search_raises_404_if_no_search_term(self):
        url = reverse('vagas:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_vaga_search_term_is_on_page_title_and_escaped(self):
        url = reverse('vagas:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_vaga_search_can_find_vaga_by_title(self):
        title1 = 'This is vaga one'
        title2 = 'This is vaga two'

        vaga1 = self.make_vaga(
            slug='one', title=title1, profile_data={'username': 'one'}
        )
        vaga2 = self.make_vaga(
            slug='two', title=title2, profile_data={'username': 'two'}
        )

        search_url = reverse('vagas:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(vaga1, response1.context['vagas'])
        self.assertNotIn(vaga2, response1.context['vagas'])

        self.assertIn(vaga2, response2.context['vagas'])
        self.assertNotIn(vaga1, response2.context['vagas'])

        self.assertIn(vaga1, response_both.context['vagas'])
        self.assertIn(vaga2, response_both.context['vagas'])
