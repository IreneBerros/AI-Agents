import os 
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from src.graph_runner import run_email_analysis
from src.core.logger import logger

def main():
    logger.info("Pipeline execution started")
    email_text = input("Enter email text: ")
    result = run_email_analysis(email_text)
    logger.info(f"Response:{result}")

if __name__ == "__main__":
    main()