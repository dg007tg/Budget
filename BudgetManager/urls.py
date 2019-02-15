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
    url(r"^$", view.budget),
    url(r"^records_json/bills$", view.retBills_json),
    url(r"^records_json/bills/details$", view.retBillDetails),
    url(r"^records_json/bills/add$", view.addBill),
    url(r"^records_json/bills/update$", view.editBill),
    url(r"^records_json/bills/delete$", view.deleteBill),
    url(r"^records_json/daily_spendings$", view.retSpendings_json),
    url(r"^records_json/daily_spendings/recompute$", view.reComputeDailySpendings),
    url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
]

