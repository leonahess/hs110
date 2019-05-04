from influxdb import InfluxDBClient
import config

client = InfluxDBClient(host=config.influx_ip, port=config.influx_port, database=config.influx_database)

print("< connected to influx!")
print("> checking if database '{}' exists ...".format(config.influx_database))

database_list = client.get_list_database()
database_exists = False

for s in range(0, len(database_list)):
    if database_list[s]['name'] == config.influx_database:
        database_exists = True

        print("< database '{}' exists".format(config.influx_database))

if not database_exists:
    print("< database '{}' does not exist!".format(config.influx_database))
    print("> creating database '{}' ...".format(config.influx_database))

    client.create_database(config.influx_database)

    print("< created database '{}'!".format(config.influx_database))
