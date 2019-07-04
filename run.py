# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from src.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
