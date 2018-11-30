from django.contrib.auth import get_user_model

from rest_framework import permissions, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class DogViewSet(ListCreateAPIView):
    """View list of available dogs
        url = api/dog/
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogDetailView(generics.RetrieveAPIView):
    """View individual dog detail
        url= api/dog/<pk>/
    """
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class UserDogStatusUpdateView(APIView):
    """Create or Update UserDog status
        'l' = liked
        'd' = disliked
        'u' = unknown/undecided
        url = api/dog/<pk>/<status>
    """

    @staticmethod
    def put(request, pk, status, format=None):
        """Updates status based on url <status>"""
        current_status = status[0]

        serializer = serializers.UserDogSerializer(data={'user': request.user.id,
                                                         'dog': pk,
                                                         'status': current_status})
        if serializer.is_valid():
            try:
                user_dog = models.UserDog.objects.get(user=request.user.id, dog=pk)
                user_dog.status = current_status
            except models.UserDog.DoesNotExist:
                user_dog = models.UserDog.objects.create(**serializer.validated_data)
            user_dog.save()
        return Response(serializer.data)


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPrefView(RetrieveUpdateAPIView, mixins.CreateModelMixin):
    """Create, View and Change User's preferences"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    lookup_field = None

    def get_object(self):
        """Get current user's preferences"""
        user = self.request.user
        try:
            user_pref = models.UserPref.objects.get(user_id=user.id)
        except models.UserPref.DoesNotExist:
            user_pref = models.UserPref.objects.create(user=user)
        return user_pref


class NextDogView(RetrieveAPIView):
    """Gets next dog of the same status"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """Filter dogs by pk and status"""
        status = self.kwargs['status'][0]
        pk = self.kwargs['pk']
        doggies = self.queryset
        return doggies.filter(id__gt=pk, userdog__status=status).order_by('pk')

    def get_object(self):
        """Gets next dog after current dog"""
        pk = self.kwargs['pk']
        queryset = self.get_queryset().filter(id__gt=int(pk))

        if len(queryset) == 1:
            dog = queryset[0]
        else:
            dog = self.get_queryset().first()
        return dog




