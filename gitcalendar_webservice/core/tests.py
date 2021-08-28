from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import GitLabAPI, CalendarConfiguration


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
        GitLabAPI.objects.create(
            user=User.objects.get(username='supertester'),
            api_name='api from supertester',
            url='lol',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester'),
            api_name='api from tester',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
            user=User.objects.get(username='supertester'),
            api_name='api',
            url='lol',
            gitlab_api_token='mytesttoken2'
        )

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
        api_from_tester = GitLabAPI.objects.get(pk=2)
        api_from_tester.save()
        self.assertEqual(api_from_tester.api_name, 'api from tester')
        self.assertEqual(api_from_tester.user_id, 1)
        self.assertEqual(api_from_tester.url, 'https://testing.com/')
        self.assertTrue(isinstance(api_from_tester, GitLabAPI))
        self.assertTrue(isinstance(api_from_tester.user, User))
        self.assertTrue(isinstance(api_from_tester.url, str))
        self.assertTrue(isinstance(api_from_tester.gitlab_api_token, str))

    def test_GitLabAPI_deletion(self):
        self.assertTrue(GitLabAPI.objects.filter(api_name='api').exists())
        GitLabAPI.objects.get(api_name='api').delete()
        self.assertFalse(GitLabAPI.objects.filter(api_name='api').exists())


class CalendarConfigTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester', password='test')
        User.objects.create_superuser('supertester', password='supertest')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester'),
            api_name='api from tester',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester'),
            api_id=1,
            config_name='test1',
            projects='28236929'
        )

    def test_CalendarConfig(self):
        empty_calendar_config = CalendarConfiguration()
        self.assertTrue(isinstance(empty_calendar_config, CalendarConfiguration))
        self.assertEqual(empty_calendar_config.user_id, None)
        self.assertEqual(empty_calendar_config.api_id, None)
        self.assertEqual(empty_calendar_config.config_name, '')
        self.assertEqual(empty_calendar_config.projects, '')
        self.assertEqual(empty_calendar_config.groups, '')
        self.assertEqual(empty_calendar_config.reminder, 0.0)
        self.assertFalse(empty_calendar_config.only_issues)
        self.assertFalse(empty_calendar_config.only_milestones)
        self.assertFalse(empty_calendar_config.combined)

    def test_create_CalendarConfig_from_user(self):
        config = CalendarConfiguration(user=User.objects.get(username='tester'),
                                       api_id=1, config_name='test', only_issues=True)
        self.assertEqual(config.config_name, 'test')
        self.assertEqual(config.api_id, 1)
        self.assertEqual(config.api.api_name, 'api from tester')
        self.assertEqual(config.user.username, 'tester')
        self.assertTrue(config.only_issues)

    def test_CalendarConfig_deletion(self):
        self.assertTrue(CalendarConfiguration.objects.filter(config_name='test1').exists())
        CalendarConfiguration.objects.get(config_name='test1').delete()
        self.assertFalse(CalendarConfiguration.objects.filter(config_name='test1').exists())


class GitLabAPIViewTests(TestCase):

    def setUp(self) -> None:
        User.objects.create_superuser('tester1', password='123')
        User.objects.create_user('tester2', password='123')
        User.objects.create_user('tester3', password='123')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='api from tester1',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
                user=User.objects.get(username='tester2'),
                api_name='api from tester2',
                url='https://testing.com/',
                gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester3'),
            api_name='api from tester3',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        self.update1 = {
            "api_name": "api from tester1",
            "url": "https://testing.com/",
            "gitlab_api_token": "mynewsupertesttoken"
        }
        self.update2 = {
            "api_name": "api from tester2",
            "url": "https://testing.com/",
            "gitlab_api_token": "mynewtesttoken"
        }

    def test_gitlabapi_list_views_when_not_logged_in(self):
        """
        tests if the GitLabAPI list can be accessed without being logged in
        """
        response = self.client.get(reverse('core:gitlabapi.list'))
        self.assertEqual(response.status_code, 404)

    def test_own_gitlabapi_list_views_for_user(self):
        """
        tests the own GitLabAPI list  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Actions')
        self.assertContains(response, 'api from tester2')

    def test_gitlabapi_detail_views_when_not_logged_in(self):
        """
        tests if the GitLabAPI detail can be accessed without being logged in
        """
        response = self.client.get(reverse('core:gitlabapi.detail', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_gitlabapi_detail_views_for_user(self):
        """
        tests the own GitLabAPI detail  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.detail', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'URL')
        self.assertContains(response, 'api from tester2')

    def test_foreign_gitlabapi_detail_views_with_user(self):
        """
        tests if a foreign GitLabAPI detail can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.detail', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_gitlabapi_edit_views_when_not_logged_in(self):
        """
        tests if the GitLabAPI update view can be accessed without being logged in
        """
        response = self.client.get(reverse('core:gitlabapi.update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_gitlabapi_edit_views_for_user(self):
        """
        tests the own GitLabAPI update view of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.update', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Url')
        self.assertContains(response, 'api from tester2')
        updated_response = self.client.post(reverse('core:gitlabapi.update', args=[2]), self.update2)
        self.assertEqual(updated_response.status_code, 302)
        GitLabAPI.objects.get(pk=2).refresh_from_db()
        self.assertEqual(GitLabAPI.objects.get(pk=2).gitlab_api_token, "mynewtesttoken")

    def test_foreign_gitlabapi_edit_views_with_user(self):
        """
        tests if a foreign GitLabAPI update view can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.update', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_gitlabapi_creation_view_when_not_logged_in(self):
        """
        tests if a GitLabAPI can be created when not logged in
        """
        response = self.client.get(reverse('core:gitlabapi.add'))
        self.assertEqual(response.status_code, 302)

    def test_gitlabapi_creation_view_of_any_user(self):
        """
        tests if every logged in user can create a GitLabAPI
        """
        result = self.client.login(username='tester1', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:gitlabapi.add'), self.update1)
        self.assertEqual(response.status_code, 302)
        api1 = GitLabAPI.objects.get(pk=4)
        self.assertEqual(api1.user.username, 'tester1')
        self.assertEqual(api1.gitlab_api_token, 'mynewsupertesttoken')
        self.client.logout()

        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:gitlabapi.add'), self.update2)
        self.assertEqual(response2.status_code, 302)
        api1 = GitLabAPI.objects.get(pk=5)
        self.assertEqual(api1.user.username, 'tester2')
        self.assertEqual(api1.gitlab_api_token, 'mynewtesttoken')

    def test_gitlabapi_deletion_view_when_not_logged_in(self):
        """
        tests if a GitLabAPI can be created when not logged in
        """
        response = self.client.get(reverse('core:gitlabapi.delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_gitlabapi_deletion_view_of_user(self):
        """
        tests if a logged in user can delete his own GitLabAPI
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:gitlabapi.delete', args=[2]))
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(GitLabAPI.objects.filter(pk=2).exists())

    def test_foreign_gitlabapi_deletion_view_of_user(self):
        """
        tests if a logged in user can delete a foreign GitLabAPI
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:gitlabapi.delete', args=[3]))
        self.assertEqual(response2.status_code, 403)


class CalendarConfigurationViewTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser('tester1', password='123')
        User.objects.create_user('tester2', password='123')
        User.objects.create_user('tester3', password='123')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='api from tester1',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
                user=User.objects.get(username='tester2'),
                api_name='api from tester2',
                url='https://testing.com/',
                gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester3'),
            api_name='api from tester3',
            url='https://testing.com/',
            gitlab_api_token='mytesttoken'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester1'),
            api_id=1,
            config_name='config from tester1',
            projects='28236929'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester2'),
            api_id=2,
            config_name='config from tester2',
            projects='28236929,abc'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester3'),
            api_id=3,
            config_name='config from tester3',
            projects='28236929,abcd'
        )

        self.update1 = {
            "api": 1,
            "projects": "28236929,abcdefg",
            "groups": "",
            "config_name": "new config from tester1",
            "only_issues": False,
            "only_milestones": False,
            "combined": False,
            "reminder": 0.0,
        }
        self.update2 = {
            "api": 2,
            "projects": "28236929,abcdefghijk",
            "groups": "",
            "config_name": "new config from tester2",
            "only_issues": False,
            "only_milestones": False,
            "combined": False,
            "reminder": 0.0,
        }

    def test_CalendarConfig_list_views_when_not_logged_in(self):
        """
        tests if the CalendarConfig list can be accessed without being logged in
        """
        response = self.client.get(reverse('core:calendar.list'))
        self.assertEqual(response.status_code, 404)

    def test_own_CalendarConfig_list_views_for_user(self):
        """
        tests the own CalendarConfig list  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calendar configuration name')
        self.assertContains(response, 'config from tester2')

    def test_CalendarConfig_detail_views_when_not_logged_in(self):
        """
        tests if the CalendarConfigCalendarConfig detail can be accessed without being logged in
        """
        response = self.client.get(reverse('core:calendar.detail', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_CalendarConfig_detail_views_for_user(self):
        """
        tests the own CalendarConfig detail  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.detail', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project list')
        self.assertContains(response, 'config from tester2')

    def test_foreign_CalendarConfig_detail_views_with_user(self):
        """
        tests if a foreign CalendarConfig detail can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.detail', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_CalendarConfig_edit_views_when_not_logged_in(self):
        """
        tests if the CalendarConfig update view can be accessed without being logged in
        """
        response = self.client.get(reverse('core:calendar.update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_CalendarConfig_edit_views_for_user(self):
        """
        tests the own CalendarConfig update view of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.update', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project list')
        self.assertContains(response, 'config from tester2')
        updated_response = self.client.post(reverse('core:calendar.update', args=[2]), self.update2)
        self.assertEqual(updated_response.status_code, 302)
        CalendarConfiguration.objects.get(pk=2).refresh_from_db()
        self.assertEqual(CalendarConfiguration.objects.get(pk=2).config_name, "new config from tester2")

    def test_foreign_CalendarConfig_edit_views_with_user(self):
        """
        tests if a foreign CalendarConfig update view can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.update', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_CalendarConfig_creation_view_when_not_logged_in(self):
        """
        tests if a CalendarConfig can be created when not logged in
        """
        response = self.client.get(reverse('core:calendar.add'))
        self.assertEqual(response.status_code, 302)

    def test_CalendarConfig_creation_view_of_any_user(self):
        """
        tests if every logged in user can create a CalendarConfig
        """
        result = self.client.login(username='tester1', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:calendar.add'), data=self.update1)
        self.assertEqual(response.status_code, 302)
        config1 = CalendarConfiguration.objects.get(pk=4)
        self.assertEqual(config1.user.username, 'tester1')
        self.assertEqual(config1.api_id, 1)
        self.client.logout()

        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:calendar.add'), data=self.update2)
        self.assertEqual(response2.status_code, 302)
        config2 = CalendarConfiguration.objects.get(config_name="new config from tester2")
        self.assertEqual(config2.user.username, 'tester2')
        self.assertEqual(config2.api_id, 2)

    def test_CalendarConfig_deletion_view_when_not_logged_in(self):
        """
        tests if a CalendarConfig can be created when not logged in
        """
        response = self.client.get(reverse('core:calendar.delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_CalendarConfig_deletion_view_of_user(self):
        """
        tests if a logged in user can delete his own CalendarConfig
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:calendar.delete', args=[2]))
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(CalendarConfiguration.objects.filter(pk=2).exists())

    def test_foreign_CalendarConfig_deletion_view_of_user(self):
        """
        tests if a logged in user can delete a foreign CalendarConfig
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:calendar.delete', args=[3]))
        self.assertEqual(response2.status_code, 403)
