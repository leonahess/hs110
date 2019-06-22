from influxdb import InfluxDBClient
import config

client = InfluxDBClient(host=config.influx_ip, port=config.influx_port, database=config.influx_database)

print("< connected to influx!")
print("> checking if database '{}' exists ...".format(config.influx_database))

database_list = client.get_list_database()
smarthome_exists = False
retention_exits = False

for s in range(0, len(database_list)):
    if database_list[s]['name'] == 'smarthome':
        smarthome_exists = True
        print("< database 'smarthome' exists")
        print("> checking retention policy")


if not smarthome_exists:

    print("< database 'smarthome' does not exist!")
    print("> creating database 'smarthome' ...")

    client.create_database('smarthome')

    print("< created database 'smarthome'!")

retention_list = client.get_list_retention_policies("smarthome")
database_list = client.get_list_database()

for s in range(0, len(database_list):
    if database_list[s]['name'] == 'smarthome':
        for rp in range(0, len(retention_list)):
            if retention_list[rp]['name'] == config.influx_retention_policy:
                print("< correct retention policy exists")
                retention_exits = True


if not retention_exits:
    print("< correct retention policy does not exists")
    print("> creating correct retention policy")

    client.create_retention_policy(config.influx_retention_policy, config.influx_retention_policy, 1,
                                   database="smarthome")

    print("< created correct retention policy")
