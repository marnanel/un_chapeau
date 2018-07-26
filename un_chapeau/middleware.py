def middleware(get_response):

    ACTIVITY_SUFFIX = '.json'

    def un_chapeau_middleware(request):

        if 'application/activity+json' in request.META.get('HTTP_ACCEPT', ''):
            request.path_info = request.path_info+ACTIVITY_SUFFIX

        #################

        response = get_response(request)

        #################

        response['Server'] = 'un_chapeau'

        #################

        return response

    return un_chapeau_middleware
