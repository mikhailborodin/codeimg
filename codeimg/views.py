import imgkit
import io
import os
import tempfile
from django.views.generic import FormView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
from django.http import FileResponse

from .forms import CodeForm


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = "base.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        formatter = HtmlFormatter(style=self.request.session.get("style", "default"))
        context = super(CodeFormView, self).get_context_data(**kwargs)
        form = self.get_form()
        if default_code := self.request.session.get("code", False):
            form.fields['code'].initial = default_code
            context["highlighted_code"] = highlight(default_code, Python3Lexer(), formatter)
        else:
            form.fields['code'].initial = "Type your code here"
        context["form"] = form
        context["style_definitions"] = formatter.get_style_defs()
        context["all_styles"] = list(get_all_styles())
        context["style_bg_color"] = formatter.style.background_color
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            code = form.data["code"]
            style = form.data["style"]
            self.request.session["code"] = code
            self.request.session["style"] = style
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def generate_img(style, code):
    formatter = HtmlFormatter(style=style)
    highlighted_code = highlight(code, Python3Lexer(), formatter)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(formatter.get_style_defs())
        temp_file_path = temp_file.name
    html = f"""
    <div class="code" style="background-color: {formatter.style.background_color}">
        {highlighted_code}
    </div>"""
    config = imgkit.config(wkhtmltoimage=os.getenv("PATH_WK_HTML"))
    options = {
        "format": "png",
    }
    return imgkit.from_string(html, False, css=temp_file_path, config=config, options=options)


def download_image(request):
    code = request.session["code"]
    style = request.session["style"]
    jpeg_byte_string = generate_img(style, code)
    response = FileResponse(io.BytesIO(jpeg_byte_string), content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="out.png"'
    return response
