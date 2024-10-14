"""Response의 형식을 통일하기 위한 Handler."""

from rest_framework.response import Response

from defines import ResponseStatus


def response_handler(response_status: int, result: dict, status_code: int, headers={}):
    """request에 대한 response의 포맷을 통일하기 위한 함수.

    Args:
        response_status (int): request의 성공/실패 여부
        result (dict): 결과값
        status_code (int): _http status code
        headers (dict): response에 적용할 headers

    Returns:
        rest_framework.response.Response: 응답
    """
    response = {}
    if response_status == ResponseStatus.FAIL.value:
        response["status"] = response_status
        response["message"] = result["message"]
        response["error_code"] = result["error_code"]

    else:
        response["status"] = response_status
        response["result"] = result
    if headers != {}:
        res = Response(response, status=status_code, headers=headers)
    else:
        res = Response(response, status=status_code)
    return res
