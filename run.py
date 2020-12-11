# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from src.app import create_app

if __name__ == "__main__":
    # (app, socketio) = create_app()
    # print(socketio)
    # if socketio:
    #     socketio.run(app)
    # else: 
    #     app.run()
    app = create_app()
    app.run()
    
