from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Message


# Create your views here.
@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return JsonResponse({'message': 'Your account and related data have been deleted.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def inbox(request):
    # Filter messages where the user is sender or receiver
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )

    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def threaded_message_view(request, message_id):
    try:
        message = Message.objects.select_related('sender', 'receiver').get(id=message_id)
    except Message.DoesNotExist:
        return render(request, '404.html', status=404)

    # Recursive function to fetch replies
    def get_thread(msg):
        replies = msg.replies.select_related('sender', 'receiver').all()
        thread = []
        for reply in replies:
            thread.append({
                'message': reply,
                'replies': get_thread(reply)
            })
        return thread

    thread_data = {
        'message': message,
        'replies': get_thread(message)
    }

    return render(request, 'messaging/threaded_message.html', {'thread': thread_data})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread.html', {'messages': unread_messages})
