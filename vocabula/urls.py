from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flashcards/', include('flashcards.urls')),
    path('hello-webpack/', TemplateView.as_view(template_name='hello_webpack.html'))
]
