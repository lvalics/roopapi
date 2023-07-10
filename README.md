# Setting up the API.

## Prerequisites
- A server environment (e.g., Linux, Ubuntu)
- Python (version compatible with the required packages)
- Postman (or a similar API development tool for testing)

## 1. RabbitMQ Installation
- Refer to the official RabbitMQ documentation to install RabbitMQ on your Ubuntu server (RabbitMQ.md).. If you are using a different environment, please consult ChatGPT for assistance.

## 2. Configuration
- Locate the `rconfig.py` file and fill in the necessary values. This configuration file contains the required settings for your RabbitMQ setup and folder structures.

## 3. Environment Setup
- Create an environment on your server and navigate to the project directory (you can try to use roop ENV as well).
- Install the project dependencies by running the command `pip install -r requirements.txt`. Note that some packages listed in `requirements.txt` may no longer be used. For example, the `cryptography` package is only required if you are using adhoc Flask.

## 4. Server Configuration
- Set up a domain or use a simple IP for your server. This guide assumes you are using Linux, specifically Ubuntu, for testing with RabbitMQ. However, it should work on other servers as well.

## 5. Running the Main App
- Execute the command `python rapp.py` to run the main application. This will start the API and make it ready to listen for requests.

## 6. Running the Worker Process
- Run the command `python rworker.py` to start the worker process responsible for handling jobs from RabbitMQ.
- Optionally, you can set up the worker process as a service. Normally, the worker process is configured to work only if `rapp.py` is running. However, it is recommended to test this setup to ensure it functions as expected.

## 7. Sending a Request
- Open Postman (or a similar tool) and make a POST request to `https://YOUR_URL/process`. Include the required parameters in the request body, as shown in the provided image.
- Send the request, and the job processing should commence successfully.

## Additional Notes
- Ensure that you have the "roop" package installed, as it is a prerequisite for this setup.
- Inside the "roop" package, you should have a folder named "api" with the required file structure. Make sure it is present.

## To-Do
- Authentication implementation and code cleaning are pending. These tasks will be addressed based on user feedback.

Please feel free to reach out if you have any questions or encounter any issues during the setup process.
