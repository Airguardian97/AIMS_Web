from django import forms
from django.db import transaction
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth.forms import PasswordResetForm
from course.models import Program
from .models import User, Student, Parent, RELATION_SHIP, LEVEL, GENDERS, Lecturer
from course.importmodels import Student as Student2,Teacher
from django.core.exceptions import ValidationError

class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Username",
        required=False,
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last Name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )
    

    
        
    teacherid = forms.ModelChoiceField(
        queryset=Teacher.objects.exclude(ref__in=Lecturer.objects.values('teacherid')),  # Exclude students already in Student model
        to_field_name='ref',  # This ensures that 'ref' is saved when submitted
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="teacherid",
    )
    

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    email = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Email",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()
            Lecturer.objects.create(
                user=user,
                teacherid=self.cleaned_data.get("teacherid").ref,
            )            
            

        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "form-control", "id": "username_id"}
        ),
        label="Username",
        required=False,
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),required=False,
    )
    
    studid = forms.ModelChoiceField(
        queryset=Student2.objects.exclude(ref__in=Student.objects.values('stud_id')),  # Exclude students already in Student model
        to_field_name='ref',  # This ensures that 'ref' is saved when submitted
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Student ID",
    )
    

    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Program",
        required=False,
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
        required=False,
    )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.gender = self.cleaned_data.get("gender")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")
        

        if commit:
            user.save()
            Student.objects.create(
                student=user,
                # level=self.cleaned_data.get("level"),
                # program=self.cleaned_data.get("program"),
                stud_id=self.cleaned_data.get("studid").ref,
            )

        return user

class LecturerOnlyForm(forms.ModelForm):
    teacherid = forms.ModelChoiceField(
        queryset=Teacher.objects.none(),  # will be set dynamically
        to_field_name='ref',
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="teacherid",
    )

    class Meta:
        model = Lecturer
        fields = ['teacherid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all assigned teacher refs
        assigned_refs = list(Lecturer.objects.values_list('teacherid', flat=True))

        # Get current ref from instance
        current_ref = None
        if self.instance and self.instance.pk and self.instance.teacherid:
            current_ref = str(self.instance.teacherid)  # ensure it's a string to match field type
            # Remove current from exclusion list
            if current_ref in assigned_refs:
                assigned_refs.remove(current_ref)

        # if current_ref and current_ref not in assigned_refs:
        #     assigned_refs.append(current_ref)

       
        # Final queryset: exclude all assigned refs except current
        self.fields['teacherid'].queryset = Teacher.objects.exclude(ref__in=assigned_refs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get("teacherid"):
            print(self.cleaned_data["teacherid"].ref)
            instance.teacherid = str(self.cleaned_data["teacherid"].ref)

        if commit:
            instance.save()
        return instance



class ProfileUpdateForm(UserChangeForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "form-control", "id": "username_id"}
        ),
        label="Username",
        required=False,
    )

    
    
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last Name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Phone No.",
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address / city",
    )
    


    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "gender",
            "email",
            "phone",
            "address",
            "picture",
        ]


class ProgramUpdateForm(UserChangeForm):
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Program",
    )

    class Meta:
        model = Student
        fields = ["program"]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified E-mail address.")
        return email


class ParentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Username",
        required=False,
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    # student = forms.ModelChoiceField(
    #     queryset=Student.objects.all(),
    #     widget=forms.Select(
    #         attrs={"class": "browser-default custom-select form-control"}
    #     ),
    #     label="Student",
    # )

    relation_ship = forms.CharField(
        widget=forms.Select(
            choices=RELATION_SHIP,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label="Relation",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
        
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
        
        required=False,
    )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.email = self.cleaned_data.get("email")
        user.save()
        parent = Parent.objects.create(
            user=user,
            relation_ship=self.cleaned_data.get("relation_ship"),
        )
        parent.save()
        return user



class StudentinfoForm(forms.ModelForm):
    class Meta:
        model = Student2
        exclude = ['studentid', 'rfid']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sex': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if 'form-control' not in visible.field.widget.attrs.get('class', ''):
                visible.field.widget.attrs['class'] = 'form-control'