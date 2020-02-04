
class YandexAPIError(Exception):
    error_codes = {
        401: "ERR_KEY_INVALID",
        402: "ERR_KEY_BLOCKED",
        403: "ERR_DAILY_REQ_LIMIT_EXCEEDED",
        413: "ERR_TEXT_TOO_LONG",
        501: "ERR_LANG_NOT_SUPPORTED",
    }

    def __init__(self, response: dict = None):
        status_code = response.get('code')
        message = response.get('message')
        error_name = self.error_codes.get(status_code, "UNKNOWN_ERROR")
        super(YandexAPIError, self).__init__(status_code, error_name, message)


class YandexDictionaryError(Exception):
    pass
