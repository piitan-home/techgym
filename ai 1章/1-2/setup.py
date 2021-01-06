def allow_all_url() -> None:
    '''
    Allow all urls

    Unconfirmed urls are allowed
    '''
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


def ignore_warnings() -> None:
    import warnings
    warnings.simplefilter('ignore')
