from django.urls import path
from .views import artisan_signup, customer_signup, add_product, homepage, artisan_login, customer_login, logout_view, \
    shop, registration_page, add_to_cart, \
    contact_us, product_list, cart, update_cart, checkout, order_list, admin_dashboard, update_order_status, \
    remove_from_cart, cancel_order, edit_product, delete_product
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name='home'),
    path('signup/artisan/', artisan_signup, name='artisan_signup'),
    path('signup/customer/', customer_signup, name='customer_signup'),
    path('signup/', registration_page, name='registration_page'),
    path('login/artisan/', artisan_login, name='artisan_login'),
    path('login/customer/', customer_login, name='customer_login'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('logout/', logout_view, name='logout'),
    path('shop/', shop, name='shop'),
    path('products/', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart, name='cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='order_list'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('contact-us/', contact_us, name='contact_us'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
