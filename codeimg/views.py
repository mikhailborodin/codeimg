from django.views.generic import FormView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles

from .forms import CodeForm


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = "base.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        formatter = HtmlFormatter(style=self.request.session.get("style", None))
        context = super(CodeFormView, self).get_context_data(**kwargs)
        form = self.get_form()
        if default_code := self.request.session.get("default_code", False):
            form.fields['code'].initial = default_code
            context["highlighted_code"] = highlight(default_code, Python3Lexer(), formatter)
        else:
            form.fields['code'].initial = "Type your code here"
        context["form"] = form
        context["style_definitions"] = formatter.get_style_defs()
        context["all_styles"] = list(get_all_styles())
        context["style_bg_color"] = formatter.style.background_color
        return context

    def get_form_kwargs(self):
        kwargs = super(CodeFormView, self).get_form_kwargs()
        if self.request.method == "POST":
            if code := kwargs["data"].get("code"):
                self.request.session["default_code"] = code
            if style := kwargs["data"].get("style"):
                self.request.session["style"] = style
        return kwargs
