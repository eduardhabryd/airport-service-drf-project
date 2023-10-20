from .views import APIRootView
from rest_framework import routers


class Router(routers.DefaultRouter):
	include_root_view = True
	include_format_suffixes = False
	root_view_name = 'index'
	
	def get_api_root_view(self, api_urls=None):
		return APIRootView.as_view()
