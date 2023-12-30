from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
     path('fruits/<slug:data>', views.fruits, name='fruits'),
      path('vegitables/<slug:data>', views.vegitables, name='vegitables'),
    path('payment/', views.payment, name='payment'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('contact/', views.contact, name='contact'),
    path('add_product/', views.add_product, name='add_product'),
     path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.allproduct, name='product'),

  #  path('mobiles/', views.mobile, name='mobiles'),
  #   path('mobiles/<slug:data>', views.mobile, name='mobiledata'),
  #  path('FV/<str:data>/', views.FV, name='FV'),
   
     path('', views.home, name='home'),
    # path('', views.home),
    path('products', views.ProductView.as_view(), name="products"),
    # path('product-detail', views.product_detail, name='product-detail'),
    # path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('view', views.product_view, name='product_view'),  # Define URL pattern for product view
    # path('mobile/', views.mobile, name='mobile'),
    # path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    # path('Category/<slug:data>', views.Category, name='Category'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),







    #PRODUCT DETALIS############
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),


    #####CART PATH#############
    path('addcart/<int:product_id>/', views.add_to_cart, name='addcart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)