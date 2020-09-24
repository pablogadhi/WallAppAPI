from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from wall_api.models import User, Post


STARTING_USER = {'username': 'startingUser',
                 'email': 'startingUser@mail.com', 'password': 'secret1234'}


def create_starting_user():
    """
    Creates a user on the db for testing.

        Returns:
            starting_user(User): The created user
    """
    starting_user = User.objects.create(
        username=STARTING_USER['username'], email=STARTING_USER['email'])
    starting_user.set_password(STARTING_USER['password'])
    starting_user.save()
    return starting_user


class UserTests(APITestCase):
    """
    Unit tests for the User related methods
    """

    def setUp(self):
        create_starting_user()

    def test_create_user(self):
        """
        Tries to create a new user with the post method and checks
        if the user was stored on the db.
        """
        user_data = {'username': 'otheruser',
                     'password': 'secret12345', 'email': 'testuser@mail.com'}

        response = self.client.post(reverse('users'), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        saved_user = User.objects.get(
            username=user_data['username'])
        self.assertEqual(user_data['username'], saved_user.username)

    def test_get_token(self):
        """
        Tries to get the authentication token with the STARTING_USER credentials
        """
        user_data = {'username': STARTING_USER['username'],
                     'password': STARTING_USER['password']}
        response = self.client.post(reverse('token'), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        testing_token = Token.objects.get(
            user__username=STARTING_USER['username'])
        self.assertEqual(response.data['token'], testing_token.key)


class PostTests(APITestCase):
    """
    Unit tests for all methods related to the Post model
    """

    def setUp(self):
        user = create_starting_user()
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        Post.objects.create(content='This is the first post.', posted_by=user)
        Post.objects.create(content='This is the second post.', posted_by=user)
        Post.objects.create(content='This is the third post.', posted_by=user)

    def test_list_posts(self):
        """
        Checks if the GET method for the posts returns exactly the same amount
        of previously created posts and that their posted_by fields match with the
        user who created them.
        """
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posted_by_users = [post['posted_by'] for post in response.data]
        self.assertEqual(posted_by_users, [STARTING_USER['username']] * 3)

    def test_create_post(self):
        """
        Tries to create a new post.
        """
        new_post_data = {'content': 'This is the post content!'}
        response = self.client.post(
            reverse('posts'), new_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], new_post_data['content'])
