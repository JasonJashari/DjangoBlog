from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django_webtest import WebTest


class RegisterPageTest(TestCase):

    def test_basic_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(WebTest):

    def test_form_error(self):
        page = self.app.get(reverse('register'))
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(reverse('register'))
        page.form['username'] = "some_user"
        page.form['email'] = "some_user@example.com"
        page.form['first_name'] = "First"
        page.form['password1'] = "TestingPassword123"
        page.form['password2'] = "TestingPassword123"

        page = page.form.submit()
        self.assertRedirects(page, reverse('login'))

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)


class LoginPageTest(TestCase):

    def test_basic_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class LoginViewTest(WebTest):

    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password
        )
    
    def test_login_error(self):
        page = self.app.get(reverse('login'))
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_login_success(self):
        response = self.client.post(
                                    reverse('login'),
                                    {'username': self.username,
                                    'password': self.password},
                                    follow=True
        )
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse('home'))


class LogoutViewTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user', password='test_password'
        )

    def test_logout(self):
        self.client = Client()
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)


class UserProfileTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user', password='test_password'
        )
    
    def test_profile_page_logged_in(self):
        self.client = Client()
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
    
    def test_profile_page_logged_out(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('login') + f"?next={reverse('profile')}")