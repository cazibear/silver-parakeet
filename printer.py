import pprint
from requests import get


class Printer:
	def print_station(self, json):
		print("Station:", json["member"][0]["name"])
		print("-" * (9 + len(json["member"][0]["name"])))
		print("Station code:", json["member"][0]["station_code"])
		print("TIPLOC code:", json["member"][0]["tiploc_code"])
		print("Latitude:", json["member"][0]["latitude"])
		print("Longitude:", json["member"][0]["longitude"])
		print()

	def print_station_departures(self, json, search=False):
		# pprint.pprint(json)
		print("Station:", json["station_name"] + "\n" + "=" * (9 + len(json["station_name"])))
		print()
		print("Departures:\n" + "-" * 14)
		for departure in json["departures"]["all"]:
			stations = self.calling_stations(departure["service_timetable"]["id"])
			if search is not False and \
				(search != departure["destination_name"] or list(filter(lambda x: search in x, stations))):
				# if searching and (neither departure matches or one of the stops does)
				continue
			else:
				# otherwise print the departure
				print("Destination:", departure["destination_name"])
				print("-" * (13 + len(departure["destination_name"])))
				print("Leaving at:", departure["aimed_departure_time"], "on", "platform", departure["platform"])
				print("Calling at:")
				for s in stations:
					print(s)
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
					pair = " - ".join([stop["aimed_arrival_time"], stop["station_name"]])
					# time - station
					output.append(pair)
			return output
		else:
			return "There was an error with the timetable id"
