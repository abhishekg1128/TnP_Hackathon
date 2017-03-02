from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import date

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            # full_name   =   full_name,
            # branch      =   branch,
            email       =   self.normalize_email(email),
            # enr_no      =   enr_no,
            # id_no       =   id_no,
            # cgpa        =   cgpa
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            # enr_no=enr_no,
            # id_no=id_no,
            # cgpa=cgpa,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


BRANCHES = {
    ('CSE',     'Computer Science & Engineering'),
    ('MECH',    'Mechanical Engineering'),
    ('CHEM',    'Chemical Engineering'),
    ('CIV',     'Civil Engineering'),
    ('META',    'Metallurgy'),
    ('MIN',     'Mining'),
    ('ARCH',    'Architecture'),
    ('EEE',    'Electrical and Electronics Engineering'),
    ('ECE',    'Electronics and Communication Engineering'),
}


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    id_no       = models.IntegerField(null=True)
    first_name  = models.CharField(max_length=50, null=True)
    last_name   = models.CharField(max_length=50, null=True)
    # branch      = models.CharField(max_length=50, null=True)
    branch      = models.CharField(max_length=4, choices=BRANCHES)
    enr_no      = models.CharField(max_length=11, null=True)
    cgpa        = models.FloatField(max_length=5, null=True)
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    resume      = models.FileField(null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is    identified by their email address
        return self.first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """"Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """"Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Companies(models.Model):
    BRANCHES = {
        ('CSE', 'Computer Science & Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CHEM', 'Chemical Engineering'),
        ('CIV', 'Civil Engineering'),
        ('META', 'Metallurgy'),
        ('MIN', 'Mining'),
        ('ARCH', 'Architecture'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
    }

    company_name = models.CharField(max_length=250)
    company_type = models.CharField(max_length=100)
    user = models.ManyToManyField(MyUser)
    req_cgpa = models.FloatField(max_length=5, null=True)
    last_date = models.DateField(null=True)
    salary = models.IntegerField(null=True)
    stipend = models.IntegerField(null=True)
    branch = models.CharField(max_length=100, blank=True)

   # slug = models.SlugField()

    def __str__(self):
        return self.company_name

    @property
    def is_past_due(self):
        return date.today() > self.last_date


class Applications(models.Model):
    TITLES = {
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
    }
    GENDER = {
        ('male', 'Male'),
        ('female', 'Female'),
    }

    title = models.CharField(max_length=4, choices=TITLES)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=4, choices=GENDER)
    dob = models.DateField(max_length=10)
    email = models.EmailField(max_length=100)
    mobile = models.IntegerField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.IntegerField()
    company = models.ForeignKey(Companies, null=True, unique=False)
    user = models.ForeignKey(MyUser, null=True, unique=False)

    def __str__(self):
        return self.email
