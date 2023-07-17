import logging
import re
from pathlib import Path
import json


class LogFile:

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

	def convertSyslog(path):
		jsonText = "{"
		with open(path, "r") as logFile:
			for line in logFile:
				# Here we need to set all the patterns for the lines
				ip_pattern = r"\d+\.\d+\.\d+\.\d+" # First thing we need to do is get the IP address
				date_pattern = r"(?:(?<=[^\d+\.])|^)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s/]+(?:\d{2})[\s/]+(?:\S+)[\:\d{2}:\d{2}]" # Get the date
				processID_pattern = r"(\S+\[\d+\])" # Get the name and ID of the process
				event_pattern = r"(?<=\:)(\s.*)" # Get the event
				ip_match = re.search(ip_pattern, line.strip())
				date_match = re.search(date_pattern, line.strip())
				process_match = re.search(processID_pattern, line.strip())
				event_match = re.search(event_pattern, line.strip())
				if ip_match:
					ip_address = ip_match.group()
					jsonText += f"ip_address: \"{ip_address}\""
				if date_match:
					# Format the time so it is always in the format (YYYY-MM-DD)
					timestamp = date_match.group()
					jsonText += f", timestamp: \"{timestamp.strip()}\""
				if process_match:
					process = process_match.group()
					jsonText += f", process: \"{process.strip()}\""
				if event_match:
					event = event_match.group()
					jsonText += f", event: \"{event.strip()}\"" + "}"


				print(jsonText)

	def convertW3C(path):
		jsonText = "{"
		with open(path, "r") as logFile:
			for line in logFile:
				# Here we need to set all the patterns for the lines
				ip_pattern = r"\d+\.\d+\.\d+\.\d+" # First thing we need to do is get the IP address
				date_pattern = r"(?:(?<=[^\d+\.])|^)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s/]+(?:\d{2})[\s/]+(?:\S+)[\:\d{2}:\d{2}]" # Get the date
				processID_pattern = r"(\S+\[\d+\])" # Get the name and ID of the process
				event_pattern = r"(?<=\:)(\s.*)" # Get the event
				ip_match = re.search(ip_pattern, line.strip())
				date_match = re.search(date_pattern, line.strip())
				process_match = re.search(processID_pattern, line.strip())
				event_match = re.search(event_pattern, line.strip())
				if ip_match:
					ip_address = ip_match.group()
					jsonText += f"ip_address: \"{ip_address}\""
				if date_match:
					# Format the time so it is always in the format (YYYY-MM-DD)
					timestamp = date_match.group()
					jsonText += f", timestamp: \"{timestamp.strip()}\""
				if process_match:
					process = process_match.group()
					jsonText += f", process: \"{process.strip()}\""
				if event_match:
					event = event_match.group()
					jsonText += f", event: \"{event.strip()}\"" + "}"


				print(jsonText)




	def __init__(self, path):
		self.path = path
