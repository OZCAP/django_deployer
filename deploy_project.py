#! /usr/bin/python3
import os

# User inputs
proj = input("\nProject name[myproject]: ")
group = (input("\nUser group for web access(default: webapps): ") or "webapps")
domain = input("\nDomain name for site[example.com]: ")
root = input("\nFull path to project directory[/myproject]: ")
if root[-1] == '/': root = root[:-1]
env = input("\nPath to python environment[/myproject/env]: ")
if env[-1] == '/': env = env[:-1]

# Create user group (if not already made) and add user to that group
print("\n...\n...\nAdding user {} to group {}...".format(proj, 'webapps'))
os.system('sudo groupadd --system {}'.format(group))
stream  = os.popen('sudo useradd --system --gid webapps --shell /bin/bash --home {} {}'.format(root, proj))
response = stream.read()
if response == "":
    print("User added successfully!")
else:
    print("User add error. Exiting...")
    exit()

# Create a gunicorn service for the project
print("\nCreating custom service...")
try:
    with open('./templates/service_template', 'r') as f:
        text = f.read()
        service_contents = text.format(group=group, root=root, proj=proj, env=env)
        f.close()
    with open('/etc/systemd/system/{}.gunicorn.service'.format(proj), 'w') as f:
        f.write(service_contents)
        f.close()
        print("Service created! ")
except:
    print("\nService creation failed. Exiting.")
    exit()

# Create a socket file for the application
print("\nGenerating socket file...")
try:
    with open('./templates/socket_template', 'r') as f:
        text = f.read()
        socket_contents = text.format(proj=proj, root=root)
        f.close()

    with open('/etc/systemd/system/{}.gunicorn.socket'.format(proj), 'w') as f:
        f.write(socket_contents)
        f.close()
        print("socket file created!")
except:
    print("Error creating socket file.")

# Start/Enable the socket connection
print("Enabling service socket...")
stream = os.popen('sudo systemctl start {}.gunicorn.socket'.format(proj))
response = stream.read()
if response == "":
    print("Socket started!")
else:
    print("Socket start error. Exiting...")
    exit()
stream = os.popen('sudo systemctl enable {}.gunicorn.socket'.format(proj))
response = stream.read()
if response == "":
    print("Socket enabled!")
else:
    print("Socket enable error. Exiting...")
    exit()

# Reload services
print("\nReloading daemon...")
os.system('sudo systemctl daemon-reload && sudo systemctl restart {}.gunicorn'.format(proj))

# Set ownership of the project folder to the specified user
print("\nSetting permissions...")
os.system('sudo chown {} {}'.format(proj, root))

# Create the configuration for the website
print("\nCreating nginx website configuration...")
try:
    with open('./templates/config_template', 'r') as f:
        text = f.read()
        config_contents = text.format(domain=domain, root=root, proj=proj)
        f.close()
    with open('/etc/nginx/sites-available/{}'.format(proj), 'w') as f:
        f.write(config_contents)
        f.close()
        print("Config file created!")
except:
    print("\nConfig creation failed. Exiting")
    exit()

# Add site to sites-enabled
print("\nCreating site link...")
os.system('sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled'.format(proj))

# Refresh Nginx
print("\nRefreshing ngix configuration...")
os.system('sudo systemctl restart nginx')

print("\nAll tasks complete.")
input("Press any key to continue...")
exit()