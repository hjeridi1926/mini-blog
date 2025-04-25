# -*- coding: utf-8 -*-
import os
import django
from faker import Faker as fa
from random import randrange
#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniBlog.settings")
django.setup()


from blog.models import Post,User,userDetail

def run():
    # do the work
    Faker=fa()
    users=[]
    for i in range(0,100):
        user=User(username=Faker.name(),password=Faker.ean(length=8))
        user.save()
        userDetail(user=user,hobby=Faker.job()).save()
        print("adding user")
        users.append(user)
        

    for i in range(0,300):
        rand=randrange(0,len(users))
        user=users[rand]
        print("adding post")
        p = Post(user=user,text=Faker.paragraph(nb_sentences=30),title=Faker.sentence(nb_words=10)).save()


if __name__ == '__main__':
    run()