from dashing.utils import router
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from statusite.repository.views import repo_list

# Load django-dashing dashboard widgets into the router
from statusite.dashboard.urls import *

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('statusite.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # API
    url(r'^api/', include('statusite.api.urls', namespace='api')),

    # repository app
    url(r'^$', repo_list, name='home'),
    url(r'^repo/', include('statusite.repository.urls', namespace='repository')),

    # django-rq
    url(r'^django-rq/', include('django_rq.urls')),

    # Dashboards
    url(r'^dashboard/', include(router.urls)),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
