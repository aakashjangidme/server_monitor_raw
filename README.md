### Server Monitoring Tool

The Server Monitoring Tool is crafted to gather and oversee diverse metrics, encompassing memory usage, disk space, and
active processes across multiple Unix servers. This project, implemented in Python, utilizes SSH connections to access
Unix servers as specified in the server_config.yaml file. The tool systematically collects metrics according to the
configurations provided.

Feel free to download and expand upon this tool based on your specific needs. Whether you want to further develop its
capabilities or seamlessly integrate it into your existing applications, the flexibility of this project allows for
diverse use cases. My motivation for creating this project-turned-library stems from addressing specific requirements
within my organization, and I invite you to leverage it for your own purposes.

# Key Features:

* Utilizes the Paramiko library for SSH connections, providing a sample password-based implementation (check main.py for
  an example).
* Incorporates PyYAML for parsing the server_config.yaml file, which outlines server details, mount points, processes,
  and alarm configurations.

```yaml
#server_config.yaml
servers:
  - name: server-1
    address: hostname
    username: username
    password: password
    mount_points:
      - /
      - /var
    processes:
      - process_name_1.ksh
      - process_name_2.sh
    alarms:
      memory:
        - "memory < 5.gb"
        - "memory < 10.gb"
      disk_space:
        - "/ < 20.gb"
        - "/var < 50.gb"

  - name: server-2
    address: hostname
    username: username
    password: password
    mount_points:
      - /
    processes:
      - process_name_1.ksh
      - process_name_2.sh
    alarms:
      memory:
        - "memory < 10.gb"
      disk_space:
        - "/ < 40.gb"
```

```shell
#create and activate the virtualenv
pip install -r requirements.txt
```