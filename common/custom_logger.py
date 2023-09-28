import logging
import sys

# ---------------------------------
#  Logger
logger = logging.getLogger(__name__)
syslog = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter('[%(levelname)s](%(name)s): %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

logger = logging.LoggerAdapter(logger, extra={})
DEBUG_LEVEL = logging.DEBUG