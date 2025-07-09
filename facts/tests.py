from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Fact, Category, UserSavedFact

# Create your tests here.

class FactViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Наука')
        self.fact = Fact.objects.create(text='Вода кипить при 100°C.', category=self.category)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'random_fact.html')
        self.assertIn('fact', response.context)

    def test_categories_page(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')
        self.assertIn('categories', response.context)
        self.assertContains(response, 'Наука')

    def test_add_fact(self):
        response = self.client.post(reverse('add_fact'), {
            'text': 'Гравітація існує!',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(Fact.objects.filter(text='Гравітація існує!').exists())

    def test_add_category(self):
        response = self.client.post(reverse('add_category'), {'name': 'Тварини'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Тварини').exists())

    def test_saved_facts_requires_login(self):
        response = self.client.get(reverse('saved_facts'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_saved_facts_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        saved = UserSavedFact.objects.create(user=self.user, fact=self.fact)
        response = self.client.get(reverse('saved_facts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved_facts.html')
        self.assertContains(response, 'Вода кипить при 100°C.')
