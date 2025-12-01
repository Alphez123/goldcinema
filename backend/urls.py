from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views
from users import admin_views
from users import advisor_views

urlpatterns = [

    # ==========================
    # USER AUTH
    # ==========================
    path("users/register/", user_views.register_view, name="register"),
    path("users/login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    
    # Account Activation
    path("activate/<uidb64>/<token>/", user_views.activate_account, name="activate"),
    path("registration-pending/", user_views.registration_pending, name="registration_pending"),
    
    # Password Reset
    path("forgot-password/", user_views.password_reset_request, name="password_reset_request"),
    path("reset-password/<uidb64>/<token>/", user_views.password_reset_confirm, name="password_reset_confirm"),

    # ==========================
    # USER HOME / DASHBOARD
    # ==========================
    path("", user_views.landing_page, name="landing_page"),
    path("homepage/", user_views.homepage, name="homepage"),

    # ==========================
    # BOOKINGS (CLIENT)
    # ==========================
    path("book/<str:movie_name>/", user_views.book_movie_page, name="book_movie"),

    # FIXED: POST booking goes here
    path("create-booking/", user_views.create_booking, name="create_booking"),
    path("cancel-my-booking/<int:booking_id>/", user_views.cancel_my_booking, name="cancel_my_booking"),

    # AJAX API
    path("api/bookings/", user_views.get_user_bookings, name="get_bookings"),
    path("api/booked-seats/<str:movie_name>/", user_views.get_booked_seats, name="get_booked_seats"),
    path("download-ticket/<int:booking_id>/", user_views.download_ticket, name="download_ticket"),

    # ==========================
    # ACCOUNT PAGE
    # ==========================
    path("account/", user_views.account_view, name="account"),
    path("account/update/", user_views.update_account, name="update_account"),
    path("account/delete/", user_views.delete_account_view, name="delete_account"),
    path("deposit/", user_views.deposit_view, name="deposit"),

    # Account Management (AJAX)
    path("users/update-profile/", user_views.update_profile, name="update_profile"),
    path("users/change-password/", user_views.change_password, name="change_password_ajax"),
    path("users/delete-account/", user_views.delete_account, name="delete_account_ajax"),

    # Notifications API
    path("api/notifications/", user_views.get_notifications, name="get_notifications"),
    path("api/notifications/mark-read/<int:notification_id>/", user_views.mark_notification_read, name="mark_notification_read"),

    # ==========================
    # DEFAULT DJANGO ADMIN
    # ==========================
    path("admin/", admin.site.urls),

    # ==========================
    path("cancel/<int:booking_id>/", admin_views.cancel_booking, name="cancel_booking"),

    # MOVIES MANAGEMENT
    path("admin-dashboard/movies/", admin_views.admin_movies, name="admin_movies"),
    path("admin-dashboard/movies/add/", admin_views.admin_movie_add, name="admin_movie_add"),
    path("admin-dashboard/movies/edit/<int:movie_id>/", admin_views.admin_movie_edit, name="admin_movie_edit"),
    path("admin-dashboard/movies/delete/<int:movie_id>/", admin_views.admin_movie_delete, name="admin_movie_delete"),

    # ==========================
    # CUSTOM ADMIN DASHBOARD
    # ==========================
    path("admin-dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),

    # USERS MANAGEMENT
    path("admin-dashboard/users/", admin_views.admin_users, name="admin_users"),
    path("admin-dashboard/users/<int:user_id>/", admin_views.admin_user_detail, name="admin_user_detail"),
    path("admin-dashboard/users/<int:user_id>/delete/", admin_views.delete_user_admin, name="delete_user_admin"),

    # BOOKINGS MANAGEMENT
    path("admin-dashboard/bookings/", admin_views.admin_bookings, name="admin_bookings"),
    path("admin-dashboard/booking/delete/<int:booking_id>/", admin_views.delete_booking_admin, name="delete_booking_admin"),

    # HISTORY
    path("admin-dashboard/history/", admin_views.admin_history, name="admin_history"),
    
    # CREATE ADVISOR
    path("admin-dashboard/create-advisor/", admin_views.create_advisor, name="create_advisor"),

    # ==========================
    # ADVISOR SYSTEM
    # ==========================
    path("advisor/dashboard/", advisor_views.advisor_dashboard, name="advisor_dashboard"),
    path("advisor/chat/<int:user_id>/", advisor_views.advisor_chat, name="advisor_chat"),
    
    # User Side Support
    path("support/advisors/", advisor_views.advisor_list, name="advisor_list"),
    path("support/chat/", advisor_views.user_chat, name="user_chat"),
    path("support/chat/<int:advisor_id>/", advisor_views.user_chat, name="user_chat_with_advisor"),
    
    # Chat API
    path("api/chat/send/", advisor_views.send_message, name="send_message"),
    path("api/chat/get/<int:other_user_id>/", advisor_views.get_messages, name="get_messages"),
    path("api/chat/unread/", advisor_views.get_unread_count, name="get_unread_count"),
]

# MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
