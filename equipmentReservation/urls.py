from django.urls import path

from equipmentReservation.views import EquipmentReservationCreateView, EquipmentReservationUpdateView, \
    EquipmentReservationDeleteView

urlpatterns = [
    path('create/eq-reservation', EquipmentReservationCreateView.as_view(), name='create-eq-reservation'),
    path('edit/eq-reservation/<int:pk>', EquipmentReservationUpdateView.as_view(), name='edit-eq-reservation'),
    path('delete/eq-reservation/<int:pk>', EquipmentReservationDeleteView.as_view(), name='delete-eq-reservation'),

]
