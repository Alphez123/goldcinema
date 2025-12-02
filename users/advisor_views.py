from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser, ChatMessage
import json

# --- Helper: Check if user is advisor ---
def is_advisor(user):
    return user.is_authenticated and (user.is_advisor or user.is_superuser)

# ================================
# ADVISOR DASHBOARD
# ================================
@login_required
@user_passes_test(is_advisor)
def advisor_dashboard(request):
    """
    Advisor sees a list of users who have chatted or are online.
    For simplicity, we'll list all users who have sent a message or are recently active.
    """
    # Get users who have sent messages or are recently active
    # We can also just list all users for now, or filter by those who initiated chat
    
    # Get distinct users involved in chats
    chat_users = CustomUser.objects.filter(
        Q(sent_messages__isnull=False) | Q(received_messages__isnull=False)
    ).distinct().exclude(id=request.user.id)

    # Annotate with last message time or unread count if needed
    # For now, just pass the list
    
    return render(request, "advisor/dashboard.html", {
        "chat_users": chat_users
    })

@login_required
@user_passes_test(is_advisor)
def advisor_chat(request, user_id):
    """
    Advisor chat interface with a specific user.
    """
    other_user = get_object_or_404(CustomUser, id=user_id)
    
    # Mark messages from this user as read
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, "advisor/chat.html", {
        "other_user": other_user
    })

# ================================
# USER CHAT
# ================================
# ================================
# USER CHAT
# ================================
from django.contrib.auth import authenticate, login
from django.contrib import messages

def advisor_login(request):
    if request.user.is_authenticated and (request.user.is_advisor or request.user.is_superuser):
        return redirect("advisor_dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_advisor or user.is_superuser:
                login(request, user)
                return redirect("advisor_dashboard")
            else:
                messages.error(request, "Access denied. Not an advisor account.")
        else:
            messages.error(request, "Invalid credentials.")
            
    return render(request, "advisor/login.html")

@login_required
def advisor_list(request):
    """
    List available advisors for the user to choose from.
    """
    advisors = CustomUser.objects.filter(is_advisor=True)
    
    # If no advisors, fallback to superusers
    if not advisors.exists():
        advisors = CustomUser.objects.filter(is_superuser=True)
        
    return render(request, "advisor_list.html", {
        "advisors": advisors
    })

def api_get_advisors(request):
    """
    API to get list of advisors for the popup
    """
    advisors = CustomUser.objects.filter(is_advisor=True)
    if not advisors.exists():
        advisors = CustomUser.objects.filter(is_superuser=True)
    
    data = []
    for adv in advisors:
        data.append({
            "id": adv.id,
            "name": f"{adv.first_name} {adv.last_name}" if adv.first_name else adv.username,
            "status": "Online" # Simplified for now
        })
    
    return JsonResponse({"advisors": data})

@login_required
def user_chat(request, advisor_id=None):
    """
    User chat interface.
    If advisor_id is provided, chat with that advisor.
    Otherwise, try to resume last chat or redirect to advisor list.
    """
    advisor = None
    
    if advisor_id:
        advisor = get_object_or_404(CustomUser, id=advisor_id)
        if not (advisor.is_advisor or advisor.is_superuser):
             return redirect('advisor_list')
    else:
        # Try to find last chatted advisor
        last_msg = ChatMessage.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).filter(
            Q(sender__is_advisor=True) | Q(receiver__is_advisor=True)
        ).order_by("-timestamp").first()
        
        if last_msg:
            advisor = last_msg.receiver if last_msg.sender == request.user else last_msg.sender
        else:
            # No history, redirect to list
            return redirect('advisor_list')

    return render(request, "user_chat.html", {
        "advisor": advisor
    })

# ================================
# API FOR CHAT (AJAX)
# ================================
@login_required
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            receiver_id = data.get("receiver_id")
            message_text = data.get("message")
            
            if not message_text or not receiver_id:
                return JsonResponse({"success": False, "error": "Missing data"})
            
            receiver = get_object_or_404(CustomUser, id=receiver_id)
            
            msg = ChatMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message_text
            )
            
            return JsonResponse({
                "success": True,
                "message": {
                    "id": msg.id,
                    "text": msg.message,
                    "timestamp": msg.timestamp.strftime("%H:%M"),
                    "sender_id": msg.sender.id
                }
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
            
    return JsonResponse({"success": False, "error": "Invalid method"})

@login_required
def get_messages(request, other_user_id):
    """
    Get messages between request.user and other_user_id
    """
    other_user = get_object_or_404(CustomUser, id=other_user_id)
    
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by("timestamp")
    
    # Mark as read if receiving
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    data = [{
        "id": m.id,
        "text": m.message,
        "timestamp": m.timestamp.strftime("%H:%M"),
        "sender_id": m.sender.id,
        "is_mine": m.sender.id == request.user.id
    } for m in messages]
    
    return JsonResponse({"messages": data})

@login_required
def get_unread_count(request):
    count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({"unread_count": count})
