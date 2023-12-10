from webapp import create_app
import logging.config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

try:
    logger.info('Starting application')
    app = create_app()

except Exception as e:
    logger.error('Error starting application', exc_info=True)

if __name__ == '__main__':
    app.run(debug=True)