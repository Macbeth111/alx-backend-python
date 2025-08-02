from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # type: ignore
from django.http import JsonResponse  # type: ignore


def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            receiver = User.objects.get(username=data['receiver'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'Receiver not found'}, status=404)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=data['content']
        )
        return JsonResponse({'message': 'Message sent successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user).select_related('sender')
    message_list = [{'sender': m.sender.username,
                     'content': m.content} for m in messages]
    return JsonResponse({'inbox': message_list})


@login_required
def unread_inbox(request):
    messages = Message.unread.for_user(request.user)
    message_list = [{'sender': m.sender.username,
                     'content': m.content} for m in messages]
    return JsonResponse({'unread': message_list})
