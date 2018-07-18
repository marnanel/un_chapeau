def middleware(get_response):

    ACTIVITY_SUFFIX = '.json'

    def _divert_to_activity(request):
        request.urlconf = 'kepi_activity.urls'

    def trilby_middleware(request):

        if request.path_info.endswith(ACTIVITY_SUFFIX):
            request.path_info = request.path_info[:-len(ACTIVITY_SUFFIX)]

            _divert_to_activity(request)

        if 'application/activity.json' in request.META['HTTP_ACCEPT']: 
            _divert_to_activity(request)

        #################

        response = get_response(request)

        #################

        response['Server'] = 'un_chapeau'

        #################

        return response

    return trilby_middleware
