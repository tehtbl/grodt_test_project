from allauth.account.forms import ChangePasswordForm
from core.constants import LanguageEnum
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from users.models import MyUser


class MyUserForm(forms.ModelForm):
    class Meta(object):
        model = MyUser
        fields = ["email", "language"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["language"].choices = LanguageEnum.choices()

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "form-label col-3 col-form-label"
        self.helper.field_class = "col"

        self.helper.layout = Layout(
            *self.fields,
            Div(
                Submit("save", "Save Changes"),
                css_class="form-footer",
            )
        )


class MyCustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "form-label col-3 col-form-label"
        self.helper.field_class = "col"

        self.helper.layout = Layout(
            *self.fields,
            Div(
                Submit("save", "Save Changes"),
                css_class="form-footer",
            )
        )
