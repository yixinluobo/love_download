from django.forms import ModelForm

from .models import ResourceInfo

class ResourceModelForm(ModelForm):

    class Meta:

        model = ResourceInfo

        fields = "__all__"