#!/bin/bash

# Update and install essential tools
sudo apt update
sudo apt install -y git python3-pip rabbitmq-server

# Start and set up RabbitMQ
sudo systemctl start rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
wget http://localhost:15672/cli/rabbitmqadmin
chmod +x rabbitmqadmin
sudo mv rabbitmqadmin /usr/local/bin/

# Define the GitHub repository URL
REPO_URL="https://github.com/imcewan7529/dcm_sw_dev.git"
CLONE_PATH="/tmp/dcm_sw_dev"

# Clone the repository
git clone $REPO_URL $CLONE_PATH

# Loop through software components and set them up
for dir in $CLONE_PATH/*; do
    # Skip the practice_code directory
    if [[ "$(basename $dir)" == "practice_code" ]]; then
        continue
    fi

    # If 'src' directory is present, proceed with copying and requirements installation
    if [ -d "$dir/src" ]; then
        # Copy source code to /usr/bin
        sudo cp -r "$dir/src" "/usr/bin/$(basename $dir)"

        # Install requirements if present
        if [ -f "$dir/requirements/requirements.txt" ]; then
            pip3 install -r "$dir/requirements/requirements.txt"
        fi
    fi

    # If 'systemd' directory is present, copy service files and enable/start them
    if [ -d "$dir/systemd" ]; then
        for service_file in "$dir/systemd"/*.service; do
            sudo cp "$service_file" /etc/systemd/system/
            service_name=$(basename "$service_file")
            sudo systemctl daemon-reload
            sudo systemctl enable "$service_name"
            sudo systemctl start "$service_name"
        done
    fi
done

# Check for the existence of the DCM_Main_Exchange and delete if it exists
if rabbitmqadmin list exchanges name | grep -q "DCM_Main_Exchange"; then
    rabbitmqadmin delete exchange name=DCM_Main_Exchange
fi

# Initialize the RabbitMQ exchange, explicitly setting it to durable
rabbitmqadmin declare exchange name=DCM_Main_Exchange type=fanout durable=true

# Cleanup by removing cloned repo
rm -rf $CLONE_PATH

# Enable SPI
# Check if SPI0 is enabled, if not, enable it
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt > /dev/null
fi

# Check if SPI1 is enabled, if not, enable it
if ! grep -q "^dtoverlay=spi1-3cs" /boot/config.txt; then
    echo "dtoverlay=spi1-3cs" | sudo tee -a /boot/config.txt > /dev/null
fi

echo "Setup completed."
