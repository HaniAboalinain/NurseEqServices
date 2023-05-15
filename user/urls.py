from django.urls import path

from user.views import UserUpdateView, UserDetailView, StaffDashboardView, StaffListView, NurseRequestCreateView, \
    DoctorDetailView, RateCreateView

urlpatterns = [
    path('update/<int:pk>/info', UserUpdateView.as_view(), name='user-update-info'),
    path('<int:pk>/info', UserDetailView.as_view(), name='user-info'),
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff-dashboard'),
    path('list/staff/', StaffListView.as_view(), name='staff-list'),
    path('nurse-request/', NurseRequestCreateView.as_view(), name='nurse-request'),

    path('<int:pk>/doctor-details/', DoctorDetailView.as_view(), name='doctor-details'),
    path('<int:pk>/doctor-details/', DoctorDetailView.as_view(), name='doctor-details'),
]
