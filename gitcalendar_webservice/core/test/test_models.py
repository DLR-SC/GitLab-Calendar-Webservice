from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from core.models import GitLabAPI, CalendarConfiguration


class GitLabAPITests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester', password='test')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester'),
            api_name='api from tester',
            url='https://example.org/',
            gitlab_api_token='mytesttoken'
        )

    def test_gitlabapi_ok(self):
        empty_api = GitLabAPI(user_id=1, api_name='test api', url='https://example.org', gitlab_api_token="testtoken")
        empty_api.full_clean()
        empty_api.save()
        expected_api = GitLabAPI.objects.get(pk=2)
        self.assertEqual(expected_api.api_name, 'test api')

    def test_gitlabapi_not_ok(self):
        empty_api = GitLabAPI()
        with self.assertRaises(ValidationError) as ve:
            empty_api.full_clean()
        self.assertEqual(ve.exception.messages[0], 'This field cannot be null.')
        self.assertEqual(ve.exception.messages[1], 'This field cannot be blank.')
        self.assertEqual(ve.exception.messages[2], 'This field cannot be blank.')
        self.assertEqual(ve.exception.messages[3], 'This field cannot be blank.')

    def test_gitlabapi_deletion(self):
        self.assertTrue(GitLabAPI.objects.filter(pk=1).exists())
        GitLabAPI.objects.get(pk=1).delete()
        self.assertFalse(GitLabAPI.objects.filter(pk=1).exists())


class CalendarConfigTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester', password='test')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester'),
            api_name='api from tester',
            url='https://example.org/',
            gitlab_api_token='mytesttoken'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester'),
            api_id=1,
            config_name='test1',
            projects='28236929'
        )

    def test_calendarconfig_ok(self):
        calendar_config = CalendarConfiguration(user_id=1, api_id=1, config_name='test config',
                                                projects='10076', only_issues=True)
        calendar_config.full_clean()
        calendar_config.save()
        expected_config = CalendarConfiguration.objects.get(pk=2)
        self.assertEqual(expected_config.config_name, 'test config')
        self.assertEqual(expected_config.api.api_name, 'api from tester')
        self.assertEqual(expected_config.user.username, 'tester')
        self.assertTrue(isinstance(expected_config, CalendarConfiguration))

    def test_calendarconfig_not_ok(self):
        calendar_config = CalendarConfiguration()
        with self.assertRaises(ValidationError) as ve:
            calendar_config.full_clean()
        self.assertEqual(ve.exception.messages[0], 'This field cannot be null.')
        self.assertEqual(ve.exception.messages[1], 'This field cannot be null.')
        self.assertEqual(ve.exception.messages[2], 'This field cannot be blank.')
        self.assertEqual(ve.exception.messages[3], 'Please provide an entry for at least one project/group')
        self.assertEqual(ve.exception.messages[4], 'Please provide an entry for at least one project/group')

    def test_calendarconfig_deletion(self):
        self.assertTrue(CalendarConfiguration.objects.filter(pk=1).exists())
        CalendarConfiguration.objects.get(pk=1).delete()
        self.assertFalse(CalendarConfiguration.objects.filter(pk=1).exists())
