from requests import get
from sys import argv
from printer import Printer
import json
import configparser
import os
from datetime import datetime

API_BASE = "http://transportapi.com/v3/uk/"
CREDENTIALS = {}


def log(string):
	f = open("log.txt", "a")
	f.write(string + "\n")
	f.close()


def get_codes(full_name):
	"""Gets a stations (CRS and TIPLOC codes) from its full name and returns None if not found
	found"""
	data = station_info(full_name)
	if not data.get("error", False):
		crs = data["member"][0]["station_code"]
		tiploc = data["member"][0]["tiploc_code"]
		return crs, tiploc
	else:
		return None


def station_info(name):
	query = {
		"query": name,
		"type": "train_station"
	}
	url = API_BASE + "places.json"
	query.update(CREDENTIALS)

	response = get(url, params=query)  # get request on the api endpoint
	log("Request made to " + response.url + " Status code: " + str(response.status_code))
	if response.status_code == 200:
		return response.json()
	else:
		error = {
			"error:": True,
			"error_from": "Function: station_info",
			"status_code": response.status_code,
			"content": response.content
		}
		return error


def station_departures(name):
	if len(name) > 3:
		print("get_crs")
		name = get_codes(name)[0]

	url = API_BASE + "train/station/{}/live.json".format(name)
	response = get(url, params=CREDENTIALS)
	log("Request made to " + response.url + " Status code: " + str(response.status_code))

	if response.status_code == 200:
		data = response.json()
		for departure in data["departures"]["all"]:
			departure["stations"] = calling_at(departure["service_timetable"]["id"])
		return data
	else:
		error = {
			"error:": True,
			"error_from": "Function: station_departures",
			"status_code": response.status_code,
			"content": response.content
		}
		return error


def load_config():
	config = configparser.ConfigParser()
	try:
		config.read("config.txt")
		app_id = config.get("credentials", "id")
		app_key = config.get("credentials", "key")

		CREDENTIALS["app_id"] = app_id
		CREDENTIALS["app_key"] = app_key
	except configparser.NoSectionError:
		print("Config file does not have the required sections.")
		exit(1)
	except KeyError:
		print("Config file does not have the required values.")
		exit(1)
	except FileNotFoundError:
		print("There is no config file to get credentials from.")
		exit(1)


def main():
	load_config()
	p = Printer()
	if len(argv) > 2:
		method = argv[1]
		if method == "info":
			data = station_info(argv[2])
			p.print_station(data)
		elif method == "departures":
			data = station_departures(argv[2])
			if len(argv) == 4:
				p.print_station_departures(data, search=argv[3])
			else:
				p.print_station_departures(data)
		elif method == "load":
			file_path = argv[2]  # gets the file path from second argument
			# get the directory not the file name (will only work on unix filesystems for now)
			directory = file_path.split("/")[1]
			data = json.load(open(file_path))

			if directory == "info":
				p.print_station(data)
			elif directory == "departures":
				p.print_station_departures(data)
			else:
				print("Function not recognised")
		elif method == "save":
			"""
			argv[2] = the method to run
			argv[3] = the parameter for selected method
			"""
			# -- getting the data to save
			func = argv[2]
			if func == "info":
				data = station_info(argv[3])
			elif func == "departures":
				data = station_departures(argv[3])
			else:
				print("Function not recognised")
				return

			# -- saving the data to file for later
			dt = datetime.today()
			file_path = os.path.join("saved", argv[2], argv[3])
			# file_path = os.path.abspath(file_path)
			file_name = dt.strftime("%Y-%m-%d_%H-%M") + ".json"
			print("Saving to", file_path)
			# create the file and folders as might be required
			if not os.path.exists(file_path):
				os.makedirs(file_path)
				f = open(os.path.join(file_path, file_name), "x")
			else:
				f = open(os.path.join(file_path, file_name), "w")
			json.dump(data, f)
			f.close()
	else:
		# codes = get_codes("wolverhampton")
		# print(codes, type(codes))
		time = datetime.today()
		print(time.strftime("%Y-%m-%d_%H-%M"))


def calling_at(endpoint):
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


if __name__ == "__main__":
	main()
