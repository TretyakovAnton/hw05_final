from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def test_post_str(self):
        """Проверка __str__ у post."""
        self.assertEqual(self.post.text[:15], str(self.post))

    def test_post_verbose_name(self):
        """Проверка verbose_name у post."""
        post = PostModelTest.post
        field_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата',
            'author': 'Автор',
            'group': 'Группа',
            'image': 'Картинка',

        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_help_text(self):
        """Проверка help_text у post."""
        post = PostModelTest.post
        feild_help_texts = {
            'text': 'Введите текст нового поста',
            'pub_date': 'Дата поста',
            'author': 'Автор поста',
            'group': 'Выбор группы к которой относится текст',
            'image': 'Картинка отображаемая в посте',

        }
        for field, expected_value in feild_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_post_str(self):
        """Проверка __str__ у group."""
        self.assertEqual(self.group.title, str(self.group))

    def test_group_verbose_name(self):
        """Проверка verbose_name у group."""
        group = GroupModelTest.group
        field_verbose = {
            'title': 'Заголовок',
            'slug': 'Slug',
            'description': 'Описание',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value
                )

    def test_group_help_text(self):
        """Проверка help_text у group."""
        group = GroupModelTest.group
        feild_help_texts = {
            'description': 'Введите описание группы'
        }
        for field, expected_value in feild_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value
                )
