from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

# Based on what I have found on internet there are three different tests writing for django apps
# 1st: writing Django tests for views
# e.g: testing if Login or signup is working alright or not
# 2nd: writningDjango tests for models
# e.g:
# 3rd: writing Django tests for urls

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_view(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, '/home/')