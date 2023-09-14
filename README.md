# dcm_sw_dev
To bringup a new RPI for testing, run the following command:
curl -s https://raw.githubusercontent.com/imcewan7529/dcm_sw_dev/main/setup.sh | sudo bash

Note to developers:
This script assumes that your software component has a specific file structure. An example using the ADC manager app:
/repo_root/
|-- /ADC_manager/
|   |-- /systemd/
|   |   |-- service_name.service
|   |-- /src/
|   |   |-- all source code
|   |-- /requirements/
|   |   |-- requirements.txt

Ensure that when you are adding a new service, that it follows this directory structure, otherwise the setup.sh script will fail!