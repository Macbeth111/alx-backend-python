from django.contrib.auth.models import User  # type: ignore
from django.http import JsonResponse  # type: ignore


def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
