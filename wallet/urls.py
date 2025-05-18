from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    WalletView,
    DepositView,
    WithdrawView,
    TransferView,
    TransactionHistoryView,
    FlaggedTransactionView,
    total_user_balances,
    top_users_by_balance,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/deposit/', DepositView.as_view(), name='deposit'),
    path('wallet/withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('wallet/transfer/', TransferView.as_view(), name='transfer'),

    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('admin/flagged/', FlaggedTransactionView.as_view(), name='flagged-transactions'),
    path('admin/summary/', total_user_balances, name='total-balances'),
    path('admin/top-users/', top_users_by_balance, name='top-users'),
]
