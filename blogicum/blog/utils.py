def get_current_user(request):
    current_user = None
    if request.user.is_authenticated:
        current_user = request.user
    return current_user


def user_allow(request, owner_id):
    user = request.user
    if user.id == owner_id:
        return True
    return False
