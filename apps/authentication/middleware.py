from django.utils.deprecation import MiddlewareMixin


class RedirectFirstTimeFromSearchEngineMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Проверяем, пришел ли пользователь через поисковые системы
        referrer = request.META.get('HTTP_REFERER', '')
        if 'google' in referrer.lower() or 'yandex' in referrer.lower():
            # Проверяем, был ли уже установлен флаг первого входа через поисковые системы
            if not request.session.get('first_time_from_search_engine', False):
                request.session['first_time_from_search_engine'] = True
                # Перенаправляем на страницу выбора типа пользователя
                from django.shortcuts import redirect
                return redirect('choice')
