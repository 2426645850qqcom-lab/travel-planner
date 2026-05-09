"""启动脚本"""

import sys

# Windows 下强制使用 UTF-8 编码输出，避免中文/emoji 导致 UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn
from app.api.main import app
from app.core.config import get_settings


if __name__ == "__main__":
    settings = get_settings()

    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        timeout_keep_alive=300
    )
