from django.urls import path

from blog.views import BlogListView
from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='category'),
    path('contacts/', contacts, name='contacts'),

    path('<int:pk>/products/', ProductListView.as_view(), name='product_list'),
    path('<create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product'),

    path('blog_list/', BlogListView.as_view(), name='blog_list'),

]
