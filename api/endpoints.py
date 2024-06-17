from rest_framework import routers
from django.urls import include, path

from .yasg import urlpatterns as url_doc
from .auth.endpoints import urlpatterns as auth_urls
from .users.endpoints import urlpatterns as users_urls
from .apiaries.endpoints import urlpatterns as apiaries_urls
from .catalog.endpoints import urlpatterns as catalog_urls
from .equipments.endpoints import urlpatterns as equipments_urls
from .order.endpoints import urlpatterns as order_urls
from .main.endpoints import urlpatterns as main_urls

urlpatterns=[
    path('accounts/', include(auth_urls)),
    path('',include(users_urls)),
    path( '',include(apiaries_urls)),
    path('', include(catalog_urls)),
    path('',include(equipments_urls)),
    path('',include(order_urls)),
    path('',include(main_urls)),
]

urlpatterns+=url_doc