from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import Companies, MyUser, Applications
from home.models import RecentNews
from django.contrib.auth import authenticate, login, logout
from .admin import CompanyCreationForm, CompanyChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

def isUserAdmin(MyUser):
    if MyUser.is_authenticated:
        if MyUser.is_admin == True:
            return True
        else:
            return False
    else:
        return False

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def admn_index(request):
    return render(request, 'admn/admn_index.html')

def admn_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                if user.is_admin:
                    login(request, user)
                    return redirect("admn:admnindex")
                else:
                    return render(request, 'admn/admn_login.html',
                                  {'error_message': "Please login with an admin ID."})
            else:
                return render(request, 'admn/admn_login.html',
                              {'error_message': "This account is disabled. Please contact administration."})
        else:
            return render(request, 'admn/admn_login.html',
                          {'error_message': "Invalid Credentials"})
    return render(request, 'admn/admn_login.html')

def admn_logout(request):
    logout(request)
    return redirect('home:home')

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def companies(request):
    # compaies = Companies.objects.values('company_name', 'id', 'applications__user__applications').order_by('-id')

    if 'query' in request.GET:
        companies = Companies.objects.filter(company_name__contains=request.GET['query']).order_by('-id')
    else:
        companies = Companies.objects.all().order_by('-id')
    return render(request, 'admn/company_list.html', {'companies': companies})

Company_Type = [
    'IT',
    'Core',
    'Management',
]

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def add_company(request):
    form = CompanyCreationForm(data=request.POST)

    # msg = "Press 'Save Changes' to make changes."

    if request.method == 'POST':
        if form.is_valid():
            company = form.save()
            company.branch = '; '.join(request.POST.getlist('branch'))
            # return HttpResponse(company.branch)
            company.save()
            # msg = "Changes Saved."
            # return render(request, 'dashboard/edit_prof.html', {'msg': 'Changes Saved'})
            # return redirect('admn:companies')
            return redirect('admn:companies')
        else:
            return HttpResponse('form not valid')

    return render(request, 'admn/new_company.html')


@user_passes_test(isUserAdmin, login_url='/admn/login/')
def edit_company(request, company_id):
    form = CompanyChangeForm(data=request.POST, instance=Companies.objects.get(pk=company_id))

    # msg = "Press 'Save Changes' to make changes."

    if request.method == 'POST':
        if form.is_valid():
            company = form.save()
            company.branch = '; '.join(request.POST.getlist('branch'))
            company.save()
            company.last_date = company.last_date.strftime('%Y-%m-%d')
            msg = "Changes Saved."
            return render(request, 'admn/edit_company.html', {
                'company': company,
                'msg'       : 'Changes Saved'
            })

    company = Companies.objects.get(pk=company_id)
    company.last_date = company.last_date.strftime('%Y-%m-%d')

    return render(request, 'admn/edit_company.html', {'company': company})


@user_passes_test(isUserAdmin, login_url='/admn/login/')
def pending(request):
    if 'query' in request.GET:
        p_user = MyUser.objects.filter(first_name__contains=request.GET['query'], is_admin = False, is_active=False).order_by('-id')
    else:
        p_user = MyUser.objects.filter(is_admin = False, is_active=False).order_by('-id')
    return render(request, 'admn/p_user_list.html', {'p_user': p_user})


@user_passes_test(isUserAdmin, login_url='/admn/login/')
def users(request):

    if 'query' in request.GET:
        user = MyUser.objects.filter(first_name__contains=request.GET['query'], is_admin=False, is_active=True).order_by('-id')
    else:
        user = MyUser.objects.filter(is_admin=False, is_active=True).order_by('-id')
    return render(request, 'admn/user_list.html', {'user': user})

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def accept_user(request, user_id):

    curr_user = MyUser.objects.get(pk = user_id)
    curr_user.is_active = not curr_user.is_active
    curr_user.save()
    # p_user = MyUser.objects.filter(is_admin=False, is_active=False).order_by('-id')
    # user = MyUser.objects.filter(is_admin=False, is_active=True).order_by('-id')

    return redirect('admn:users')
    # return render(request, 'admn/user_list.html', {'user': user, 'p_user': p_user})

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def delete_user(request, user_id):
    curr_user = MyUser.objects.get(pk=user_id)
    curr_user.delete()
    p_user = MyUser.objects.filter(is_admin=False, is_active=False).order_by('-id')
    user = MyUser.objects.filter(is_admin=False, is_active=True).order_by('-id')

    return render(request, 'admn/user_list.html', {'user': user, 'p_user': p_user})

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def view_user(request, user_id):
    if request.method == 'POST':
        user = MyUser.objects.get(pk = user_id)
        user.first_name = request.POST['f_name']
        user.last_name = request.POST['l_name']
        user.branch = request.POST['branch']
        user.id_no = request.POST['id_no']
        user.enr_no = request.POST['enr_no']
        user.cgpa = request.POST['cgpa']
        if user.is_active == True:
            if request.POST['act'] == 'False':
                user.is_active = False
        elif user.is_active == False:
            user.is_active = True
        user.save()

        # p_user = MyUser.objects.filter(is_admin=False, is_active=False).order_by('-id')
        # user = MyUser.objects.filter(is_admin=False, is_active=True).order_by('-id')

        # return render(request, 'admn/user_list.html', {'user': user, 'p_user': p_user})
        return redirect('admn:users')
    curr_user = MyUser.objects.get(pk=user_id, is_admin=False)
    if curr_user is not None:
        return render(request, 'admn/view_user.html', {'curr_user': curr_user})
    else:
        return render(request, 'admn/view_user.html')


@user_passes_test(isUserAdmin, login_url='/admn/login/')
def delete_user2(request, user_id):
    curr_user = MyUser.objects.get(pk=user_id)
    curr_user.delete()
    p_user = MyUser.objects.filter(is_admin=False, is_active=False).order_by('-id')
    user = MyUser.objects.filter(is_admin=False, is_active=True).order_by('-id')

    return render(request, 'admn/user_list.html', {'user': user, 'p_user': p_user})


@user_passes_test(isUserAdmin, login_url='/admn/login/')
def applications(request):

    if 'query' in request.GET:
        application = Applications.objects.filter(company__company_name__contains=request.GET['query'])
    else:
        application = Applications.objects.all()
    return render(request, 'admn/applications_page.html', {'application': application})

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def add_news(request):
    if request.method == 'POST':
        newnews = RecentNews()

        newnews.news = request.POST['news']
        newnews.link = request.POST['link']
        newnews.post_date = request.POST['post_date']

        newnews.save()

        return redirect('admn:admnindex')

    return render(request, 'admn/add_news.html')

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def list_news(request):
    news = RecentNews.objects.all().order_by('-post_date')

    return render(request, 'admn/news_list.html', {'all_news': news})

@user_passes_test(isUserAdmin, login_url='/admn/login/')
def delete_news(request, news_id):
    news = RecentNews.objects.get(pk=news_id)

    news.delete()

    return redirect('admn:news-list')

