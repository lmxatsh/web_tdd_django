from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

# Create your tests here.

class HomePageTest(TestCase):

    def test_user_home_template(self):        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_save_nothing_after_GET(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_can_save_a_POST_to_an_existing_list(self):
        list_a = List.objects.create()
        list_b = List.objects.create()

        self.client.post(f'/lists/{list_a.id}/', data={'item_text': 'new item of list_a'})        
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(list=list_a).text, 'new item of list_a')
        self.assertEqual(Item.objects.get(list=list_a).list, list_a)

    def test_redirect_to_list_view(self):
        list_a = List.objects.create()
        list_b = List.objects.create()
        response = self.client.post(f'/lists/{list_a.id}/', data={'item_text': 'new item of list_a'})
        self.assertRedirects(response, f'/lists/{list_a.id}/')

    
    def test_validationerror_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        err_msg = 'empty item not allowed'
        self.assertContains(response, err_msg)

    def test_duplicate_item_validation_erros_endup_on_list_pages(self):
        list_a = List.objects.create()
        item_a = Item.objects.create(list=list_a, text='item_a')
        response = self.client.post(
            f'/lists/{list_a.id}/',
            data={'item_text':'item_a'}
        )
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, 'duplicate item')



class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'New List Item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'New List Item')

    
    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertEqual(response['location'], f'/lists/{new_list.id}/')     

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_item_arent_saved(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)








        

