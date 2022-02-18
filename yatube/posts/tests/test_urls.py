from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

from ..models import Post, Group

User = get_user_model()


class StaticPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create(username='user_author')
        cls.post_author = Client()
        cls.post_author.force_login(cls.user_author)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый описание',
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            text='Тествый текст',
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.another_user = User.objects.create(username='another_user')
        self.authorized_user = Client()
        self.authorized_user.force_login(self.another_user)
        cache.clear()

    def test_url_anonymous(self):
        """Проверка доступности адресов."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test_slug/',
            'posts/profile.html': '/profile/user_author/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertTemplateUsed(response, template)

    def test_url_create_redirect_anonymous_on_login(self):
        """Страница по адресу create перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('post:post_create'),
            follow=True
        )
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_url_follow_redirect_anonymous_on_login(self):
        """Страница по адресу follow перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('post:follow_index'),
            follow=True
        )
        self.assertRedirects(
            response, '/auth/login/?next=/follow/'
        )

    def test_url_edit_post_anonymous_on_login(self):
        """Страница по адресу /post.id/edit перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('post:post_edit', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.id}/edit/'
        )

    def test_url_authorization_user(self):
        """Проверка доступности адресов."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test_slug/',
            'posts/profile.html': '/profile/user_author/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
            'posts/create_post.html': '/create/',
            'posts/follow.html': '/follow/'
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_user.get(address, follow=True)
                self.assertTemplateUsed(response, template)

    def test_url_not_adress(self):
        """Страница по ошибочному адресу выводит 404."""
        response = self.guest_client.get('/any/', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_edit_authorization_user(self):
        """Если не автор поста редирект на просмотр поста."""
        response = self.authorized_user.get(
            reverse('post:post_edit', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertRedirects(response, f'/posts/{self.post.id}/')

    def test_url_edit_post_author_user(self):
        """Если автор поста открывается редактирование поста."""
        response = self.post_author.get(
            reverse('post:post_edit', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
