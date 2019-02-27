"""BudgetManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from . import view
from . import db_tools
from . import settings
from . import functions

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello$', view.hello),
    #url(r"^$", view.budget),
    url(r"^$", view.login),
    url(r"^user-api/records_json/bills$", view.retBills_json),
    url(r"^user-api/records_json/bills/details$", view.retBillDetails),
    url(r"^user-api/records_json/bills/add$", view.addBill),
    url(r"^user-api/records_json/bills/update$", view.editBill),
    url(r"^user-api/records_json/bills/delete$", view.deleteBill),
    url(r"^user-api/records_json/daily_spendings$", view.retSpendings_json),
    url(r"^user-api/records_json/daily_spendings/recompute$", view.reComputeDailySpendings),
    url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    url(r"^user-api/registration/details$", view.registrationDetails),
    url(r"^user-api/registration/register$", view.registration),
    url(r"^user-api/validation$", view.validate),
    url(r"^user-api/user-report$", view.budget),
    url(r"^user-api/logout$", view.logout),
    url(r"^user-api/mobile-end/user-report$", view.mobileEndReport),
    url(r"^user-api/mobile-end/validation$", view.mobileEndValidate),
    url(r"^user-api/mobile-end/logout$", view.mobileEndLogout),
]

