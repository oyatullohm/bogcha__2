
from django.contrib import admin
from django.urls import path , include , re_path
from django.views.static import serve as mediaserve
from django.conf import settings

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

