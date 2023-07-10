To install RabbitMQ on a Ubuntu system, you can follow these steps:

1. **Update the Packages**

    Update the packages to the latest version with the following command:

    ```bash
    sudo apt-get update -y
    sudo apt-get upgrade -y
    ```

2. **Install Required Packages**

    Install the necessary packages, Erlang being a chief one as RabbitMQ is built on the Erlang runtime. 

    ```bash
    sudo apt-get install -y erlang
    ```

3. **Add the RabbitMQ Repository**

    To add the official RabbitMQ repository, first add the RabbitMQ signing key to your system:

    ```bash
    wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
    ```

    Add the RabbitMQ repository to your system's sources:

    ```bash
    echo "deb https://dl.bintray.com/rabbitmq-erlang/debian buster erlang" | sudo tee /etc/apt/sources.list.d/bintray.erlang.list
    echo "deb https://dl.bintray.com/rabbitmq/debian buster main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
    ```

4. **Update the Package Lists**

    To make sure your system knows about the packages in the RabbitMQ repository you just added, update the package lists:

    ```bash
    sudo apt-get update -y
    ```

5. **Install RabbitMQ Server**

    Install the RabbitMQ server:

    ```bash
    sudo apt-get install -y rabbitmq-server
    ```

6. **Start and Enable RabbitMQ Service**

    Once the RabbitMQ server is installed, start the RabbitMQ service and enable it to launch at boot with:

    ```bash
    sudo systemctl start rabbitmq-server
    sudo systemctl enable rabbitmq-server
    ```

7. **Check the Status of RabbitMQ Service**

    You can check the status of the RabbitMQ service to ensure that it is running properly:

    ```bash
    sudo systemctl status rabbitmq-server
    ```

This installs RabbitMQ and sets it up to run as a service, meaning that it will start up automatically whenever your system boots.

Please note that these instructions are for Ubuntu 18.04 LTS and newer versions, so they may not work exactly as written on other systems. You may need to adapt them for your specific operating system.

You can monitor RabbitMQ server and get information about exchanges, queues, bindings, and more by using RabbitMQ management plugin. If it's not enabled by default, you can enable it by running:

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Once the plugin is enabled, you can access the RabbitMQ management console via a web browser at:

```http
http://localhost:15672
```

By default, the username and password are both "guest".

However, if you prefer to use command line, you can use the following commands:

1. **List of Queues**

    ```bash
    sudo rabbitmqctl list_queues
    ```

2. **List of Exchanges**

    ```bash
    sudo rabbitmqctl list_exchanges
    ```

3. **List of Bindings**

    ```bash
    sudo rabbitmqctl list_bindings
    ```

4. **List of Connections**

    ```bash
    sudo rabbitmqctl list_connections
    ```

5. **List of Channels**

    ```bash
    sudo rabbitmqctl list_channels
    ```

6. **List of Consumers**

    ```bash
    sudo rabbitmqctl list_consumers
    ```

Remember to replace `localhost` with the IP address of your RabbitMQ server if it's not on the same machine.

The default 'guest' user in RabbitMQ is only permitted to access the server from localhost for security reasons. 
This is a good default setting for security, but if you want to change it, you'll need to add a new user.

You can add a new user and give it permissions by using the following commands:

1. **Add a new user**

   Replace 'newuser' and 'newpassword' with your desired username and password.

    ```bash
    sudo rabbitmqctl add_user newuser newpassword
    ```

2. **Set user tags**

    The tags parameter is a comma-separated list of user tags for the user. The tag 'administrator' will provide the user with administrative privileges.

    ```bash
    sudo rabbitmqctl set_user_tags newuser administrator
    ```

3. **Set permissions for the new user**

    This command gives the new user access to all resources, including virtual hosts, exchanges, queues, bindings, etc.

    ```bash
    sudo rabbitmqctl set_permissions -p / newuser ".*" ".*" ".*"
    ```

After running these commands, you should be able to connect to RabbitMQ from a remote host using the new username and password you've just created. 

Remember to replace 'newuser' and 'newpassword' with the actual username and password you want to use. Make sure to use a strong, unique password to keep your RabbitMQ server secure.

And of course, ensure your firewall rules allow connections to RabbitMQ ports (typically 5672 for the messaging service itself, and 15672 for the web-based management plugin if it's enabled and you want to access it remotely).
