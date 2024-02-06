
from django.contrib import admin
from django.urls import path , include , re_path
from django.views.static import serve as mediaserve
from django.conf import settings
from django.conf.urls import handler404,handler500
from main.views import handler_404,handler_500


urlpatterns = [
    path('',include('main.urls',namespace='main')),
    path('admin/', admin.site.urls),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns +=[
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
urlpatterns += [
        re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]

handler404=handler_404
handler500=handler_500