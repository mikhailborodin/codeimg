from django.views.generic import FormView
from .forms import CodeForm


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = "base.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(CodeFormView, self).get_context_data(**kwargs)
        form = self.get_form()
        if default_code := self.request.session.get("code", False):
            form.fields['code'].initial = default_code
        else:
            form.fields['code'].initial = "Type your code here"
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            code = form.data["code"]
            self.request.session["code"] = code
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
