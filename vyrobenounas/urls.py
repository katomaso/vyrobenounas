# coding: utf-8
import logging

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
# from django.contrib.flatpages import views as flatpage_views
from django.utils.translation import gettext as _
from urljects import view_include, url, U

logger = logging.getLogger("market")

admin.autodiscover()

urlpatterns = [
    url(U, include('market.core.urls')),
    url(U / _('admin/'), include(admin.site.urls)),
]


def app_url(app, regex, view, kwargs=None, name=None):
    """Lazily add url provided its app is among INSTALLED_APPS."""
    if app in settings.INSTALLED_APPS:
        urlpatterns.append(url(regex, view, kwargs, name))
    else:
        logger.warn("Not including app " + app)


# safely add market urls
app_url('market.checkout', U / _('checkout/'), include('market.checkout.urls'))
app_url('market.tariff', '', view_include('market.tariff.views'))
app_url('market.search', U / _('search/'), view_include('market.search.views'))

# safely add the rest of external apps
app_url('bitcategory', U / _('whisper/') / _('category/'), include('bitcategory.urls'), {"model": 'market.Category'})
app_url('allauth', U / _('signup/'), include('allauth.urls'))
app_url('autocomplete_light', U / _('whisper/'), include('autocomplete_light.urls'))
app_url('ratings', U / _('rating/'), include('ratings.urls'))
app_url('stats', U / _('stats/'), include('stats.urls'))
app_url('django_comments', U / _('comment/'), include('django_comments.urls'))

# TODO: add djangoratings-stars
# url(r'^rating/(?P<content_type_id>\d+)/, object_id, field_name, score>',
# djangoratings.views.AddRatingView),

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns.append(
#    # catch-all for flatpages
#    url(r'^(?P<url>.*)$', flatpage_views.flatpage, name='flatpage')
# )
