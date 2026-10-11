from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JsonResponse404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return JsonResponse({
                'error': '404',
                'message': 'صفحه مورد نظر یافت نشد یا پاک شده',
                'statusCode': 404
            }, status=404)
        return response


class JsonResponse403Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 403:
            return JsonResponse({
                'error': '403',
                'message': 'شما دسترسی به این url ندارید',
                'statusCode': 403
            }, status=403)
        return response