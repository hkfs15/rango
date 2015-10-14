from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime

# Create your views here.


def default(request):
    # context_dict = {'boldmsg': 'I am bold font form context.'}
    category_list = Category.objects.all().order_by('-views')[:5]
    page_top_five = Page.objects.all().order_by('-views')[:5]
    context_dict = {
        'category_list': category_list,
        'page_top_five': page_top_five,
        }

    response = render(request, 'default.html', context_dict)

    # visits = int(request.COOKIES.get('visits', 1))
    # reset_last_visit_time = False

    # if 'last_visit' in request.COOKIES:
    #     last_visit = request.COOKIES['last_visit']
    #     if (datetime.now()-datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')).seconds > 5:
    #         visits += 1
    #         reset_last_visit_time = True
    # else:
    #     reset_last_visit_time = True

    # if reset_last_visit_time:
    #     response.set_cookie('visits', visits)
    #     response.set_cookie('last_visit', datetime.now())

    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        if (datetime.now()-datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['visits'] = visits
        request.session['last_visit'] = str(datetime.now())

    context_dict['visits'] = visits    

    return response


def about(request):
    return render(request, 'about.html', {})


def category_detail(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        pages = Page.objects.filter(category__slug=category_slug)

        context_dict = {
            'category_name': category.name,
            'category': category,
            'pages': pages,
        }

        return render(request, 'category_detail.html', context_dict)
    except Category.DoesNotExist:
        pass

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return default(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form})

@login_required
def add_page(request, category_slug):
    try:
        cat = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = cat
            page.save()
            return category_detail(request, category_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {
        'form': form,
        'category_slug': category_slug,
    }

    return render(request, 'page_form.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        userform = UserForm(request.POST)
        userprofileform = UserProfileForm(request.POST)

        if userform.is_valid() and userprofileform.is_valid():
            user = userform.save()

            user.set_password(user.password)
            user.save()

            profile = userprofileform.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(userform.errors)
            print(userprofileform.errors)

    else:
        userform = UserForm()
        userprofileform = UserProfileForm()

    context_dict = {
        'registered': registered,
        'userform': userform,
        'userprofileform': userprofileform,
    }

    return render(request, 'register.html', context_dict)


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("This account has been disabled.")
        else:
            return HttpResponse("Invalid username or password, try again.")
    else:
        return render(request, 'login.html', {})


@login_required
def restricted(request):
    return HttpResponse('You can view this as you are logged in.')


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')





