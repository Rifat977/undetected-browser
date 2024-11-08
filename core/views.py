from django.shortcuts import render, redirect
from django.http import JsonResponse
from .driver import *

browsers = {}

def index(request):
    if request.method == 'POST':
        proxy_strings = request.POST.getlist('proxies[]')
        results = {}

        for i, proxy in enumerate(proxy_strings):
            browser_name = f"Browser {i + 1}"
            proxy = proxy.replace('\r', '').strip()

            if proxy:  # If a proxy is provided
                ip = fetch_ip_using_proxy(proxy, browser_name)
            else:  # No proxy provided, run without proxy
                ip = fetch_ip_using_proxy(None, browser_name)
                
            results[browser_name] = ip

        return JsonResponse({'results': results})

    return render(request, 'index.html')

def profiles(request):
    return render(request, 'portal/profiles.html')

def stop_browser(request, browser_name):
    if browser_name in browsers:
        try:
            # Attempt to quit the browser
            browsers[browser_name].quit()
            del browsers[browser_name]
            return JsonResponse({'status': 'success', 'message': f'{browser_name} browser closed successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error closing {browser_name} browser: {str(e)}'})
    else:
        return JsonResponse({'status': 'error', 'message': f'{browser_name} browser not found.'})
