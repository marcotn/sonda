from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Permette il login solo a utenti già presenti con is_staff=True
        return False

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if not user.pk:
            # Utente non ancora in DB: cerca per email
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                existing = User.objects.get(email=user.email)
            except User.DoesNotExist:
                from allauth.socialaccount.models import SignupClosedException
                raise SignupClosedException()
            if not existing.is_staff:
                from allauth.socialaccount.models import SignupClosedException
                raise SignupClosedException()
            sociallogin.connect(request, existing)
