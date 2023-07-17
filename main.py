from logfile import LogFile


print(LogFile.determineFormat("syslog.log"))
LogFile.convertSyslog("syslog.log")
LogFile.convertW3C("w3clog.log")