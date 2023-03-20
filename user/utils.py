from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["usernames"] = user.username
    return {
        'token': str(refresh),
    }