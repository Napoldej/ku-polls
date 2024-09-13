"""Tests of user authentication.

   Put this file in a subdirectory of your ku-polls project,
   for example, a directory named "tests".
   Then run: manage.py test tests

"""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # to "login" a user using code
from polls.models import Question, Choice
from mysite import settings

class UserAuthTest(django.test.TestCase):

    def setUp(self):
        # superclass setUp creates a Client object and initializes test database
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester"
        self.user1.save()
        # we need a poll question to test voting
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_logout(self):
        """A user can logout using the logout url.

        As an authenticated user,
        when I visit /accounts/logout/
        then I am logged out
        and then redirected to the login page.
        """
        logout_url = reverse("logout")
        # Authenticate the user.
        # We want to logout this user, so we need to associate the
        # user user with a session.  Setting client.user = ... doesn't work.
        # Use Client.login(username, password) to do that.
        # Client.login returns true on success
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        # visit the logout page
        form_data = {}
        response = self.client.post(logout_url, form_data)
        self.assertEqual(302, response.status_code)

        # should redirect us to where? Polls index? Login?
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using a POST request
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser",
                     "password": "FatChance!"
                     }
        response = self.client.post(login_url, form_data)
        # after successful login, should redirect browser somewhere
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))


    def test_auth_required_to_vote(self):
            """Authentication is required to submit a vote.

            As an unauthenticated user,
            when I submit a vote for a question,
            then I am redirected to the login page
              or I receive a 403 response (FORBIDDEN)
            """
            vote_url = reverse('polls:vote', args=[self.question.id])

            # what choice to vote for?
            choice = self.question.choice_set.first()
            # the polls detail page has a form, each choice is identified by its id
            form_data = {"choice": f"{choice.id}"}
            response = self.client.post(vote_url, form_data)
            # should be redirected to the login page
            self.assertEqual(302, response.status_code)
            login_with_next = f"{reverse('login')}?next={vote_url}"
            self.assertRedirects(response, login_with_next)

    def test_redirect_polls_page_after_signup(self):
        """
        Test if user is redirected to the polls page after a successful signup.
        """
        register_url = reverse("signup")

        # Load the signup page
        response = self.client.get(register_url)
        self.assertEqual(response.status_code, 200)  # Verify the signup page loads correctly

        # Prepare new user data to avoid conflicts with self.user1
        new_user_data = {
            'username': 'newuser',
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!',
            'email': 'newuser@nowhere.com',
        }

        # Submit the form with valid user data
        response = self.client.post(register_url, new_user_data)

        # Verify that after successful signup, we are redirected to the polls page
        self.assertRedirects(response, reverse('polls:index'))

        # Verify that the new user can now log in
        login_successful = self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        self.assertTrue(login_successful)


    def test_invalid_username(self):
        login_url  = reverse('login')
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {"username": "invalid_username", "password": self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(200, response.status_code)
