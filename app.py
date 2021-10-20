from dashboard import app
import os

if __name__ == '__main__':
    app.run_server('0.0.0.0', os.getenv('PORT'))
    # server = app.server
