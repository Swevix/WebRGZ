from django import forms
from .models import Car
from django.utils.safestring import mark_safe
from .models import Comment

# 1. Собственный валидатор: запрет цифр в названии
def validate_title_no_digits(value):
    if any(ch.isdigit() for ch in value):
        raise forms.ValidationError(
            'Название не должно содержать цифр',
            code='no_digits'
        )

# 2. Собственный валидатор: запрет слова "test"
def validate_no_test(value):
    if 'test' in value.lower():
        raise forms.ValidationError(
            'Слово "test" запрещено в названии',
            code='no_test'
        )

# Несвязанная с моделью форма
class CarForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label='Название автомобиля',
        validators=[validate_title_no_digits],
        help_text='До 255 символов, без цифр')
    help_text = mark_safe(
        'Число от 0 до 10 с двумя знаками после точки'
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Описание',
        help_text='Дополнительная информация (необязательно)'
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Цена, €',
        min_value=0,
        help_text='Число от 0 до 10<sup>10</sup> с двумя знаками после точки'
    )
    image = forms.ImageField(
        required=False,
        label='Изображение',
        help_text='JPG/PNG до 5 МБ'
    )

# Форма, связанная с моделью
class CarModelForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        label='Название автомобиля',
        validators=[validate_no_test, validate_title_no_digits],
        help_text='Без цифр и слова "test"'
    )
    image = forms.ImageField(
        required=False,
        label='Изображение',
        help_text='JPG/PNG до 5 МБ'
    )


    class Meta:
        model = Car
        fields = [
            'title',
            'slug',
            'description',
            'price',
            'manufacturer',
            'tags',
            'image',
        ]
        widgets = {
            'description': forms.Textarea,
        }

class UploadForm(forms.Form):
    file = forms.FileField(
        label='Выберите файл',
        help_text='Максимум 10 МБ. Любой тип.'
    )

    def clean_file(self):
        f = self.cleaned_data['file']
        if f.size > 10 * 1024 * 1024:
            raise forms.ValidationError('Файл слишком большой (больше 10 МБ)')
        return f

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'})
        }
        labels = {
            'text': 'Комментарий'
        }