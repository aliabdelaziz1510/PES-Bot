import logging
from datetime import datetime, timedelta
from pytz import timezone


def _logger():
  # Create a logger object with the name of the script
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)

  # Create a file handler and a stream handler
  fh = logging.FileHandler("logger.txt", "a")
  sh = logging.StreamHandler()


  def timetz(*args):
    return datetime.now(tz).timetuple()

  tz = timezone('Africa/Cairo') # UTC, Asia/Shanghai, Europe/Berlin

  logging.Formatter.converter = timetz

  # Set the logging format
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  
  fh.setFormatter(formatter)
  sh.setFormatter(formatter)

  # Add the handlers to the logger object (only if they are not already added)
  if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(sh)

  return logger


if __name__ == "__main__":
  _logger()
