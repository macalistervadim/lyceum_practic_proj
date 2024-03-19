import django.contrib.auth.forms
import django.contrib.auth.models

class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            
    class Meta:
        model = django.contrib.auth.models.User
        fields = (
            'username',
            'email',
            'password1',
            'password2', 
        )