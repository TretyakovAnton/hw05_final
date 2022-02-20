from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу',
            'image': 'Загрузите картинку'
        }
        help_text = {
            'text': 'Введите любой текст',
            'group': 'Выбирите группу из списка',
            'image': 'Загрузите картинку с компьтера '
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Оставьте комментарий',
        }
        help_text = {
            'text': 'Вы можете оставьте комментарий к посту',
        }
