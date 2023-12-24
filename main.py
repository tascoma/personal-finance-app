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

# TODO:
# Complete manage_data.py to edit and delete data
# Complete the form.html to edit and delete data
# Complete the close_books.py to close books