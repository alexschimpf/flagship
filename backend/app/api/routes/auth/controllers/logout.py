from fastapi.responses import RedirectResponse
from fastapi import status

from app.config import Config


class LogoutController:

    @staticmethod
    def handle_request() -> RedirectResponse:
        response = RedirectResponse(url=f'{Config.UI_BASE_URL}/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key=Config.SESSION_COOKIE_KEY)
        return response
