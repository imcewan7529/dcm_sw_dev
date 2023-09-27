# dcm_sw_dev
To bringup a new RPI for testing, run the following command: <br>
curl -s https://raw.githubusercontent.com/imcewan7529/dcm_sw_dev/main/setup.sh | sudo bash

Note to developers:
This script assumes that your software component has a specific file structure. An example using the ADC manager app: <br>
/repo_root/ <br>
|-- /ADC_manager/ <br>
|&emsp;&emsp;|-- /systemd/ <br>
|&emsp;&emsp;|&emsp;&emsp;|-- service_name.service <br>
|&emsp;&emsp;|-- /src/ <br> 
|&emsp;&emsp;|&emsp;&emsp;|-- all source code <br>
|&emsp;&emsp;|-- /requirements/ <br>
|&emsp;&emsp;|&emsp;&emsp;|-- requirements.txt <br>

Ensure that when you are adding a new service/software component (swc), that it follows this directory structure, otherwise the setup.sh script will fail!
