from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):
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
            text='Тествый пост',
            author=cls.user_author,
            group=cls.group,
        )
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

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        """Проверка создания поста."""
        post_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Отправить текст',
            'image': self.uploaded
        }
        self.post_author.post(
            reverse('post:post_create'), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        new_post = Post.objects.latest('id')
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.author, self.user_author)
        self.assertEqual(new_post.group.id, form_data['group'])
        self.assertTrue(new_post.image)

    def test_edit_post(self):
        """Проверка редактирования поста."""
        form_data = {
            'group': self.group.id,
            'text': 'Обновленный текст',
        }
        self.post_author.post(
            reverse('post:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data, follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                group=self.group.id,
                text='Обновленный текст',
            ).exists()
        )

    def test_anonymous_create_post(self):
        """Проверка создания записи анонимным пользователем."""
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Отправить текст',
        }
        response = self.guest_client.post(
            reverse('post:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_add_comment(self):
        """Проверка добавления комментария."""
        form_data = {
            'author': self.user_author,
            'post': self.post.id,
            'text': 'comment',
        }
        response = self.post_author.post(
            reverse('post:add_comment', kwargs={'post_id': self.post.id}
                    ),
            data=form_data,
            follow=True
        )
        response_comment = response.context['comments'].count()
        self.assertEqual(response_comment, 1)
