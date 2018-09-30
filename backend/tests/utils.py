from base64 import b64encode


def make_basic_auth_headers(username, password):
    return {
        'Authorization': 'Basic ' + b64encode(bytes("{0}:{1}".format(
            username, password), 'ascii')).decode('ascii')}


def make_token_auth_headers(access_token):
    return {'Authorization': 'Bearer ' + access_token}
