from django.contrib.auth.models import User
from django.db import models, IntegrityError
from . import choices


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=200)
    breed = models.CharField(max_length=255)
    age = models.IntegerField(help_text="Age in months")
    gender = models.CharField(max_length=2, choices=choices.GENDERS)
    size = models.CharField(max_length=2, choices=choices.SIZES)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=choices.STATUS, default='u')

    def __str__(self):
        return "{} is {} by {}".format(self.dog.name, self.status, self.user)

    def save(self, *args, **kwargs):
        if self.pk is None:
            user_dog = UserDog.objects.filter(user=self.user, dog=self.dog)
            if user_dog.count() != 0:
                raise IntegrityError(
                    "Already exists"
                )
        super(UserDog, self).save(*args, **kwargs)


class UserPref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    size = models.CharField(max_length=20)

    def __str__(self):
        return "{} prefers {}, {}, and {} dogs".format(self.user, self.age, self.gender, self.size)
