from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase):

    def test_user_home_template(self):        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_save_nothing_after_GET(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    




    

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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_items_for_differnt_list(self):
        list_a = List.objects.create()
        list_b = List.objects.create()

        Item.objects.create(text='item 1a', list=list_a)
        Item.objects.create(text='item 2a', list=list_a)

        Item.objects.create(text='item 1b', list=list_b)
        Item.objects.create(text='item 2b', list=list_b)

        response = self.client.get(f'/lists/{list_a.id}/')
        self.assertContains(response, 'item 1a')
        self.assertContains(response, 'item 2a')
        self.assertNotContains(response, 'item 1b')
        self.assertNotContains(response, 'item 2b')

        response = self.client.get(f'/lists/{list_b.id}/')
        self.assertContains(response, 'item 1b')
        self.assertContains(response, 'item 2b')

    
    def test_passes_correct_to_template(self):
        list_a = List.objects.create()
        response = self.client.get(f'/lists/{list_a.id}/')
        self.assertEqual(response.context['list'], list_a) 



    def test_users_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'New List Item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'New List Item')

    
    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertEqual(response['location'], f'/lists/{new_list.id}/')

    def test_can_save_a_POST_to_an_existing_list(self):
        list_a = List.objects.create()
        list_b = List.objects.create()

        self.client.post(f'/lists/{list_a.id}/add_item', data={'item_text': 'new item of list_a'})        
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(list=list_a).text, 'new item of list_a')

        self.client.post(f'/lists/{list_b.id}/add_item', data={'item_text': 'new item of list_b'})
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(list=list_b).text, 'new item of list_b')

    
    def test_redirect_to_list_view(self):
        list_a = List.objects.create()
        list_b = List.objects.create()
        response = self.client.post(f'/lists/{list_a.id}/add_item', data={'item_text': 'new item of list_a'})
        self.assertRedirects(response, f'/lists/{list_a.id}/')
        







        

