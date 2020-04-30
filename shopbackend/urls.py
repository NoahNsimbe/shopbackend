from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
# from shopbackend.admin import MyAdminSite
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    re_path(r'^', include('main.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    # path('adminSite/', MyAdminSite.urls),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
