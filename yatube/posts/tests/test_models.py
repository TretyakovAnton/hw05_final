from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, Follow, Comment

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст должен быть больше 15 символов',
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


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.follower = User.objects.create_user(username='follower')
        cls.follow = Follow.objects.create(
            author=cls.author,
            user=cls.follower
        )

    def test_follow_str(self):
        """Проверка __str__ у follow."""
        self.assertEqual(self.follow.user, self.follower)

    def test_follow_verbose_name(self):
        """Проверка verbose_name у follow."""
        follow = FollowModelTest.follow
        field_verbose = {
            'author': 'На кого подписались',
            'user': 'Подписчик',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name, expected_value
                )


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментрий',
        )

    def test_comment_str(self):
        """Проверка __str__ у comment."""
        self.assertEqual(self.post.text, str(self.post))

    def test_comment_verbose_name(self):
        """Проверка verbose_name у comment."""
        comment = CommentModelTest.comment
        field_verbose = {
            'text': 'Текст комментария',
            'created': 'Дата публикации',
            'author': 'Автор',
            'post': 'Пост',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name, expected_value
                )

    def test_comment_help_text(self):
        """Проверка help_text у comment."""
        comment = CommentModelTest.comment
        feild_help_texts = {
            'text': 'Введите комментарий',
            'created': 'Дата комментария',
            'author': 'Автор комментария',
            'post': 'Комментируемый пост',
        }
        for field, expected_value in feild_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text, expected_value
                )
