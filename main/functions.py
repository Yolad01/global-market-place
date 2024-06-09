from main.models import Wallet, Payment




def user_wallet(user):
    payment = Payment.objects.filter(skilla=user).last()
    wallet, _ = Wallet.objects.get_or_create(
        user=user,
    )
    if payment:
        wallet.pending += payment.pending
        wallet.save()
        payment.pending = 0.00
        payment.save()
        return wallet.pending
    

