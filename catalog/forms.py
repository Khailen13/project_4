from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = [
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "name": "Укажите наименование",
            "description": "Добавьте описание",
            "image": "",
            "category": "",
            "price": "Укажите цену",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control"})
            if placeholder:
                self.fields[field].widget.attrs.update({"placeholder": placeholder})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in name.lower():
                raise ValidationError(f'Название продукта не должно содержать запрещенное слово "{forbidden_word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in description.lower():
                raise ValidationError(f'Описание продукта не должно содержать запрещенное слово "{forbidden_word}".')
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена продукта не должна быть отрицательной.")
        return price
