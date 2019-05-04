from pyHS100 import SmartPlug
import datetime
import time
from app import client


class HS110:

    def __init__(self, ip):

        self.plug = SmartPlug(ip)
        self.name = self.plug.alias

        while True:
            self.today = datetime.date.today()

            try:
                self.write(self.read())
            except Exception as e:
                print("Current Stats Exception: {}".format(e))

            time.sleep(1)

    def read(self):
        year = self.today.year
        month = self.today.month

        realtime = self.plug.get_emeter_realtime()
        daily_avg = self.plug.get_emeter_daily(year, month)

        jsons = []
        x = 0

        for day in daily_avg:
            daytime = datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0)

            jsons.append({
                "measurement": "power",
                "tags": {
                    "name": self.name
                },
                "fields": {
                    "daily_average": daily_avg[day]
                },
                "time": daytime

            })

            x += 1

        jsons.append({
            "measurement": "power",
            "tags": {
                "name": self.name
            },
            "fields": {
                "milliwatt": realtime["power_mw"],
                "milliampere": realtime["current_ma"],
                "millivolt": realtime["voltage_mv"],
                "watthours": realtime["total_wh"]
            },
            "time": datetime.datetime.utcnow()
        })

        return jsons

    def write(self, jsons):

        try:
            client.write_points(jsons, protocol="json")
        except Exception as e:
            print("Write exception: {}".format(e))
