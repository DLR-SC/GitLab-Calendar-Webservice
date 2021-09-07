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


class GitLabAPIViewTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester1', password='123')
        User.objects.create_user('tester2', password='123')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='api from tester1',
            url='https://example.org/',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
                user=User.objects.get(username='tester2'),
                api_name='api from tester2',
                url='https://example.org/',
                gitlab_api_token='mytesttoken'
        )
        self.update1 = {
            "api_name": "api from tester1",
            "url": "https://example.org/",
            "gitlab_api_token": "mynewsupertesttoken"
        }
        self.update2 = {
            "api_name": "api from tester2",
            "url": "https://example.org/",
            "gitlab_api_token": "mynewtesttoken"
        }

    def test_gitlabapiviews_not_logged_in(self):
        """
        tests if the GitLabAPI views can be accessed without being logged in
        """
        response = self.client.get(reverse('core:gitlabapi.list'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('core:gitlabapi.detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:gitlabapi.update', args=[1]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:gitlabapi.add'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:gitlabapi.delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_gitlabapi_list_views(self):
        """
        tests the own GitLabAPI list of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Actions')
        self.assertContains(response, 'api from tester2')

    def test_own_gitlabapi_detail_views(self):
        """
        tests the own GitLabAPI detail of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.detail', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'URL')
        self.assertContains(response, 'api from tester2')

    def test_foreign_gitlabapi_detail_views(self):
        """
        tests if a foreign GitLabAPI detail can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_own_gitlabapi_edit_views(self):
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

    def test_foreign_gitlabapi_edit_views(self):
        """
        tests if a foreign GitLabAPI update view can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:gitlabapi.update', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_gitlabapi_creation_view(self):
        """
        tests if every logged in user can create a GitLabAPI
        """
        result = self.client.login(username='tester1', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:gitlabapi.add'), self.update1)
        self.assertEqual(response.status_code, 302)
        api1 = GitLabAPI.objects.get(pk=3)
        self.assertEqual(api1.user.username, 'tester1')
        self.assertEqual(api1.gitlab_api_token, 'mynewsupertesttoken')

    def test_own_gitlabapi_deletion_view(self):
        """
        tests if a logged in user can delete his own GitLabAPI
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response2 = self.client.post(reverse('core:gitlabapi.delete', args=[2]))
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(GitLabAPI.objects.filter(pk=2).exists())

    def test_foreign_gitlabapi_deletion_view(self):
        """
        tests if a logged in user can delete a foreign GitLabAPI
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response2 = self.client.post(reverse('core:gitlabapi.delete', args=[1]))
        self.assertEqual(response2.status_code, 403)


class CalendarConfigurationViewTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester1', password='123')
        User.objects.create_user('tester2', password='123')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='api from tester1',
            url='https://example.org/',
            gitlab_api_token='mytesttoken'
        )
        GitLabAPI.objects.create(
                user=User.objects.get(username='tester2'),
                api_name='api from tester2',
                url='https://example.org/',
                gitlab_api_token='mytesttoken'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester1'),
            api_id=1,
            config_name='config from tester1',
            projects='28236929,abcd'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester2'),
            api_id=2,
            config_name='config from tester2',
            projects='28236929,abc'
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

    def test_calendarconfig_views_not_logged_in(self):
        """
        tests if the CalendarConfig list can be accessed without being logged in
        """
        response = self.client.get(reverse('core:calendar.list'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('core:calendar.detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:calendar.update', args=[1]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:calendar.add'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('core:calendar.delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_own_calendarconfig_list_views(self):
        """
        tests the own CalendarConfig list  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calendar configuration name')
        self.assertContains(response, 'config from tester2')

    def test_own_calendarconfig_detail_views(self):
        """
        tests the own CalendarConfig detail  of a user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.detail', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project list')
        self.assertContains(response, 'config from tester2')

    def test_foreign_calendarconfig_detail_views(self):
        """
        tests if a foreign CalendarConfig detail can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_own_calendarconfig_edit_views(self):
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

    def test_foreign_calendarconfig_edit_views(self):
        """
        tests if a foreign CalendarConfig update view can be accessed by another normal user
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)
        response = self.client.get(reverse('core:calendar.update', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_calendarconfig_creation_views(self):
        """
        tests if every logged in user can create a CalendarConfig
        """
        result = self.client.login(username='tester1', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:calendar.add'), data=self.update1)
        self.assertEqual(response.status_code, 302)
        config1 = CalendarConfiguration.objects.get(pk=3)
        self.assertEqual(config1.user.username, 'tester1')
        self.assertEqual(config1.api_id, 1)

    def test_own_calendarconfig_deletion_views(self):
        """
        tests if a logged in user can delete his own CalendarConfig
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:calendar.delete', args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CalendarConfiguration.objects.filter(pk=2).exists())

    def test_foreign_CalendarConfig_deletion_views(self):
        """
        tests if a logged in user can delete a foreign CalendarConfig
        """
        result = self.client.login(username='tester2', password='123')
        self.assertTrue(result)

        response = self.client.post(reverse('core:calendar.delete', args=[1]))
        self.assertEqual(response.status_code, 403)


class ICSFileCreationViews(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('tester1', password='123')
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='not valid api from tester1',
            url='https://example.org/',
            gitlab_api_token='mytesttoken'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester1'),
            api_id=1,
            config_name='config from tester1',
            projects='28236929,abcd'
        )
        GitLabAPI.objects.create(
            user=User.objects.get(username='tester1'),
            api_name='valid api from tester1',
            url='https://gitlab.com/',
            gitlab_api_token='DhvrWaxnZ3S3bV1C7_sa'
        )
        CalendarConfiguration.objects.create(
            user=User.objects.get(username='tester1'),
            api_id=2,
            config_name='valid_config_from_tester1',
            projects='28236929'
        )

    def test_not_valid_config_not_logged_in(self):
        config = CalendarConfiguration.objects.get(pk=1)
        response = self.client.get(reverse('core:ics.generate', args=[config.write_token]))
        self.assertEqual(response.status_code, 400)

    def test_not_valid_config_logged_in(self):
        result = self.client.login(username='tester1', password='123')
        self.assertTrue(result)
        config = CalendarConfiguration.objects.get(pk=1)
        response = self.client.get(reverse('core:ics.generate', args=[config.write_token]))
        self.assertEqual(response.status_code, 400)

    def test_valid_config_not_logged_in(self):
        config = CalendarConfiguration.objects.get(pk=2)
        response = self.client.get(reverse('core:ics.generate', args=[config.write_token]))
        self.assertURLEqual(reverse('core:ics.generate', args=[config.write_token]), (f'/ics/generate/{str(config.write_token)}/'))
        self.assertEqual(response.status_code, 302)

    def test_get_ics_file_not_logged_in(self):
        config = CalendarConfiguration.objects.get(pk=2)
        self.assertURLEqual(reverse('core:ics.show', args=[config.read_token, config.config_name + '.ics']), (f'/ics/show/{str(config.read_token)}/{str(config.config_name)}.ics'))
