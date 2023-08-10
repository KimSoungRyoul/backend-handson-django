# Create your views here.
from django.views.generic import TemplateView


class SignUpDemoTemplateView(TemplateView):
    template_name = "frontend_demo/signup.html"

    def get(self, request, *args, **kwargs):
        ctx = {}  # 템플릿에 전달할 데이터
        return self.render_to_response(ctx)
