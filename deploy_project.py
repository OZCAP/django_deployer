#! /usr/bin/python3
import os

# User inputs
proj = input("\nProject name[myproject]:  ")
group = (input("\nUser group for web access(default: webapps): ") or "webapps")
domain = input("\nDomain name for site[example.com]: ")
root = input("\nFull path to project directory[/myproject]: ")
if root[-1] == '/': root = root[:-1]
env = input("\nFull path to virtual environment[/myproject/env]: ")
if env[-1] == '/': env = env[:-1]

# Create user group (if not already made) and add user to that group
print(f"\n...\n...\nAdding user {proj} to group {group}...")

os.system(f'sudo groupadd --system {group}')
stream  = os.popen(f'sudo useradd --system --gid {group} --shell /bin/bash --home {root} {proj}')
response = stream.read()
if response == "":
    print("User added successfully!")
else:
    print("User already exists. Exiting...")

print("\nSetting permissions...")
os.system(f'sudo chown {proj} {root}')

# Create a gunicorn service for the project
print("\nCreating custom service...")
try:
    with open('./templates/service_template', 'r') as f:
        text = f.read()
        service_contents = text.format(group=group, root=root, proj=proj, env=env)
        f.close()
    with open(f'/etc/systemd/system/{proj}.gunicorn.service', 'w') as f:
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

    with open(f'/etc/systemd/system/{proj}.gunicorn.socket', 'w') as f:
        f.write(socket_contents)
        f.close()
        print("socket file created!")
except:
    print("Error creating socket file.")

# Start/Enable the socket connection
print("Enabling service socket...")
os.system('sudo systemctl daemon-reload')
stream = os.popen(f'sudo systemctl start {proj}.gunicorn.socket')
response = stream.read()
if response == "":
    print("Socket started!")
else:
    print("Socket start error. Exiting...")
    exit()
os.system('sudo systemctl daemon-reload')
stream = os.popen(f'sudo systemctl enable {proj}.gunicorn.socket')
response = stream.read()
if response == "":
    print("Socket enabled!")
else:
    print("Socket enable error. Exiting...")
    exit()

# Reload services
print("\nReloading daemon...")
os.system(f'sudo systemctl daemon-reload && sudo systemctl restart {proj}.gunicorn')

# Set ownership of the project contents to specified user
print("\nSetting permissions...")
os.system(f'sudo chown {proj} {root}/*')

# Create the configuration for the website
print("\nCreating nginx website configuration...")
try:
    with open('./templates/config_template', 'r') as f:
        text = f.read()
        config_contents = text.format(domain=domain, root=root, proj=proj)
        f.close()
    with open(f'/etc/nginx/sites-available/{proj}', 'w') as f:
        f.write(config_contents)
        f.close()
        print("Config file created!")
except:
    print("\nConfig creation failed. Exiting")
    exit()

# Add site to sites-enabled
print("\nCreating site link...")
os.system(f'sudo ln -s /etc/nginx/sites-available/{proj} /etc/nginx/sites-enabled')

# Refresh Nginx
print("\nRefreshing ngix configuration...")
os.system('sudo systemctl restart nginx')

print("\nAll tasks complete.")
input("Press any key to continue...")
exit()