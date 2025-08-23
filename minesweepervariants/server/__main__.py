import sys

from minesweepervariants.utils.tool import get_logger

import waitress

from .router import app



get_logger(log_lv="DEBUG")
port = int(sys.argv[1] if len(sys.argv) == 2 else "5050")
host = "0.0.0.0"

print(f"server start at {host}:{port}")
waitress.serve(app, host=host, port=port)
