api_errors = {
    'WrongTokenError': {
        'message': "Wrong token. Please provide a valid token.",
        'status': 401
    },
    'InvalidSignatureError': {
        'message': "Invalid signature. Please provide a valid token.",
        'status': 401
    },
    'ExpiredSignatureError': {
        'message': "Expired signature. Please provide a valid token.",
        'status': 401
    },
    'NoAuthorizationError': {
        'message': "Missing Authorization header.",
        'status': 401
    }
}