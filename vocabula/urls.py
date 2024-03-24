from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from django_js_reverse import views

urlpatterns = [
    path('jsreverse.json', cache_page(3600)(views.urls_json), name='js_reverse'),
    path('admin/', admin.site.urls),
    path('flashcards/', include('flashcards.urls')),
    path('', TemplateView.as_view(template_name='base.html'))
]
