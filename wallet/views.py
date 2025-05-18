from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum

from .models import Wallet, Transaction
from .serializers import (
    RegisterSerializer,
    WalletSerializer,
    TransactionSerializer
)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


class WalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = Decimal(str(request.data.get('amount', 0)))
        except (InvalidOperation, TypeError):
            return Response({'error': 'Invalid amount format'}, status=400)

        if amount <= 0:
            return Response({'error': 'Amount must be positive'}, status=400)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += amount
        wallet.save()

        Transaction.objects.create(
            from_user=request.user,
            amount=amount,
            type='deposit'
        )

        return Response({'message': 'Deposit successful'}, status=201)


class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = Decimal(request.data.get('amount', 0))
        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        if amount <= 0 or amount > wallet.balance:
            return Response({'error': 'Invalid withdrawal amount'}, status=400)

        wallet.balance -= amount
        wallet.save()

        is_flagged = amount > 1000

        Transaction.objects.create(
            from_user=request.user,
            amount=amount,
            type='withdraw',
            is_flagged=is_flagged
        )

        if is_flagged:
            send_mail(
                'Suspicious Withdrawal Alert',
                f'A large withdrawal of ₹{amount} was flagged.',
                'noreply@wallet.com',
                [request.user.email],
                fail_silently=True,
            )

        return Response({'message': 'Withdrawal successful'})


class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_username = request.data.get('to_user')
        amount = Decimal(request.data.get('amount', 0))

        if not to_username or amount <= 0:
            return Response({'error': 'Invalid transfer details'}, status=400)

        try:
            to_user = User.objects.get(username=to_username)
        except User.DoesNotExist:
            return Response({'error': 'Recipient user not found'}, status=404)

        from_wallet, _ = Wallet.objects.get_or_create(user=request.user)
        to_wallet, _ = Wallet.objects.get_or_create(user=to_user)

        if from_wallet.balance < amount:
            return Response({'error': 'Insufficient balance'}, status=400)

        from_wallet.balance -= amount
        to_wallet.balance += amount
        from_wallet.save()
        to_wallet.save()

        recent_transfers = Transaction.objects.filter(
            from_user=request.user,
            type='transfer',
            timestamp__gte=timezone.now() - timedelta(minutes=1)
        ).count()

        is_flagged = recent_transfers >= 3

        Transaction.objects.create(
            from_user=request.user,
            to_user=to_user,
            amount=amount,
            type='transfer',
            is_flagged=is_flagged
        )

        if is_flagged:
            send_mail(
                'Suspicious Transfer Activity',
                f'High-frequency transfers detected from your account.',
                'noreply@wallet.com',
                [request.user.email],
                fail_silently=True,
            )

        return Response({'message': 'Transfer successful'})


class TransactionHistoryView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            from_user=self.request.user,
            is_deleted=False
        ).order_by('-timestamp')


class FlaggedTransactionView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(is_flagged=True).order_by('-timestamp')


@api_view(['GET'])
def total_user_balances(request):
    total = Wallet.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    return Response({'total_balance': total})


@api_view(['GET'])
def top_users_by_balance(request):
    top_wallets = Wallet.objects.select_related('user').order_by('-balance')[:5]
    data = [
        {
            'username': w.user.username,
            'balance': w.balance
        } for w in top_wallets
    ]
    return Response(data)
