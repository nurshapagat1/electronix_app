from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from .views import SubmitReviewView, ListReviewsView, ReviewDetailView, ReviewThanksView

from django.contrib.auth.decorators import login_required
from allauth.socialaccount.views import ConnectionsView
from allauth.socialaccount.views import ConnectionsView

from allauth.account.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    EmailView,
    LoginView,
    SignupView,
    LogoutView,
    ConfirmEmailView,
    EmailVerificationSentView
)

from allauth.socialaccount.views import ConnectionsView
urlpatterns = [

    path("", views.main, name="main-page"),
    path("laptops/", views.laptops, name="laptops-list"),
    path("about-us/", views.about_us, name="about-us"),


    path("product/<int:pk>/", views.product_detail, name="product-detail"),


    path("cart/", views.cart, name="electronics-cart"),
    path("create-order/<int:product_id>/", views.create_order, name="create-order"),
    path("update-cart/<int:product_id>/<str:action>/", views.update_cart, name="update_cart"),
    path(
        "update-cart-in-cart/<int:product_id>/<str:action>/",
        views.update_cart_in_cart,
        name="update_cart_in_cart",
    ),
    path("remove-from-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),


    path("feedback/", SubmitReviewView.as_view(), name="submit_review"),
    path("feedback/thanks/", ReviewThanksView.as_view(), name="review_thanks"),
    path("reviews/", ListReviewsView.as_view(), name="review_list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review_detail"),
    path(
        "reviews/<int:review_id>/like/",
        views.toggle_review_like,
        name="toggle_review_like",
    ),


    path(
        "contact-support/",
        TemplateView.as_view(template_name="electronics/contact_support.html"),
        name="contact_support",
    ),


    path("debug-google/", views.debug_google_url, name="debug_google"),
    path("forgotpass/", views.forgotpass, name="forgotpass"),

    path("accounts/login/", LoginView.as_view(), name="account_login"),
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/logout/", LogoutView.as_view(), name="account_logout"),
    

    path("accounts/email/", EmailView.as_view(), name="account_email"),
    path("accounts/confirm-email/", EmailVerificationSentView.as_view(), name="account_email_verification_sent"),
    path("accounts/confirm-email/<key>/", ConfirmEmailView.as_view(), name="account_confirm_email"),
    

    path("accounts/password/change/", PasswordChangeView.as_view(), name="account_change_password"),
    path("accounts/password/set/", TemplateView.as_view(template_name="account/password_set.html"), name="account_set_password"),
    path("accounts/password/reset/", PasswordResetView.as_view(), name="account_reset_password"),
    path("accounts/password/reset/done/", PasswordResetDoneView.as_view(), name="account_reset_password_done"),
    path("accounts/password/reset/key/<uidb36>/<key>/", PasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    path("accounts/password/reset/key/done/", PasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),
   
path('policy/', TemplateView.as_view(template_name='privacy.html'), name='policy'),
    


path("account/connections/", views.socialaccount_connections, name="socialaccount_connections"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
