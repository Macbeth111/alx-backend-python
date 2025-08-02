from django.http import JsonResponse
from django.views.decorators.cache import cache_page


@cache_page(60)  # Cache for 60 seconds
def list_messages(request):
    messages = [
        {"sender": "alice", "content": "Hello!"},
        {"sender": "bob", "content": "Hi, how are you?"}
    ]
    return JsonResponse({"messages": messages})
