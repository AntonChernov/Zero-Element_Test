from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

@csrf_exempt
def test_username_and_create_new_user(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            User.objects.get(username=kwargs.get('username'))
            return JsonResponse(data={'error': True, 'msg': 'Користувач з таким ім’ям вже існує!'},
                                safe=False,
                                content_type='application/json', status=200)
        except ObjectDoesNotExist:
            return JsonResponse(data={'error': False, 'msg': 'Username доступний для регістрації!'}, safe=False, content_type='application/json', status=200)

    elif request.method == 'POST':
        user = User.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        Consumers.objects.create(
            user=user,
            full_name=request.POST.get('fullname'),
        )
        return redirect('/products/all/')
        # return JsonResponse(data={'error': False}, safe=False, content_type='application/json', status=200)
    else:
        return JsonResponse(data={'error': True, 'msg': 'Невідомий тип запиту!'},
                            safe=False,
                            content_type='application/json', status=404)


class ViewListOfProducts(ListView):

    def get(self, request, *args, **kwargs):
        queryset = Products.objects.all()
        args = {}
        items_queryset = [i.as_dict() for i in queryset]
        args['items'] = items_queryset
        paginator = Paginator(queryset, 25)
        page = request.GET.get('page')
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products_page = paginator.page(paginator.num_pages)
        args['products_page'] = products_page
        template = render_to_string('products.html', {'data': args})
        # print(template)
        # return JsonResponse(data=template, safe=False, content_type='application/json', status=200)
        return HttpResponse(template)


class ViewProductItem(DetailView):

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            consumers = Consumers.objects.get(user_id=user.id)
        except ObjectDoesNotExist:
            consumers = None
        try:
            product = Products.objects.get(id=kwargs.get('id'))
            item = {
                'product': product.as_dict(),
                'error': False,
            }
            if consumers and consumers.banned:
                item['banned'] = True
            item[user] = user
            like = Like.objects.filter(product_id=product.id).count()
            item['likes'] = like
            comments = [i.as_dict() for i in Comments.objects.filter(product_id=product.id)]
            item['comments'] = comments
            # return JsonResponse(data=template, safe=False, content_type='application/json', status=200)
            template = render_to_string('product.html', {'data': item})
            return HttpResponse(template)
        except ObjectDoesNotExist:
            return JsonResponse(data={'error': True, 'msg': 'Користувач з таким ім’ям вже існує!'},
                                safe=False,
                                content_type='application/json', status=404)


def login_logout(request):

    if request.method == 'GET':
        logout(request)
        return JsonResponse(data={'error': False, 'msg': 'Користувач вийшов з системи.'},
                            safe=False,
                            content_type='application/json', status=200)

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(data={'error': False, 'msg': 'Користувач зайшов в системму.'},
                                safe=False,
                                content_type='application/json', status=200)
        else:
            return JsonResponse(data={'error': True, 'msg': 'Невірний пароль або ім’я користувача!!'},
                                safe=False,
                                content_type='application/json', status=404)
    else:
        return JsonResponse(data={'error': True, 'msg': 'Невідомий тип запиту!'},
                            safe=False,
                            content_type='application/json', status=404)


class AddLike(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            consumers = Consumers.objects.filter(id=user.id)
            if consumers and not consumers.banned:
                Like.objects.create(
                    product=kwargs.get('product_id')
                )
                return JsonResponse(data={'error': False, 'msg': 'Додана оцінка товару.'},
                                    safe=False,
                                    content_type='application/json', status=200)
            else:
                return JsonResponse(data={'error': False, 'msg': 'Користувача забанено!'},
                                    safe=False,
                                    content_type='application/json', status=200)
        else:
            return JsonResponse(data={'error': True, 'msg': 'Користувач не війшов в системму!'},
                                safe=False,
                                content_type='application/json', status=404)


def add_comment(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            consumers = Consumers.objects.filter(id=user.id)
            if consumers and not consumers.banned:
                Comments.objects.create(
                    product=request.POST.get('product_id'),
                    text=request.POST.get('comment_text'),
                    user=user,
                )
            else:
                return JsonResponse(data={'error': False, 'msg': 'Додана оцінка товару.'},
                                    safe=False,
                                    content_type='application/json', status=200)
        else:
            return JsonResponse(data={'error': True, 'msg': 'Користувач не війшов в системму!'},
                                safe=False,
                                content_type='application/json', status=404)
    else:
        return JsonResponse(data={'error': True, 'msg': 'Невірний тип запита!'},
                            safe=False,
                            content_type='application/json', status=404)


def filter_most_liked_product(request):
    date = datetime.datetime.now() - datetime.timedelta(day=1)
    if request.method == 'GET':
        products = Products.objects.filter(like__date__gte=date).order_by('-')
        pass #Entry.objects.dates('pub_date', 'day')>>>[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]


def register(request):
    args = {'gender': [{'gender': Consumers.CHOICES[0][1]}, {'gender': Consumers.CHOICES[1][1]}]}
    return render(request, 'registration.html', args)
