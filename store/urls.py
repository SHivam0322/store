from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="Order-Status"),
    path("search/",views.search,name="Search"),
    path("product/<int:myid>",views.productView,name="Productinfo"),
    path("checkout/",views.checkout,name="Checkout"),
    path("signup/",views.handleSignup,name="Signup"),
    path("login/",views.handleLogin,name="Login"),
    path("logout/",views.handleLogout,name="Logout")
]
