from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import AutorViewSet, EditoraViewSet

router = SimpleRouter()
router.register(r'autores', AutorViewSet)
router.register(r'editoras', EditoraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
