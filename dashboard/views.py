from django.shortcuts import render, redirect,get_object_or_404
from dashboard.admin import UserChangeForm, UserCreationForm, EditApplication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import MyUser, Companies, Applications
from .admin import EditProfileForm
from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage
import json

@login_required
def dashboard(request):
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
            context = {
                'management_companies': Companies.objects.filter(company_type='Management'),
                'it_companies': Companies.objects.filter(company_type='IT'),
                'core_companies': Companies.objects.filter(company_type='Core'),
                'enr_no'    : request.user.enr_no,
                'id_no'     : request.user.id_no,
                'cgpa'      : request.user.cgpa,
                'branch'    : request.user.branch,
                'first_name' : request.user.first_name,
                'last_name': request.user.last_name,

            }
            return render(request, 'dashboard/index.html', context)
        # else:
            # return HttpResponse('login kar na bhai')
            # return redirect('dashboard:login')
    # else:
    #     return redirect('signup')
RESUME_FILE_TYPES = ['pdf']


def signup(request):
    form = UserCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.resume = request.FILES['resume']
        file_type = form.resume.name.split('.')[-1]
        if file_type not in RESUME_FILE_TYPES:
            context = {
                'form': form,
                'error_message': 'Resume file must be PDF',
                'WP': 'WP',
            }
            return render(request, 'dashboard/signup.html', context)
        fs = FileSystemStorage()
        file = fs.save(form.resume.name, form.resume)

        user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user.set_password(password)
        user.resume = file
        user.is_active = False
        user.is_admin = False
        user.save()
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("dashboard:dashboard")
        else:
            return HttpResponse("Your approval request has been sent and will be processed in next 3 days.")
    # else:
    #     return HttpResponse("Form is not valid.")

    return render(request, 'dashboard/signup.html', {"form": form})


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("dashboard:dashboard")
            else:
                return render(request, 'dashboard/login.html',
                              {'error_message': "This account is disabled. Please contact administration."})
        else:
            return render(request, 'dashboard/login.html',
                          {'error_message': "Invalid Credentials"})
    # else:
    #     return HttpResponse("Form is not valid.")

    return render(request, 'dashboard/login.html', {'WP': 'WP'})

@login_required
def log_out(request):
    logout(request)
    return redirect('home:home')

@login_required
def edit_prof(request):
    form = EditProfileForm(data=request.POST, instance=request.user)

    msg = "Press 'Save Changes' to make changes."

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.save()
            msg = "Changes Saved."
            # return render(request, 'dashboard/edit_prof.html', {'msg': 'Changes Saved'})

    last_name = request.user.last_name
    first_name = request.user.first_name
    enr_no = request.user.enr_no
    id_no = request.user.id_no
    cgpa = request.user.cgpa
    branch = request.user.branch
    email = request.user.email

    # if request.method == "POST":
    #     cgpa = request.POST['cgpa']
    #     MyUser.cgpa = cgpa

    context = {
        'management_companies': Companies.objects.filter(company_type='Management'),
        'it_companies': Companies.objects.filter(company_type='IT'),
        'core_companies': Companies.objects.filter(company_type='Core'),
        'last_name' : last_name,
        'first_name': first_name,
        'enr_no'    : enr_no,
        'id_no'     : id_no,
        'cgpa'      : cgpa,
        'branch'    : branch,
        'email'     : email,
        'msg'       : msg,
        'form'      : form,
    }
    return render(request, 'dashboard/edit_prof.html', context)


@login_required
def change_pw(request):

    context = {
        'management_companies': Companies.objects.filter(company_type='Management'),
        'it_companies': Companies.objects.filter(company_type='IT'),
        'core_companies': Companies.objects.filter(company_type='Core'),
    }

    if request.method == 'POST':

        old_password = request.POST['old_password']
        user = authenticate(email=request.user.email, password=old_password)
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if user is not None:
            if password1 and password2 and password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect('dashboard:dashboard')

        else:
            msg = 'Wrong old password!'
            return render(request, 'dashboard/change_pw.html', {'msg': msg})

    return render(request, 'dashboard/change_pw.html', context)

@login_required
def app_form(request, company_id):
    # if request.method == 'POST':
    #
    #     application = Applications()
    #     application.title = request.POST['title']
    #     application.f_name = request.POST['f_name']
    #     application.m_name = request.POST['m_name']
    #     application.l_name = request.POST['l_name']
    #     application.gender = request.POST['gender']
    #     application.dob = request.POST['dob']
    #     application.email = request.POST['email']
    #     application.mobile = request.POST['mob_no']
    #     application.address = request.POST['address']
    #     application.city = request.POST['city']
    #     application.state = request.POST['state']
    #     application.country = request.POST['country']
    #     application.zip = request.POST['zip']
    #
    #     application.company = Companies.objects.get(pk=company_id)
    #     application.user = request.user
    #     application.save()
    #     return redirect('dashboard:dashboard')

        # msg = 'Please enter the same email address used for registration.'
        #
        # context = {
        #     'management_companies': Companies.objects.filter(company_type='Management'),
        #     'it_companies': Companies.objects.filter(company_type='IT'),
        #     'core_companies': Companies.objects.filter(company_type='Core'),
        #     'msg': msg,
        # }
        # return render(request, 'dashboard/temp.html', context)

    # comp = Companies.objects.get(pk=company_id).pk
    try:
        application = Applications.objects.get(company=company_id, user=request.user.pk)
        context = {
            'management_companies': Companies.objects.filter(company_type='Management'),
            'it_companies': Companies.objects.filter(company_type='IT'),
            'core_companies': Companies.objects.filter(company_type='Core'),
            'title': application.title,
            'f_name': application.f_name,
            'm_name': application.m_name,
            'l_name': application.l_name,
            'gender': application.gender ,
            'dob': application.dob,
            'email': application.email,
            'mob_no': application.mobile,
            'address': application.address,
            'city': application.city,
            'state': application.state,
            'country': application.country,
            'zip': application.zip,
                 }

        if request.method == 'POST':
            application.title = request.POST['title']
            application.f_name = request.POST['f_name']
            application.m_name = request.POST['m_name']
            application.l_name = request.POST['l_name']
            application.gender = request.POST['gender']
            application.dob = request.POST['dob']
            application.email = request.POST['email']
            application.mobile = request.POST['mob_no']
            application.address = request.POST['address']
            application.city = request.POST['city']
            application.state = request.POST['state']
            application.country = request.POST['country']
            application.zip = request.POST['zip']
            application.save()

            return redirect('dashboard:dashboard')

        return render(request, 'dashboard/app_form.html', context)

    except Applications.DoesNotExist:
        context = {
            'management_companies': Companies.objects.filter(company_type='Management'),
            'it_companies': Companies.objects.filter(company_type='IT'),
            'core_companies': Companies.objects.filter(company_type='Core'),
        }

        if request.method == 'POST':
            application = Applications()
            application.title = request.POST['title']
            application.f_name = request.POST['f_name']
            application.m_name = request.POST['m_name']
            application.l_name = request.POST['l_name']
            application.gender = request.POST['gender']
            application.dob = request.POST['dob']
            application.email = request.POST['email']
            application.mobile = request.POST['mob_no']
            application.address = request.POST['address']
            application.city = request.POST['city']
            application.state = request.POST['state']
            application.country = request.POST['country']
            application.zip = request.POST['zip']

            application.company = Companies.objects.get(pk=company_id)
            application.user = request.user
            application.save()
            return redirect('dashboard:dashboard')

        return render(request, 'dashboard/app_form.html', context)
    # if application is not None:
    #     context = {
    #         'management_companies': Companies.objects.filter(company_type='Management'),
    #         'it_companies': Companies.objects.filter(company_type='IT'),
    #         'core_companies': Companies.objects.filter(company_type='Core'),
    #         'f_name': application.f_name,
    #     }


        # return render(request, 'dashboard/app_form.html', context)

    # else:
    #     context = {
    #         'management_companies': Companies.objects.filter(company_type='Management'),
    #         'it_companies': Companies.objects.filter(company_type='IT'),
    #         'core_companies': Companies.objects.filter(company_type='Core'),
    #     }
    #     return render(request, 'dashboard/app_form.html', context)

@login_required
def company_details(request, company_id):

    company = get_object_or_404(Companies, pk=company_id)
    if company is not None:
        data = {}
        data['eligibility'] = company.req_cgpa
        data['salary'] = company.salary
        data['stipend'] = company.stipend
        data['last_date'] = company.last_date
        data['id'] = company.pk

        if request.user.cgpa >= company.req_cgpa and request.user.branch in company.branch:
            data['can_apply'] = 'true'
        else:
            data['can_apply'] = 'false'

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")
        # render_template_to_response("index.html", data)



  #  companyname = get_object_or_404(Companies, company_name=company_name)
  #   company = get_object_or_404(Companies, pk=company_id)
  #   company = Companies.objects.create(company_name=company_name, slug=slugify(company_name))

    # context = {
        # 'management_companies': Companies.objects.filter(company_type='Management'),
        # 'it_companies': Companies.objects.filter(company_type='IT'),
        # 'core_companies': Companies.objects.filter(company_type='Core'),
        #'companyName': companyname,
        # 'company': company,
    # }
    # return render(request, 'dashboard/company_details.html', context)

@login_required
def apply(request):

    if request.method == 'POST':
      #  form = ApplicationForm(request.POST or None)

        application = Applications()
        application.title = request.POST['title']
        application.f_name = request.POST['f_name']
        application.m_name = request.POST['m_name']
        application.l_name = request.POST['l_name']
        application.gender = request.POST['gender']
        application.dob = request.POST['dob']
        application.email = request.POST['email']
        application.mobile = request.POST['mob_no']
        application.address = request.POST['address']
        application.city = request.POST['city']
        application.state = request.POST['state']
        application.country = request.POST['country']
        application.zip = request.POST['zip']

        #application.company = Companies.objects.get(company_name='Google')
        application.user = request.user
        application.save()
        return redirect('dashboard:dashboard')

        # context = {
        #     'management_companies': Companies.objects.filter(company_type='Management'),
        #     'it_companies': Companies.objects.filter(company_type='IT'),
        #     'core_companies': Companies.objects.filter(company_type='Core'),
        #     'msg': msg,
        # }
        # return render(request, 'dashboard/temp.html', context)
    else:
        return render(request, 'dashboard/temp.html')


def current_app (request):
    apps = Applications.objects.filter(user = request.user)
    context = {'apps' : apps , 'SP': 'SP'}
    return render(request, 'dashboard/current_app.html', context )


def view_appl(request, app_id):
    application = Applications.objects.get(pk=app_id)
    context = {
        'management_companies': Companies.objects.filter(company_type='Management'),
        'it_companies': Companies.objects.filter(company_type='IT'),
        'core_companies': Companies.objects.filter(company_type='Core'),
        'title': application.title,
        'f_name': application.f_name,
        'm_name': application.m_name,
        'l_name': application.l_name,
        'gender': application.gender,
        'dob': application.dob,
        'email': application.email,
        'mob_no': application.mobile,
        'address': application.address,
        'city': application.city,
        'state': application.state,
        'country': application.country,
        'zip': application.zip,
    }
    return render(request, 'dashboard/app.html', context)


def edit_appl(request, app_id):
    application = Applications.objects.get(pk=app_id)
    form = EditApplication(data=request.POST, instance=application)

    msg = "Press 'Save Changes' to make changes."

    if request.method == 'POST':
        if form.is_valid():
            application = form.save()
            application.save()
            msg = "Changes Saved."
            # return render(request, 'dashboard/edit_prof.html', {'msg': 'Changes Saved'})

    title = application.title
    f_name = application.f_name
    m_name = application.m_name

    # if request.method == "POST":
    #     cgpa = request.POST['cgpa']
    #     MyUser.cgpa = cgpa

    context = {
        'management_companies': Companies.objects.filter(company_type='Management'),
        'it_companies': Companies.objects.filter(company_type='IT'),
        'core_companies': Companies.objects.filter(company_type='Core'),
        'title': application.title,
        'f_name': application.f_name,
        'm_name': application.m_name,
        'l_name': application.l_name,
        'gender': application.gender,
        'dob': application.dob,
        'email': application.email,
        'mob_no': application.mobile,
        'address': application.address,
        'city': application.city,
        'state': application.state,
        'country': application.country,
        'zip': application.zip,
    }
    return render(request, 'dashboard/edit_appl.html', context)
