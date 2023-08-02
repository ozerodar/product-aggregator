"""URL mappings for the recipe app"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from offer import views

router = DefaultRouter()
router.register("offers", views.OfferViewSet)

app_name = "offer"

urlpatterns = [path("", include(router.urls))]
