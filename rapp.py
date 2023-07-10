#App part written for Flash webserver to serve as REST API for roop
#TO DO: Cleanup the file, document it more.
# version 0.1

from flask import Flask, request, jsonify, send_from_directory, redirect, session, url_for
from werkzeug.utils import secure_filename
import pika, json, os, time, uuid
from rconfig import RoopConfig
from rworker import main as worker_main

app = Flask(__name__)
app.config.from_object(RoopConfig)

image_queue = {}  # Dictionary to store image names and timestamps

def is_allowed_extension(filename):
    """
    Check if the file extension is allowed.
    TO DO: Separate the allowed extensions for source and target. Source cannot be video

    Args:
        filename (str): Name of the file.

    Returns:
        bool: True if the extension is allowed, False otherwise.
    """
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in app.config['ALLOWED_EXTENSIONS_IMAGES'] or ext in app.config['ALLOWED_EXTENSIONS_VIDEO']:
            return True
    return False

def is_allowed_size(file):
    """
    Check if the file size is within the allowed limit.
    TO DO: Separate for video size and image.

    Args:
        file (FileStorage): File object.

    Returns:
        bool: True if the file size is within the limit, False otherwise.
    """
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size <= app.config['MAX_FILE_SIZE_IMAGES'] or file_size <= app.config['MAX_FILE_SIZE_VIDEO']:
        return True
    return False

@app.route('/process', methods=['POST'])
def process_file():
    # Check if the source_path was already submitted and queued
    source_name = request.files['source_path'].filename
    if source_name in image_queue:
        timestamp = image_queue[source_name]
        current_timestamp = time.time()
        time_difference = current_timestamp - timestamp

        if time_difference <= 1:  # Timeframe of 1 minute
            return jsonify({'message': 'Source_path was already submitted and queued. Wait for a mail with more info.'}), 200

    # Update the image queue with the current timestamp
    image_queue[source_name] = time.time()

    # Generate a unique job ID using UUID and log it
    job_id = str(uuid.uuid4())
    app.logger.info(f'New job created with ID: {job_id}')

    try:
        if 'source_path' in request.files:
            source = request.files['source_path']
            filename = secure_filename(source.filename)
            source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            source.save(source_path)
        elif 'source_path' in request.form:
            source_path = request.form['source_path']
            filename = os.path.basename(source_path)
        else:
            return jsonify({'message': 'No source_path file or string in request'}), 400
    except Exception as e:
        # Log the error details
        app.logger.error(f'An error occurred during image processing: {str(e)}')

        # Handle the exception and return an appropriate error response
        return jsonify({'error': 'An error occurred during image processing.', 'details': str(e)}), 500

    #TO DO: Check Job Data why is not writing into dictionary.
    #Write a structure for the job_data, like time created, time updated, job_name, filenames etc.
    job_data = {}
    try:
        if 'target_path' in request.files:
            target = request.files['target_path']
            target_path = os.path.join(app.config['TEMPLATE_FOLDER'], secure_filename(target.filename))
            target.save(target_path)
        elif 'target_path' in request.form:
            target_path = os.path.join(app.config['TEMPLATE_FOLDER'], request.form['target_path'])
            if not os.path.isfile(target_path):
                return jsonify({'message': 'Target file does not exist in TEMPLATE_FOLDER'}), 400
            else:
                job_data['target_path'] = target_path
    except Exception as e:
        # Log the error details
        app.logger.error(f'An error occurred during image processing: {str(e)}')

        # Handle the exception and return an appropriate error response
        return jsonify({'error': 'An error occurred during image processing.', 'details': str(e)}), 500

    # Save the source to the upload folder
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    source.save(source_path)
    app.logger.debug(f"Saved source file to: {source_path}")

    # Validate target_path parameter
    if 'target_path' in request.files:
        target = request.files['target_path']
        filename = secure_filename(target.filename)
        target_path = os.path.join(app.config['TEMPLATE_FOLDER'], filename)
        target.save(target_path)
    elif 'target_path' in request.form:
        target_path = request.form['target_path']
    else:
        app.logger.debug("Missing target_path parameter.")
        return jsonify({'message': 'Missing target_path parameter.'}), 400

    data = {
        'job_id': job_id,
        'source_path': source_path,
        'target_path': target_path,
    }

    #TO DO: Duplicate in rworker.py To put in config in one place.
    optional_parameters = [
        'frame-processor',
        'keep-fps',
        'keep-audio',
        'keep-frames',
        'many-faces',
        'video-encoder',
        'video-quality',
        'max-memory',
        'execution-threads'
    ]

    for param in optional_parameters:
        if param in request.form and request.form[param]:
            data[param] = request.form[param]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')
    app.logger.info(f'Starting job with ID: {job_id}')
    channel.basic_publish(exchange='', routing_key='image_queue', body=json.dumps(data))
    connection.close()

    final_image_url = f"{app.config['SERVER_URL']}/{app.config['FINAL_URL_FOLDER']}/{job_id}.png"

    # Create the response JSON with the job ID, final image URLs, and message
    response = {
        'message': 'Image processing initiated!',
        'job_id': job_id,
        'final_image': final_image_url
    }

    return jsonify(response), 202

@app.route('/generated/<filename>')
def get_generated_file(filename):
    """
    Endpoint to retrieve the generated image.
    TO DO: Get a filename, if exist. Usually to see if the file was generated.

    Args:
        filename (str): Name of the generated image file.

    Returns:
        File: The generated image file.
    """
    return send_from_directory(app.config['FINAL_FOLDER'], filename)

@app.route('/job_status/<job_id>')
def get_job_status(job_id):
    """
    Endpoint to retrieve the status of a job.
    TO DO: Get status of a specific job from dictionary.

    Args:
        job_id (str): The ID of the job.

    Returns:
        JSON: The status of the job.
    """
    app.logger.info(f"Requested job_id: {job_id}")
    app.logger.info(f"Current job statuses: {job_statuses}")

    if job_id in job_statuses:
        return jsonify({'job_id': job_id, 'status': job_statuses[job_id]})
    else:
        app.logger.warning(f'Job ID {job_id} not found in job_statuses')
        return jsonify({'error': 'Job not found'}), 404

# Removed enhance_image endpoint

@app.route('/job_status/')
def get_all_job_statuses():
    """
    Endpoint to retrieve the status of all jobs.
    TO DO: Get status of all jobs from dictionary.

    Returns:
        JSON: The status of all jobs.
        
    """
    app.logger.info(f"Requested all job statuses")
    app.logger.info(f"Current job statuses: {job_statuses}")

    return jsonify(job_statuses)

@app.route('/')
def home():
    app.logger.info(f"HOME")
    return "Welcome API user"

if __name__ == '__main__':
    # Check if running in HTTP or HTTPS mode
    use_https = False  # Set this variable based on your condition
    
    # Configure SSL/TLS context if using HTTPS
    ssl_context = None
    if use_https:
        #ssl_context = 'adhoc'  # Use the built-in self-signed certificate for development/testing
        
        # Use the Cloudflare SSL/TLS certificate and private key for production
        ssl_context = ('certificate.crt', 'private.key')

    # Run the Flask application
    if use_https:
        app.run(ssl_context=ssl_context, host='0.0.0.0', port=443, debug=True)
    else:
        app.run(host='0.0.0.0', port=80, debug=True)

    # Start the worker
    worker_main()
