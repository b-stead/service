from rest_framework_simplejwt.tokens import BlacklistMixin, AccessToken


class BlacklistableAccessToken(BlacklistMixin, AccessToken):
    """
    Custom access token that can be blacklisted.
    This class extends the default AccessToken from Simple JWT
    to include blacklist functionality.
    """

    pass
