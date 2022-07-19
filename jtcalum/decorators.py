from functools import wraps

# def unread_count():
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapper_view(request, *args, **kwargs):
#             unreadCount = None
#             profile = None
#             try:
#                 profile = request.user.profile
#             except:
#                 pass
#             if profile != None and profile != 'AnonymousUser':
#                 try:
#                     messageRequests = profile.messages.all()
#                     unreadCount = messageRequests.filter(is_read = False).count()
#                 except:
#                     pass
            
#             kargs = kwargs 
#             kwargs = kargs | {'unread': unreadCount}
#             return _wrapper_view
#         return unread_count