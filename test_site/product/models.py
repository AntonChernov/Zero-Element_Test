# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Products(models.Model):
    product_name = models.CharField(max_length=700, blank=True)
    product_slug = models.CharField(max_length=700, blank=True)
    product_description = models.TextField(max_length=10000, blank=True)
    product_price = models.FloatField()
    product_created_at = models.DateTimeField(auto_now_add=True)
    product_modified_at = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'product_list'
        verbose_name_plural = 'Продукти'

    def __unicode__(self):
        return self.product_name

    def as_dict(self):
        items = {
            'id': self.id,
            'name': self.product_name,
            'description': self.product_description,
            'price': self.product_price,
            'created_at': self.product_created_at,
            'modified_at': self.product_modified_at,
            'slug': self.product_slug,
        }
        return items


class Consumers(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    CHOICES = (
        (MALE, 'Чоловіча'),
        (FEMALE, 'Жіноча')
    )
    user = models.ForeignKey(User)
    full_name = models.CharField(max_length=700, blank=True)
    banned = models.BooleanField(default=False)
    gender = models.CharField(max_length=100, choices=CHOICES, blank=True)

    class Meta:
        db_table = 'consumers'
        verbose_name_plural = 'Споживачі'

    def __unicode__(self):
        return self.user.username

    def as_dict(self):
        items = {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'full_name': self.full_name,
            'banned': self.banned,
            'gender': self.gender,
        }
        return items


class Comments(models.Model):
    product = models.ForeignKey(Products)
    text = models.TextField(max_length=2000)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'comments'
        verbose_name_plural = 'Коментарі'

    def __unicode__(self):
        return self.product.name

    def as_dict(self):
        items = {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username,
            'product_id': self.product_id,
            'product_name': self.product.name,
            'comment_text': self.text,
        }
        return items


class Like(models.Model):
    product = models.ForeignKey(Products)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products_like'
        verbose_name_plural = 'Продукти які подобаються'

    def __unicode__(self):
        return self.product.name

    def as_dict(self):
        items = {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name,
        }
        return items