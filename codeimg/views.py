from django.views.generic import FormView
from .forms import CodeForm


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = "base.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(CodeFormView, self).get_context_data(**kwargs)
        form = self.get_form()
        if default_code := self.request.session.get("default_code", False):
            form.fields['code'].initial = default_code
        else:
            form.fields['code'].initial = "Type your code here"
        context["form"] = form
        return context

    def get_form_kwargs(self):
        kwargs = super(CodeFormView, self).get_form_kwargs()
        if self.request.method == "POST":
            if code := kwargs["data"].get("code"):
                self.request.session["default_code"] = code
        return kwargs
