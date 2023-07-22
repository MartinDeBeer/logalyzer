import logging
import re
from pathlib import Path
import json


class WebLogFile:

	def determineFormat(path):
        # Regular expressions to identify patterns in log entries
		w3c_pattern = r'^\S+\s+\S+\s+\S+\s+\[\S+\s+\S+\]\s+.*'
		syslog_pattern = r"^\S+\s+\S+\s+\S+\s+\S+\s+\S+\[\d+\]\:.*"

		with open(path, "r") as logFile:
			for line in logFile:
				if re.match(w3c_pattern, line.strip()):
					return "W3C"

				if re.match(syslog_pattern, line.strip()):
					return "syslog"

		return None

	def apacheAccessLog(path): # This will be used when we see that we have a syslog for a webserver
		jsonText = "{"
		with open(path, "r") as logFile:
			for line in logFile:
				'''
					The info we need:
						IP address
						Date
						Site
						Request
						Referrer
				'''
				# Here we need to set all the patterns for the lines
				ip_pattern = r"\d+\.\d+\.\d+\.\d+" # First thing we need to do is get the IP address
				date_pattern = r"(?<=\[)\S+(?=\s)" # First thing we need to do is get the IP address
				site_pattern = r"(?<=\s)(\w+\.\S+[^;]|-)(?=\s)" # We get the site name
				request_pattern = r"((?<=\")(.*?)(?=\"))\" (\d{3}) (\d+)" # We get the site name
				referrer_pattern = r"(?<=\")(\S+)(?=\")" # We get the site name
				site_match = re.search(site_pattern, line.strip())
				date_match = re.search(date_pattern, line.strip())
				ip_match = re.search(ip_pattern, line.strip())
				request_match = re.search(request_pattern, line.strip())
				referrer_match = re.search(referrer_pattern, line.strip())
				if ip_match:
					ip_address = ip_match.group()
					jsonText += f"ip_address: \"{ip_address}\", "
				if date_match:
					date = date_match.group()
					jsonText += f"date: \"{date}\", "
				if site_match:
					site = site_match.group()
					jsonText += f"site: \"{site}\", "
				if request_match:
					request = request_match.group()
					request = request.replace("\"", "")
					jsonText += f"request: \"{request}\", "
				if referrer_match:
					referrer = referrer_match.group()
					jsonText += f"referrer: \"{referrer}\"" + "}"

				print(jsonText)

	def apacheErrorLog(path):
		jsonText = "{"
		date_pattern = r"(?<=\[).*(?=\])" # Get the date
		event_pattern = r"(?<=\:)(\s.*)" # Get the event
		date_match = re.search(date_pattern, path.strip())
		event_match = re.search(event_pattern, path.strip())
		if date_match:
			# Format the time so it is always in the format (YYYY-MM-DD)
			timestamp = date_match.group()
			jsonText += f"timestamp: \"{timestamp.strip()}\", "
		if event_match:
			event = event_match.group()
			jsonText += f"event: \"{event.strip()}\"" + "}"


		print(jsonText)

	def createErrorFile(log_line):
		'''
			This is going to take the output we get from the analyzer and put it into a file for the web interface
		'''
		with open("/var/www/logalyzer") as log_folder:
			pass




	def __init__(self, path):
		self.path = path
