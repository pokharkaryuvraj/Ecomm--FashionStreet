from django.contrib import admin
from django.urls import path
from firstapp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   # path('admin/', admin.site.urls),
    path('home',views.home_fn),
    path('studinfo',views.Wear_Details),
    path('dash',views.dashboard),
    path('delwe/<rid>',views.delWear),
    path('index',views.index_pg),
    path('make',views.set_default_value),
    path('done',views.Migration),
    path('index',views.index_pg),
    path('regis',views.register),
    path('login',views.userlogin),
    path('logout',views.user_logout),
    path('filterbycategory/<caname>',views.filterByCategory),
    path('sort/<ord>',views.sortStudents),
    path('range',views.rangeSearch),
    path('details/<sid>',views.showDetails),
    path('addtocart/<sid>',views.addToCart),
    path('viewcart',views.viewcart),
    path('delete/<cid>',views.deleteFromCart),
    path('updateqty/<incr>/<cid>',views.updateQuantity),
    path('placeorder',views.placeOrder),
    path('makepayment',views.makePayment),
    path('sendemail',views.sendemail),
    path('contact',views.Contact_us)
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
