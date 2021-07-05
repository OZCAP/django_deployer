## Django Deployer
A one hit tool for preparing a Django project to a server with Gunicorn and Nginx.

When hosting multiple sites on a vps or server, it can be a bit cumbersome and slow to add and configure each site seperately.
This tool makes it easy to launch multiple sites onto one server, including setting specific user permissions for an added layer of security.

### Prerequisites
This tool relies on having a Django project ready to go, with an exclusive virtual environment with all of the modules needed for the project, ready installed to it as well as Gunicorn. So to sumarise, in your virtual environment you will need:
*Django
*Gunicorn

### Usage
Clone the repository to a directory of choice onto your server.
```
git clone https://github.com/OZCAP/django_deployer/ [path/to/your/chosen/directory]
```

Run deploy_project.py to enter the wizard
```
sudo python3 ./deploy_project.py
```

Follow the prompts on the wizard and the rest will be configured for you.
