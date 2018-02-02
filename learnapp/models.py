from django.db import models

#     class Person(models.Model):
#     location = models.CharField(max_length=100)
#     education = models.IntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(null = true)
#     password = models.CharField(max_length=100)
#     skills = models.ManyToManyField('Skill', blank=True)
#     role = models.IntegerField()
#     bio = models.TextField()
#     rating = models.IntegerField()
#     difficulty = models.IntegerField()
#
#
#
#
# class Skill(models.Model):
#     name = models.CharField(max_length = 100)
#     category = models.ManyToManyField('Category')
#
# class Category(models.Model):
#     name = models.CharField(max_length = 100)
