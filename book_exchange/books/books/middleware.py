from django.shortcuts import redirect

class SessionInvalidateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the user is authenticated, set the cache control headers
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-store'
        else:
            # If the user is not authenticated, prevent access to authenticated pages
            if request.path in ['/landing', '/any-other-protected-path']:
                return redirect('login')

        return response
