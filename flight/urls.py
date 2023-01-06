from rest_framework import routers
from .views import FlightView, ReservationView

router = routers.DefaultRouter()
router.register("flights", FlightView)
router.register("reservation", ReservationView)

urlpatterns = [

]
urlpatterns += router.urls