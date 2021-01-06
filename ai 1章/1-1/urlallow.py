import ssl
from warnings import warn


def allow_all_https(show_warning: bool = True):
    '''
    使用目的
    -------
    未確認のurlに接続できるようにします
    '''
    # webの証明書を確認しないし、証明書がなくてもエラーを出力しない
    ssl._create_default_https_context = ssl._create_unverified_context
    if show_warning:
        warn('未確認のurlへリクエストをすると危険な場合があります 非表示にする場合は show_warning = False としてください')
