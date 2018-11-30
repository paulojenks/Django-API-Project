from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate


from . import models
from . import serializers
from . import views


class UserAPITest(APITestCase):
    """Test User API functions"""
    def setUp(self):
        self.user = models.User.objects.create(username='testapie', password='testing')
        self.factory = APIRequestFactory()
        self.user_pref = models.UserPref.objects.create(
            user=self.user,
            age= 'b',
            gender= 'f',
            size='l')

    def test_create_user(self):
        """Test creating a user, assert 201 status, increased user count and correct username"""
        new_user = {
            'username': 'Test',
            'password': 'password'
        }
        request = self.factory.post(reverse('pugorugh:register-user'), new_user)
        view = views.UserRegisterView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.User.objects.count(), 2)
        self.assertEqual(models.User.objects.get(pk=2).username, 'Test')

    def test_user_preferences(self):
        """Fetch current user's preferences, make sure serializer and response data are the same"""
        request = self.factory.get(reverse('pugorugh:preferences-user'))

        view = views.UserPrefView.as_view()
        force_authenticate(request, user=self.user)
        serializer = serializers.UserPrefSerializer(self.user_pref)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_user_preferences_update(self):
        """Update user's preferences"""
        new_user_pref = {
            'user': self.user.id,
            'age': 'a',
            'gender': 'f',
            'size': 'm'
        }
        request = self.factory.put(reverse('pugorugh:preferences-user'), new_user_pref)
        force_authenticate(request, user=self.user)

        view = views.UserPrefView.as_view()
        response = view(request)

        serializer = serializers.UserPrefSerializer(models.UserPref.objects.get())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)


class DogAPITest(APITestCase):
    """Test Dog API functions"""
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = models.User.objects.create(username='testapie', password='testing')
        self.dog = models.Dog.objects.create(
            name='Testdog',
            image_filename='2.jpg',
            breed='TestPug',
            age=3,
            gender='f',
            size='m'
        )

        self.userdog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )

        self.user_pref = models.UserPref.objects.create(
            user=self.user,
            age='b',
            gender='f',
            size='m')

    def test_create_dog(self):
        """Add a dog to the database, ensure creation, status of 201 and increased dog count"""
        dog_2 = {
            'name': 'Deuce',
            'image_filename': '2.jpg',
            'breed': 'Unknown',
            'age': 1,
            'gender': 'f',
            'size': 'm'
        }

        request = self.factory.post(reverse('pugorugh:dog-list'), dog_2)
        force_authenticate(request, user=self.user)

        view = views.DogViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Dog.objects.count(), 2)
        self.assertEqual(models.Dog.objects.get(pk=2).name, 'Deuce')

    def test_dog_list(self):
        """Get list of all dogs in database"""
        request = self.factory.get(reverse('pugorugh:dog-list'))
        force_authenticate(request, user=self.user)
        view = views.DogViewSet.as_view()
        response = view(request)
        serializer = serializers.DogSerializer(models.Dog.objects.all(), many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_dog_status_update(self):
        """Update dog status based on status in url"""
        request = self.factory.put(reverse('pugorugh:status', kwargs={'pk': 1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)
        view = views.UserDogStatusUpdateView.as_view()
        response = view(request, pk=1, status='liked')

        user_dog = models.UserDog.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_dog.status, 'l')

    def test_next_dog(self):
        """Get next dog in list with same status"""
        dog_1 = models.Dog.objects.create(
            id=2,
            name='Chunky',
            image_filename='1.jpg',
            breed='Breeds are a construct',
            age=3,
            gender='f',
            size='m'
        )
        userdog = models.UserDog.objects.create(
            user = self.user,
            dog = dog_1,
            status = 'l'
        )
        request = self.factory.get(reverse('pugorugh:nextdog', kwargs={'pk': 1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)

        view = views.NextDogView.as_view()
        response = view(request, pk=1, status='liked')

        serializer = serializers.DogSerializer(dog_1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
