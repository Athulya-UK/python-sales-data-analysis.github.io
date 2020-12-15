from django.urls import path
from .views import chart_select_view,top_perf_view,low_perf_view,top_branch_view,low_branch_view,count_daily_product,add_purchase_view,dashboard_view,send_email_view,send_email_low_view

app_name='products'

urlpatterns = [
    path('',chart_select_view,name='main-products-view'),
    path('top_perf/',top_perf_view, name='top-view'),
    path('low_perf/',low_perf_view, name='low-view'),
    path('top_branch/',top_branch_view, name='top-branch-view'),
    path('low_branch/',low_branch_view, name='low-branch-view'),
    path('product_daily/',count_daily_product, name='count_daily_product'),
    path('add/',add_purchase_view, name='add-purchase-view'),
    path('dash/',dashboard_view, name='dashboard-view'),
    path('email/',send_email_view, name='send-email-view'),
    path('email1/',send_email_low_view, name='send-email-low-view'),
    

]