from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [

    *router.urls
]