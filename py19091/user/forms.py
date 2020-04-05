from django.forms import ModelForm
from user.models import User, UserInfo


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserInfoModelForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"
