from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import GitLabAPI


class LoginTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester', password='123')

    def test_not_logged_in(self):
        """
        tests whether a user can access the main page
        """
        response = self.client.get(reverse('core:homesite'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in")

    def test_logged_in(self):
        result = self.client.login(username='tester', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:homesite'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hi tester!")


# models test
class GitLabAPITests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester', password='test')
        User.objects.create_superuser('supertester', password='supertest')

    def test_GitLabAPI(self):
        empty_api = GitLabAPI()
        self.assertEqual(empty_api.api_name, '')
        self.assertEqual(empty_api.user_id, None)
        self.assertEqual(empty_api.url, '')
        self.assertEqual(empty_api.gitlab_api_token, '')

    def test_create_GitLabAPI_normal_user(self):
        """
        tests whether a user can create an API configuration
        """
        api_from_tester = GitLabAPI(
            user=User.objects.get(username='tester'),
            api_name='api from tester',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        api_from_tester.save()
        self.assertEqual(api_from_tester.api_name, 'api from tester')
        self.assertEqual(api_from_tester.user_id, 1)
        self.assertEqual(api_from_tester.url, 'https://testing.com/')
        self.assertTrue(isinstance(api_from_tester, GitLabAPI))

    def test_create_GitLabAPI_super_user(self):
        """
        tests whether a superuser can create an API configuration
        """
        api_from_supertester = GitLabAPI(
            user=User.objects.get(username='supertester'),
            api_name='api from supertester',
            url='lol',
            gitlab_api_token='mytesttoken'
        )
        self.assertEqual(api_from_supertester.api_name, 'api from supertester')
        self.assertEqual(api_from_supertester.user_id, 2)
        self.assertEqual(api_from_supertester.url, 'lol')
        self.assertTrue(isinstance(api_from_supertester, GitLabAPI))
