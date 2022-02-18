from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from ..models import Post, Group, Follow
from ..forms import PostForm

User = get_user_model()

TEN_POST = 10
THREE_POST = 3


class TestPostsViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create(username='user_author')
        cls.post_author = Client()
        cls.post_author.force_login(cls.user_author)

        cls.another_user = User.objects.create(username='another_user')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.another_user)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый описание',
            slug='test_slug'
        )
        cls.group_2 = Group.objects.create(
            title='Тестовый заголовок 2',
            description='Тестовый описание 2',
            slug='test_slug_2'
        )
        cls.post = Post.objects.create(
            text='Тествый пост',
            author=cls.user_author,
            group=cls.group,
            image=cls.uploaded
        )

    def setUp(self):
        self.guest_client = Client()
        cache.clear()

    def test_correct_context_index(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('post:index'))
        self.assertEqual(response.context.get('page_obj')[0], self.post)

    def test_correct_context_group(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.post_author.get(
            reverse('post:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context.get('page_obj')[0], self.post)
        self.assertEqual(response.context.get('group'), self.post.group)

    def test_correct_context_profile(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.post_author.get(
            reverse('post:profile', kwargs={'username': self.post.author})
        )
        self.assertEqual(response.context.get('page_obj')[0], self.post)
        self.assertEqual(response.context.get('author'), self.post.author)

    def test_correct_context_post_detail(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.post_author.get(
            reverse('post:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context.get('post_id'), self.post.id)

    def test_correct_context_post_edit(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.post_author.get(
            reverse('post:post_edit', kwargs={'post_id': self.post.id})
        )
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['post'], self.post)
        self.assertTrue(response.context['is_edit'])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_correct_context_post_create(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.post_author.get(reverse("post:post_create"))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_after_create_in_index(self):
        """Проверка, что пост попадает на главную."""
        response = self.post_author.get(reverse('post:index'))
        self.assertEqual(response.context['page_obj'][0], self.post)

    def test_post_after_create_in_self_group(self):
        """Проверка, что пост попадает в свою группу."""
        response = self.post_author.get(
            reverse('post:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['page_obj'][0], self.post)

    def test_post_after_create_not_in_another_group(self):
        """Проверка, что пост не попадает в чужую группу."""
        response = self.post_author.get(
            reverse('post:group_list', kwargs={'slug': self.group_2.slug})
        )
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_cache(self):
        """Тест кеширования главной страницы."""
        response = self.post_author.get(reverse('posts:index'))
        cache_check = response.content
        post = Post.objects.get(pk=1)
        post.delete()
        response = self.post_author.get(reverse('posts:index'))
        self.assertEqual(response.content, cache_check)
        cache.clear()
        response = self.post_author.get(reverse('posts:index'))
        self.assertNotEqual(response.content, cache_check)

    def test_follow(self):
        """ Проверяется, что после подписки появится новый обект Follow."""
        follow = reverse('posts:profile_follow',
                         kwargs={'username': self.another_user})
        self.post_author.get(follow, follow=True)
        self.assertEqual(Follow.objects.all().count(), 1)

    def test_unfollow(self):
        """ а после отписки он исчезнет."""
        unfollow = reverse('posts:profile_unfollow',
                           kwargs={'username': self.another_user})
        self.post_author.get(unfollow, follow=True)
        self.assertEqual(Follow.objects.all().count(), 0)


class PaginatorViewsTest(TestCase):
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
        for i in range(13):
            Post.objects.create(
                text=f'Тествый пост №{i}',
                author=cls.user_author,
                group=cls.group,
            )

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_ten_post(self):
        """Первая странца имеет 10 постов."""
        pages = [
            reverse('post:index'),
            reverse('post:group_list', kwargs={'slug': self.group.slug}),
            reverse('post:profile', kwargs={'username': self.user_author}),
        ]
        for key in pages:
            with self.subTest(key=key):
                response = self.guest_client.get(key)
                self.assertEqual(len(response.context['page_obj']), TEN_POST)

    def test_second_page_three_post(self):
        """Вторая странца имеет 3 поста."""
        pages = [
            reverse('post:index'),
            reverse('post:group_list', kwargs={'slug': self.group.slug}),
            reverse('post:profile', kwargs={'username': self.user_author}),
        ]
        for key in pages:
            with self.subTest(key=key):
                response = self.guest_client.get(key, {'page': 2})
                self.assertEqual(len(response.context['page_obj']), THREE_POST)
