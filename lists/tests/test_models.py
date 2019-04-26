from django.test import TestCase
from lists.models import Item, List

class ListAndItemModelTest(TestCase):

    def test_saving_and_retriving_items(self):
        list_ = List.objects.create()
        list_.save()


        first_item = Item()
        first_item.text = '1st item from 1st list'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '2ed item from 1st list'
        second_item.list = list_
        second_item.save()

        self.assertEqual(List.objects.first(), list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, '1st item from 1st list')
        self.assertEqual(saved_items[0].list, list_)
        
        self.assertEqual(saved_items[1].text, '2ed item from 1st list')
        self.assertEqual(saved_items[1].list, list_)