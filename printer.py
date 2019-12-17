import pprint
from datetime import datetime
from requests import get


class Printer:
	def print_station(self, json):
		# pprint.pprint(json)
		print("Station:", json["member"][0]["name"])
		print("-" * (9 + len(json["member"][0]["name"])))
		print("Station code:", json["member"][0]["station_code"])
		print("TIPLOC code:", json["member"][0]["tiploc_code"])
		print("Latitude:", json["member"][0]["latitude"])
		print("Longitude:", json["member"][0]["longitude"])
		print()

	def print_station_departures(self, json, search=False):
		# pprint.pprint(json)
		found = False

		print("Station:", json["station_name"])
		print("=" * (9 + len(json["station_name"])))
		print()
		if not json["departures"]["all"]:
			print(json)
			return

		for departure in json["departures"]["all"]:
			if type(search) != bool:
				if not any([str(search).lower() in s["name"].lower() for s in stations]):
					found = True
					continue

			# get time till departure
			now = datetime.now()
			depart = datetime.strptime(departure["aimed_departure_time"], "%H:%M")
			depart = depart.replace(year=now.year, month=now.month, day=now.day)
			eta = int((depart - now).total_seconds() / 60)
			# nicely format it into 'x hours and y minute(s)' as required
			if eta == 1:
				eta = "1 minute"
			elif eta <= 60:
				eta = "{} minutes".format(eta)
			else:
				hours = int(eta / 60)
				minutes = eta % 60
				if hours == 1:
					if minutes == 1:
						eta = "{} hour and {} minute".format(hours, minutes)
					else:
						eta = "{} hour and {} minutes".format(hours, minutes)
				else:
					if minutes == 1:
						eta = "{} hours and {} minute".format(hours, minutes)
					else:
						eta = "{} hours and {} minutes".format(hours, minutes)


			# print the departure
			print("Destination:", departure["destination_name"])
			print("-" * (13 + len(departure["destination_name"])))
			print("Leaving at:", departure["aimed_departure_time"], "in", eta)
			print("Platform:", departure["platform"])
			print("Calling at:")

			# printing stations
			for stations in departure["stations"]:
				if stations["name"] == departure["destination_name"]:
					print(stations["time"], "-", stations["name"])
				elif stations["name"] == json["station_name"]:
					print(stations["time"], "-", json["station_name"])
				else:
					print(stations["time"], "-", stations["name"])
			print()  # newline
		if not found:
			print()
