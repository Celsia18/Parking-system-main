from django.contrib import admin
from django.urls import path, include
from main.api import views as api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'places', api_views.ParkingPlaceViewset)
router.register(r'statuses', api_views.ParkingPlaceStatusViewset)
router.register(r'parkings', api_views.ParkingViewset)
router.register(r'types', api_views.ParkingPlaceTypeViewset)
router.register(r'profiles', api_views.ProfileViewset)
router.register(r'questions', api_views.QuestionViewset)
router.register(r'prefs', api_views.PreferencesViewset)
router.register(r'logs', api_views.LogViewset)

for url in router.urls: print(url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/v1/', include(router.urls)),
    path("api/v1/places/<pk>/parking/", api_views.ParkingPlaceListView.as_view(), name="api-place-list"),
]
