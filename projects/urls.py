from django.urls import path

from . import views
app_name = 'api'

urlpatterns = [
    path('v1/users/create/', views.createUserApiView.as_view(), name='user_create'),
    path('v1/users/list/', views.UserListAPIView.as_view(), name='user-list'),
    path('v1/users/detail/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),

    #bank urls
    path('v1/banks/list/', views.BankListAPIView.as_view(), name='bank-list'),
    path('v1/banks/create/', views.BankCreateAPIView.as_view(), name='bank-create'),
    path('v1/banks/detail/<int:pk>/', views.BankDetailAPIView.as_view(), name='bank-detail'),
    path('v1/banks/update/<int:pk>/', views.BankUpdateAPIView.as_view(), name='bank-update'),
    path('v1/banks/delete/<int:pk>/', views.BankDeleteAPIView.as_view(), name='bank-delete'),

    #Account urls
    path('v1/accounts/list/', views.AccountListAPIView.as_view(), name='accounts-list'),
    path('v1/accounts/detail/<int:pk>/', views.AccountDetailAPIView.as_view(), name='account-detail'),
    path('v1/accounts/create/<int:pk>/', views.AccountCreateAPIView.as_view(), name='account-create'),
    path('v1/accounts/update/<int:pk>/', views.AccountUpdateAPIView.as_view(), name='account-update'),

    #URLS PROVIDERS
    path('v1/providers/list/', views.ProviderListAPIView.as_view(), name='providers-list'),
    path('v1/providers/detail/<int:pk>/', views.ProviderDetailAPIView.as_view(), name='provider-detail'),
    path('v1/providers/create/', views.ProviderCreateAPIView.as_view(), name='provider-create'),
    path('v1/providers/update/<int:pk>/', views.ProviderUpdateAPIView.as_view(), name='provider-update'),
    path('v1/providers/delete/<int:pk>/', views.ProviderDeleteAPIView.as_view(), name='provider-delete'),

]