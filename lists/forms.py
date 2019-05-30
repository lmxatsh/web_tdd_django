from django import forms
from lists.models import Item, List
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = 'empty item not allowed'
DUPLICATE_ITEM_ERROR = 'duplicate item'
class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget = forms.fields.TextInput(
            attrs={
                'placeholder':'Enter a to-do item',
                'class': 'form-control input-lg',
            }
        ),
        error_messages = {'required': EMPTY_ITEM_ERROR,
        }
    )
   

    def save(self, for_list):
        if self.is_valid():
            return Item.objects.create(text=self.cleaned_data.get('item_text'), list=for_list)


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super(ExistingListItemForm,self).__init__(*args, **kwargs)
        self.for_list = for_list

    def clean_item_text(self):
        if len(Item.objects.filter(list=self.for_list, text=self.cleaned_data.get('item_text'))) > 0:
            raise ValidationError(DUPLICATE_ITEM_ERROR)
        else:
            return self.cleaned_data['item_text']