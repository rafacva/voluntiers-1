from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_vaga_base import Vaga, VagaTestBase


class VagaModelTest(VagaTestBase):
    def setUp(self) -> None:
        self.vaga = self.make_vaga()
        return super().setUp()

    def make_vaga_no_defaults(self):
        vaga = Vaga(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Vaga Title',
            description='Vaga Description',
            slug='vaga-slug-for-no-defaults',
            time=10,
            time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            steps='Vaga Preparation Steps',
        )
        vaga.full_clean()
        vaga.save()
        return vaga

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_vaga_fields_max_length(self, field, max_length):
        setattr(self.vaga, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.vaga.full_clean()

    def test_vaga_steps_is_html_is_false_by_default(self):
        vaga = self.make_vaga_no_defaults()
        self.assertFalse(
            vaga.steps_is_html,
            msg='Vaga steps_is_html is not False',
        )

    def test_vaga_is_published_is_false_by_default(self):
        vaga = self.make_vaga_no_defaults()
        self.assertFalse(
            vaga.is_published,
            msg='Vaga is_published is not False',
        )

    def test_vaga_string_representation(self):
        needed = 'Testing Representation'
        self.vaga.title = needed
        self.vaga.full_clean()
        self.vaga.save()
        self.assertEqual(
            str(self.vaga), needed,
            msg=f'Vaga string representation must be '
                f'"{needed}" but "{str(self.vaga)}" was received.'
        )
