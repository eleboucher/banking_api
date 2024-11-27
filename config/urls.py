"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AccountViewSet
from users.views import UserViewSet
from transactions.views import AccountTransactionViewSet

# First, let's create a router. Think of this as a traffic director for your API endpoints.
# It automatically creates all the necessary URL patterns for your ViewSets.
router = DefaultRouter()

router.register("users", UserViewSet, basename="user")
router.register("accounts", AccountViewSet, basename="account")
urlpatterns = [
    path("admin/", admin.site.urls),
    # Include all the routes from your router
    # We put them under 'api/' to keep a clean separation
    path("api/", include(router.urls)),
    path(
        "api/accounts/<uuid:account_id>/transactions/",
        AccountTransactionViewSet.as_view({"get": "list"}),
        name="account-transactions",
    ),
]
