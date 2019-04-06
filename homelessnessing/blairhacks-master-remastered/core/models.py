import hashlib
from django import forms
from django.db import models
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList

GRADES = [
    (9, 'Freshman'),
    (10, 'Sophomore'),
    (11, 'Junior'),
    (12, 'Senior')
]


class InfoSection(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    rank = models.IntegerField()

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.title


class ShirtSize(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class BreakfastChoice(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class LunchChoice(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class DinnerChoice(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class DietaryRestriction(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=16, unique=True, null=True)

    def generate_code(self):
        hasher = hashlib.sha256()
        hasher.update(self.name.encode('ascii'))
        hasher.update('&vvjl4u*c*^o1h=e=__r7u6=3to5l9dwzqd94m1po+rd)gr@e!'.encode('ascii'))

        return hasher.hexdigest()[:16]

    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class HackerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    school = models.CharField(max_length=64)
    grade = models.IntegerField(choices=GRADES)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    t_shirt_size = models.ForeignKey(ShirtSize, on_delete=models.SET_NULL, null=True)
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)
    allergies = models.CharField(max_length=128, null=True, blank=True)

    checked_in = models.BooleanField(default=False)
    breakfast = models.ForeignKey(BreakfastChoice, on_delete=models.SET_NULL, null=True, blank=True)
    lunch = models.ForeignKey(LunchChoice, on_delete=models.SET_NULL, null=True, blank=True)
    dinner = models.ForeignKey(DinnerChoice, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField(max_length=254, label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = ""
        super(UserForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(UserForm, self).is_valid()
        if not valid:
            return False

        if User.objects.filter(email=self.cleaned_data['email']).count() > 0:
            errors = self._errors.setdefault('email', ErrorList())
            errors.append('User with that email already exists.')
            return False

        return True


class HackerForm(forms.ModelForm):
    class Meta:
        model = HackerProfile
        fields = ['school', 'grade', 't_shirt_size', 'dietary_restrictions', 'allergies']
        widgets = {
            'dietary_restrictions': forms.CheckboxSelectMultiple
        }
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = ""
        super(HackerForm, self).__init__(*args, **kwargs)


class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = ""
        super(TeamCreationForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(TeamCreationForm, self).is_valid()
        if not valid:
            return False

        if Team.objects.filter(name=self.cleaned_data['name']).count() > 0:
            errors = self._errors.setdefault('name', ErrorList())
            errors.append('Team with that name already exists.')
            return False

        return True


class HardwareItem(models.Model):
    name = models.CharField(max_length=64)
    hacker = models.ForeignKey(HackerProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class TeamJoiningForm(forms.Form):
    code = forms.CharField(max_length=16)

    code.widget.attrs['placeholder'] = 'Team Code'

    def is_valid(self):
        valid = super(TeamJoiningForm, self).is_valid()
        if not valid:
            return False

        if Team.objects.filter(code=self.cleaned_data['code']).count() == 0:
            errors = self._errors.setdefault('code', ErrorList())
            errors.append('No team with that code exists.')
            return False

        if HackerProfile.objects.filter(team__code=self.cleaned_data['code']).count() >= 4:
            errors = self._errors.setdefault('code', ErrorList())
            errors.append('That team is full.')
            return False

        return True


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    username.widget.attrs['placeholder'] = ''
    password.widget.attrs['placeholder'] = ''


class TeamAdmin(ModelAdmin):
    list_display = ['name', 'member_count']

    def member_count(self, obj):
        return HackerProfile.objects.filter(team=obj).count()

    member_count.short_description = 'Member Count'


class ShirtSizeAdmin(ModelAdmin):
    list_display = ['name', 'number_needed']

    def number_needed(self, obj):
        return HackerProfile.objects.filter(t_shirt_size=obj).count()

    number_needed.short_description = 'Number Needed'


class DietaryRestrictionAdmin(ModelAdmin):
    list_display = ['name', 'number_needed']

    def number_needed(self, obj):
        return HackerProfile.objects.filter(dietary_restrictions=obj).count()

    number_needed.short_description = 'Number Needed'


class DinnerChoiceAdmin(ModelAdmin):
    list_display = ['name', 'number_needed']

    def number_needed(self, obj):
        return HackerProfile.objects.filter(dinner=obj).count()

    number_needed.short_description = 'Number Needed'


class LunchChoiceAdmin(ModelAdmin):
    list_display = ['name', 'number_needed']

    def number_needed(self, obj):
        return HackerProfile.objects.filter(lunch=obj).count()

    number_needed.short_description = 'Number Needed'

class BreakfastChoiceAdmin(ModelAdmin):
    list_display = ['name', 'number_needed']

    def number_needed(self, obj):
        return HackerProfile.objects.filter(breakfast=obj).count()

    number_needed.short_description = 'Number Needed'

def check_in(modeladmin, request, queryset):
    queryset.update(checked_in=True)


check_in.short_description = 'Check Hackers In'


class HackerAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'school', 'grade', 't_shirt_size', 'team', 'checked_in', 'breakfast', 'lunch',
                    'dinner', 'allergies']
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple}
    }

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    actions = [check_in]

    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'


def check_back_in(modeladmin, request, queryset):
    queryset.update(hacker=None)


class HardwareAdmin(ModelAdmin):
    list_display = ['name', 'hacker']
    actions = [check_back_in]

class BreakfastForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=BreakfastChoice.objects.all())

class LunchForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=LunchChoice.objects.all())


class DinnerForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=DinnerChoice.objects.all())
