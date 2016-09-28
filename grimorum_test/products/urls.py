from django.conf.urls import url, patterns
from .views import ProductListView,GetCheckout


urlpatterns = [
    url(r'^home/', ProductListView.as_view(), name="home"),
    url(r'^checkout/', GetCheckout.as_view(), name="Checkout"),
]
