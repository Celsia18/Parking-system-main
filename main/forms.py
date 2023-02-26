from django.contrib.auth.models import User
from .models import Profile, Preferences, ParkingPlaceType, Parking, Question
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-input form-control',
            'placeholder': 'Пароль',
        }
    ))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "class": "form-input form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль", "class": "form-input form-control"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        self.fields['username'].widget.attrs.update({"placeholder": "Логин", "class": "form-input form-control"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "Имя", "class": "form-input form-control", "required": "required"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Фамилия", "class": "form-input form-control", "required": "required"})
        self.fields['email'].widget.attrs.update({"placeholder": "Email", "class": "form-input form-control", "required": "required"})

        for field in self.fields:
            self.fields[field].label = ''

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        if len(cd["password"]) < 5:
            raise forms.ValidationError("Пароль слишком короткий. Минимум 5 символов")
        return cd["password2"]


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {"placeholder": "Имя", "class": "form-input form-control", "required": "required"}
        )
        self.fields['last_name'].widget.attrs.update(
            {"placeholder": "Фамилия", "class": "form-input form-control", "required": "required"}
        )
        self.fields['email'].widget.attrs.update(
            {"placeholder": "Email", "class": "form-input form-control", "required": "required"}
        )

        for field in self.fields:
            self.fields[field].label = ''


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("car_number", "birthdate")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['car_number'].widget.attrs.update(
            {"placeholder": "Номер машины", "class": "form-input form-control", "required": "required"})
        self.fields['birthdate'].widget.attrs.update(
            {
                "placeholder": "Дата рождения",
                "class": "form-input form-control",
                "required": "required",
                "type": "date"
            }
        )

        for field in self.fields:
            self.fields[field].label = ''


class PreferencesForm(forms.ModelForm):

    class Meta:
        model = Preferences
        fields = ("is_any", "is_open", "location", "is_for_disabled")
        labels = {
            "is_any": "Любое",
            "is_open": "Открытое-крытое",
            "location": "Расположение",
            "is_for_disabled": "Для инвалидов"
        }

    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)

        self.fields['is_any'].widget.attrs.update({"class": "preferences-any"})
        self.fields['is_for_disabled'].widget.attrs.update({"class": "for-disabled"})


class ParkingPlaceTypeForm(forms.ModelForm):

    free = forms.CharField(widget=forms.CheckboxInput(), label="Свободное")
    occupied = forms.CharField(widget=forms.CheckboxInput(), label="Занятое")

    class Meta:
        model = ParkingPlaceType
        fields = ("is_open", "location", "is_for_disabled")
        labels = {
            "is_open": "Открытое-крытое",
            "location": "Расположение",
            "is_for_disabled": "Для инвалидов"
        }


class ParkingForm(forms.ModelForm):

    class Meta:
        model = Parking
        fields = ("address", )

    def __init__(self, *args, **kwargs):
        super(ParkingForm, self).__init__(*args, **kwargs)
        self.fields["address"] = forms.ChoiceField(
            choices=tuple([(parking.pk, parking.address) for parking in Parking.objects.all().order_by("address")])
        )
        self.fields["address"].label = ""
        self.fields["address"].widget.attrs.update({"class": "select-address"})

        for field in self.fields:
            self.fields[field].widget.attrs.update({"required": "false"})


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("text", )

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['text'].widget.attrs.update(
            {"placeholder": "Ваш вопрос", "class": "form-input form-control", "required": "required"})
        self.fields["text"].label = ""
