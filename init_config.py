import os
from configparser import ConfigParser

app_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_root, 'config/config.ini')

config = ConfigParser()

print(
    "Hello! I am your interactive guide to setting up the website-metrics application.\n" +
    "Please follow the prompts to configure Postgres and Kafka.\n" +
    "Let's start with Postgres:\n"
)
username = input("Postgres username: ")
password = input("Postgres password: ")
host = input("Postgres hostname or IP: ")
port = input("Postgres port: ")
database = input("Postgres database: ")

print("\nGreat! Now, on to Kafka:\n")

servers = input("Kafka server(s) with port(s): ")
topic = input("Kafka topic (e.g. website-metrics): ")

config['POSTGRES'] = {'user': username,
                    'password': password,
                    'host': host,
                    'port': port,
                    'database': database}

config['KAFKA'] = {'servers': servers,
                    'topic': topic}

with open(config_path, 'w') as configfile:
    config.write(configfile)

print(
    "\nExcellent! Finally, please download your Kafka certificate files \n" +
    "and place them in website-metrics/config/certs/\n" +
    "\nThe following files are needed: ca.pem, service.cert, service.key\n"
)

while True:
    completed = input("Has this been completed? (y/n): ")
    if completed.lower() in ('y', 'yes'):
        print("\nFantastic! You can now start using these awesome tools.")
        print("If you ever wish to reconfigure, run this utility again.")
        break
    elif completed.lower() in ('n', 'no'):
        print("No worries! Let me know when it's done.")
        continue
    else:
        print("Hmm... I didn't quite understand that. Let's try again.")
        continue

