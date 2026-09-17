import logging 
import os 
import sys
from datetime import datetime

log_file = f"{datetime.now().strftime('%m__%d__%Y__%H__%M__%S')}.log"

logs_path = os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path, exist_ok=True)
log_file_path = os.path.join(logs_path,log_file)

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Expose a module-level logger instance for convenience
logger = logging.getLogger("networksequrity")