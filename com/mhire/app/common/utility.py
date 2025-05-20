import uuid
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def generate_request_id(key):
    """
    Generate a unique request ID based on the provided key
    
    Args:
        key (str): A string key to generate the UUID from
        
    Returns:
        str: A formatted request ID
    """
    request_id = f"REQ-{uuid.uuid5(uuid.NAMESPACE_DNS, key)}"
    return request_id

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, creating it if necessary
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logging.info(f"Created directory: {directory_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {directory_path}: {str(e)}")
        return False

def get_timestamp():
    """
    Get current timestamp in a formatted string
    
    Returns:
        str: Formatted timestamp string
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_filename(prefix, extension):
    """
    Generate a unique filename with timestamp
    
    Args:
        prefix (str): Prefix for the filename
        extension (str): File extension (without dot)
        
    Returns:
        str: Generated filename
    """
    timestamp = get_timestamp()
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def validate_file_path(file_path, allowed_extensions=None):
    """
    Validate if a file path exists and has an allowed extension
    
    Args:
        file_path (str): Path to the file
        allowed_extensions (list): List of allowed file extensions
        
    Returns:
        bool: True if file is valid
    """
    if not os.path.exists(file_path):
        logging.error(f"File does not exist: {file_path}")
        return False
        
    if allowed_extensions:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower().lstrip('.')
        if ext not in allowed_extensions:
            logging.error(f"Invalid file extension: {ext}. Allowed: {allowed_extensions}")
            return False
            
    return True