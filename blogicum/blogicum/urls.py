from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView
from blog.forms import UserForm
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_failure'

urlpatterns = [
                  path('', include('blog.urls'), name='blog'),
                  path('pages/', include('pages.urls')),
                  path('admin/', admin.site.urls),
                  path(
                      'auth/registration/',
                      CreateView.as_view(
                          template_name='registration/registration_form.html',
                          form_class=UserForm,
                          success_url=reverse_lazy('blog:index')
                      ),
                      name='registration'
                  ),
                  path('auth/', include('django.contrib.auth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
