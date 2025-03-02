import logging
import sys

# Define the logger
logger = logging.getLogger("email-analyzer")
logger.setLevel(logging.DEBUG) 

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)  
#file_handler = logging.FileHandler("logs/email_analyzer.log") 

# Set logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
#file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
#logger.addHandler(file_handler)

# Prevent duplicate logs if running in some environments
logger.propagate = False
