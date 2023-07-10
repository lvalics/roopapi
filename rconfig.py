import os
import logging

class RoopConfig:
    """
    Configuration class for the image processing application.
    """
    ROOT_FOLDER = os.getenv('ROOT_FOLDER', '/home/roop/api/')  #CHANGE IT!!!!!
    """
    Root folder where is the API. API folder need to be inside of roop directory.
    """
    USE_HTTPS = bool(os.getenv('USE_HTTPS', 'True'))
    """
    Determines whether the application uses HTTP or HTTPS.
    """
    protocol = 'https://' if USE_HTTPS else 'http://'
    """
    The protocol (HTTP or HTTPS) based on the `USE_HTTPS` configuration. 
    """
    SERVER_URL = os.getenv('SERVER_URL', f"{protocol}roop.3dphoto.io")  #CHANGE IT!!!!!
    """
    The URL of the server where the file will be downloaded and the application is running.
    """

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(ROOT_FOLDER, 'upload/'))
    """
    The folder where uploaded images will be stored.
    Note: Files are not deleted automatically in the current implementation.
    """

    FINAL_FOLDER = os.getenv('FINAL_FOLDER', os.path.join(ROOT_FOLDER, 'generated/'))
    """
    The folder where the generated images will be stored.
    """

    FINAL_URL_FOLDER = os.getenv('FINAL_URL_FOLDER', 'generated')
    """
    The URL path for the generated images.
    Note: If the `FINAL_FOLDER` path is changed, this URL path should be updated accordingly.
    """

    TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', os.path.join(ROOT_FOLDER, 'template/'))
    """
    The folder where the template images (video files, image files) are stored.
    """

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    """
    The hostname of the RabbitMQ server.
    """

    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'image_queue')
    """
    The name of the queue used for image processing jobs in RabbitMQ.
    """

    LOG_FILE_WORKER = os.getenv('LOG_FILE_WORKER', 'worker.log')
    """
    The filename of the log file for worker errors.
    """

    LOG_FILE_UPSCALE = os.getenv('LOG_FILE_UPSCALE', 'upscale.log')
    """
    The filename of the log file for upscale errors.
    """

    LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', str(logging.INFO)))
    """
    The logging level for worker errors.
    """

    FRAME_PROCESSOR = os.getenv('FRAME_PROCESSOR', '--frame-processor')
    KEEP_FPS =  os.getenv('KEEP_FPS', '--keep-fps')
    KEEP_AUDIO =  os.getenv('FRAME_PROCESSOR', '--keep-audio')
    FRAME_MANYFACES =  os.getenv('FRAME_MANYFACES', '--many-faces')
    VIDEO_ENCODER =  os.getenv('VIDEO_ENCODER', '--video-encoder')
    VIDEO_QUALITY =  os.getenv('VIDEO_QUALITY', '--video-quality')
    MAX_MEMORY =  os.getenv('MAX_MEMORY', '--max-memory')
    EXECUTION_THREADS =  os.getenv('EXECUTION_THREADS', '--execution-threads')
    """
    Parameters to Roop App.
    """
    ALLOWED_EXTENSIONS_IMAGES = os.getenv('ALLOWED_EXTENSIONS', ('png', 'jpg', 'jpeg'))
    ALLOWED_EXTENSIONS_VIDEO = os.getenv('ALLOWED_EXTENSIONS', ('avi' 'mov' 'mp4' 'mpeg'))
    MAX_FILE_SIZE_IMAGES = 10 * 1024 * 1024  # 10MB
    MAX_FILE_SIZE_VIDEO = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def init_app(app):
        """
        Optionally perform any additional initialization tasks for the application.

        Args:
            app (Flask): The Flask application instance.
        """
        pass
