from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler


def get_error_message(data):
    error = data.popitem()[1]
    return error[0] if isinstance(error, list) else get_error_message(error)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and response.data.get('detail'):
            response.data['message'] = response.data.pop('detail')

        # Now add the HTTP status code to the response.
        if isinstance(response.data, ReturnDict):
            response.data = {
                'message': get_error_message(response.data)
            }
    return response
