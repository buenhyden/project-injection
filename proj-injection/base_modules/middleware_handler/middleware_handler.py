"""Custom Middleware."""


class CheckHeaderForAuthorizationMiddleware:
    """Request에서 header를 확인하고, Authorization가 Bearer로 시작하지 않을 경우, 채워주는 Middleware."""

    def __init__(self, get_response):
        """One-time configuration and initialization."""
        self.get_response = get_response
        #

    def __call__(self, request):
        """Code to be executed for each request before.

        the view (and later middleware) are called.
        """
        authorization = request.headers.get("Authorization")
        if authorization is not None and not authorization.startswith("Bearer"):
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {authorization}"

        response = self.get_response(request)

        return response
