import os

basedir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(basedir, '.env')

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

uri = input("Kafka URI (server:port): ")
topic = input("Kafka topic (e.g. website-metrics): ")

print("\nNow let's configure website checker parameters:\n")

website = input("URL of website to check: ")
interval = input("Time interval in seconds: ")
pattern = input("Regex pattern to look for (optional): ")

with open(dotenv_path, 'w') as f:
    f.write('POSTGRES_USER=' + username + '\n')
    f.write('POSTGRES_PASSWORD=' + password + '\n')
    f.write('POSTGRES_HOST=' + host + '\n')
    f.write('POSTGRES_PORT=' + port + '\n')
    f.write('POSTGRES_DB=' + database + '\n')
    f.write('\n')
    f.write('KAFKA_URI=' + uri + '\n')
    f.write('KAFKA_TOPIC=' + topic + '\n')
    f.write('\n')
    f.write('WEBSITE_URL=' + website + '\n')
    f.write('TIME_INTERVAL=' + interval + '\n')
    f.write('REGEX_PATTERN=' + pattern + '\n')

print(
    "\nExcellent! Finally, please download your Kafka certificate files \n" +
    "and place them in website-metrics/certs/\n" +
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

