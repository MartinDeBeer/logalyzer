from weblog import WebLogFile
import subprocess


# This will collect the log files for PHP errors

def get_php_errors():
    try:
        with subprocess.Popen(["tail", "-n", "0", "-F", "/var/log/php/www-error_log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                line = line.strip()
                WebLogFile.apacheErrorLog(line)
    except KeyboardInterrupt:
        print("Log analyzer stopped.")