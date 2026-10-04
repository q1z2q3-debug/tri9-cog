"""Allow `python -m tri9cog ...`."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())