from django.test import TestCase

from vagas.models import Category, Vaga, User


class VagaMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_vaga(
        self,
        category_data=None,
        author_data=None,
        title='Vaga Title',
        description='Vaga Description',
        slug='vaga-slug',
        time=10,
        time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        steps='Vaga Preparation Steps',
        steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Vaga.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            time=time,
            time_unit=time_unit,
            servings=servings,
            servings_unit=servings_unit,
            steps=steps,
            steps_is_html=steps_is_html,
            is_published=is_published,
        )

    def make_vaga_in_batch(self, qtd=10):
        vagas = []
        for i in range(qtd):
            kwargs = {
                'title': f'Vaga Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            vaga = self.make_vaga(**kwargs)
            vagas.append(vaga)
        return vagas


class VagaTestBase(TestCase, VagaMixin):
    def setUp(self) -> None:
        return super().setUp()
