#Worker file to hnadle request, send into queue, listen to queue.
#TO DO: More details into worker.log
#Cleanup code, consistency, not used packages

import pika, json, os, time, uuid, subprocess
import torch
import logging
from rconfig import RoopConfig

# Set up logging
logging.basicConfig(
    filename=RoopConfig.LOG_FILE_WORKER,
    level=RoopConfig.LOGGING_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

def process_job(job_data):
    """
    Process a job from the queue.

    Args:
        job_data (dict): The job data.
    """
    logging.info(f'Processing job with ID: {job_data["job_id"]}')
    # Construct the command to call 'run.py' with the appropriate parameters
    output_path = os.path.join(RoopConfig.FINAL_FOLDER, str(job_data['job_id']) + '.png')
    target_path = os.path.join(RoopConfig.TEMPLATE_FOLDER, job_data['target_path'])
    command = [
        'python',
        os.path.join(RoopConfig.ROOP_ROOT_FOLDER, 'run.py'),
        '-s', job_data['source_path'],
        '-t', target_path,
        '-o', output_path,
    ]

    # Check if the execution provider is GPU or CPU (choose from 'tensorrt', 'cuda', 'cpu')
    execution_provider = 'cuda' if torch.cuda.is_available() else 'cpu'
    command.append('--execution-provider')
    command.append(execution_provider)

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
        if param in job_data:
            value = job_data[param]
            if isinstance(value, bool):
                if value:  # Check if the value is True
                    command.append(f'--{param}')
            elif value:  # non-boolean values
                if (param == 'many-faces' or param == 'keep-fps' or param == 'keep-audio' or param == 'keep-frames') and str(value).lower() == 'true':
                    command.append(f'--{param}')
                    command.append('')
                else:
                    command.append(f'--{param}')
                    command.append(str(value))
    # Log the command and call the 'run.py' script
    command_line = ' '.join(command)
    print(f"Executing command: {command_line}")
    logging.info(f"Executing command: {command_line}")
    subprocess.run(command)

def main():
    """
    Main function to start the worker.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RoopConfig.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RoopConfig.RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        job_data = json.loads(body)
        process_job(job_data)

    channel.basic_consume(queue=RoopConfig.RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()
