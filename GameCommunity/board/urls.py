from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AdvertView, AdvertDetail, ProfileView
from .views import AdvertCreateView, AdvertUpdateView, AdvertDeleteView, ProfileMessageView, upgrade_me
from .views import CommentAccept, ProfileList, CommentDelete


app_name = 'board'

urlpatterns = [
    path('', AdvertView.as_view(), name='allAdverts'),
    path('adverts/<int:pk>', AdvertDetail.as_view(), name='AdvertDetail'),    

    path('adverts/add', AdvertCreateView.as_view(), name='create'),
    path('adverts/edit/<int:pk>', AdvertUpdateView.as_view(), name='update'),
    path('adverts/delete/<int:pk>', AdvertDeleteView.as_view(), name='delete'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/responses', ProfileList.as_view(), name='responses'),
    path('profile/messages', ProfileMessageView.as_view(), name='messages'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('<int:pk>/accept', CommentAccept.as_view(), name='accept'),
    path('<int:pk>/delete', CommentDelete.as_view(), name='com_delete'),    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)