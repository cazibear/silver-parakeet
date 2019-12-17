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
			stations = self.calling_stations(departure["service_timetable"]["id"])

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
			for s in stations:
				if s["name"] == departure["destination_name"]:
					print("->", s["time"], "-", s["name"])
				elif s["name"] == json["station_name"]:
					print("<-", s["time"], "-", json["station_name"])
				else:
					print("  ", s["time"], "-", s["name"])
			print()  # newline
		if not found:
			print()

	def calling_stations(self, endpoint):
		"""Gets the calling stations from the API's provided endpoint"""
		response = get(endpoint)  # no need to add credentials as they should be there
		if response.status_code == 200:
			# pprint(response.json())
			output = []
			first = True
			for stop in response.json()["stops"]:
				if first:
					first = False
				else:
					if type(stop["aimed_arrival_time"]) is None:
						continue
					data = {
						"time": stop["aimed_arrival_time"],
						"name": stop["station_name"]
					}
					output.append(data)
			return output
		else:
			return "There was an error with the timetable id"
