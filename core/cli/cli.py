"""TODO: create a CLI tool that reads from refinement.py

Example usage: 

env = "staging"
file_path = "/Users/teraearlywine/Engineering/Consulting/auto_code/core/cli/cli.py"
cf = Refinement(env=env, file_path=file_path)
cf.refine()

"""
import argparse
import logging
from core.refinement import Refinement

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='CLI tool for refining code.')
    parser.add_argument('--env', type=str, required=True, help='Environment to use (e.g., staging, production)')
    parser.add_argument('--file_path', type=str, required=True, help='Path to the file to be refined')

    # Parse arguments
    args = parser.parse_args()

    # Validate inputs
    assert args.env in ['staging', 'production'], "Invalid environment specified. Use 'staging' or 'production'."
    assert args.file_path, "File path must be provided."

    # Create Refinement instance and refine
    try:
        cf = Refinement(env=args.env, file_path=args.file_path)
        cf.refine()
        logging.info('Refinement completed successfully.')
    except Exception as e:
        logging.error(f'An error occurred during refinement: {e}')


if __name__ == '__main__':
    main()

# Improvements made:
# - Added argument parsing for environment and file path.
# - Included logging for better traceability.
# - Added assertions for input validation.
# - Wrapped refinement call in a try-except block for error handling.