from django.utils.deprecation import MiddlewareMixin

class DisableClientSideCachingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Isse browser ko instruction milti hai ki page cache na kare
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response