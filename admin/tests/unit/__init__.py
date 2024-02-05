from app.config import Config
from app.services.strings.service import StringsService


Config.init()
StringsService.init(default_locale=Config.DEFAULT_LOCALE)
