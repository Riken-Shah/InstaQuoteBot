import requests


def send_request(url, method='get', headers=None):
    """
    This function returns an API response
    :param url: api url
    :param method: api method
    :param headers: api headers
    :return: requests instance
    """
    if not (method == 'get' or method == 'post'):
        raise ValueError('method should only be `get` or `post` ')
    return getattr(requests, method)(url=url, headers=headers)
