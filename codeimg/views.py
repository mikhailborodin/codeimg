from django.views.generic import FormView
from .forms import CodeForm


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = "base.html"
    success_url = "/"
