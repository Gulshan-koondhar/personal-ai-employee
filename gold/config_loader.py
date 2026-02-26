"""
Configuration Loader for AI Employee

This module handles loading configuration from environment variables
and .env files securely.
"""
import os
from pathlib import Path
from typing import Optional

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, manually load the .env file
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    if key not in os.environ:  # Only set if not already set
                        os.environ[key] = value

def get_env_variable(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable with optional default.

    Args:
        var_name: Name of the environment variable
        default: Default value if variable is not set

    Returns:
        Value of the environment variable or default
    """
    return os.environ.get(var_name, default)

def get_required_env_variable(var_name: str) -> str:
    """
    Get a required environment variable.

    Args:
        var_name: Name of the environment variable

    Returns:
        Value of the environment variable

    Raises:
        ValueError: If the environment variable is not set
    """
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Required environment variable '{var_name}' is not set")
    return value

def check_credentials_configuration() -> dict:
    """
    Check which credentials are configured and which are missing.

    Returns:
        Dictionary with configuration status
    """
    status = {
        'email_configured': bool(get_env_variable('EMAIL_API_KEY')),
        'odoo_configured': bool(get_env_variable('ODOO_API_KEY')),
        'facebook_configured': bool(get_env_variable('FACEBOOK_API_KEY')),
        'twitter_configured': bool(get_env_variable('TWITTER_API_KEY')),
        'linkedin_configured': bool(get_env_variable('LINKEDIN_API_KEY')),
        'gmail_configured': bool(get_env_variable('GMAIL_CLIENT_ID')),
        'vault_path': get_env_variable('VAULT_PATH', './AI_Employee_Vault')
    }

    return status

def validate_configured_services() -> list:
    """
    Validate which services are properly configured.

    Returns:
        List of configured services
    """
    configured_services = []

    if get_env_variable('EMAIL_API_KEY'):
        configured_services.append('Email Service')

    if get_env_variable('ODOO_API_KEY'):
        configured_services.append('Odoo Accounting')

    if get_env_variable('FACEBOOK_API_KEY'):
        configured_services.append('Facebook Integration')

    if get_env_variable('TWITTER_API_KEY'):
        configured_services.append('Twitter/X Integration')

    if get_env_variable('LINKEDIN_API_KEY'):
        configured_services.append('LinkedIn Integration')

    if get_env_variable('GMAIL_CLIENT_ID'):
        configured_services.append('Gmail Integration')

    return configured_services

def print_configuration_status():
    """Print the current configuration status."""
    print("=== AI Employee Configuration Status ===")

    status = check_credentials_configuration()
    configured_services = validate_configured_services()

    print(f"Vault Path: {status['vault_path']}")
    print(f"Email Service: {'[YES] Configured' if status['email_configured'] else '[NO] Not configured'}")
    print(f"Odoo Accounting: {'[YES] Configured' if status['odoo_configured'] else '[NO] Not configured'}")
    print(f"Facebook: {'[YES] Configured' if status['facebook_configured'] else '[NO] Not configured'}")
    print(f"Twitter/X: {'[YES] Configured' if status['twitter_configured'] else '[NO] Not configured'}")
    print(f"LinkedIn: {'[YES] Configured' if status['linkedin_configured'] else '[NO] Not configured'}")
    print(f"Gmail: {'[YES] Configured' if status['gmail_configured'] else '[NO] Not configured'}")

    print(f"\nActive Services: {len(configured_services)}")
    for service in configured_services:
        print(f"  - {service}")

    if not configured_services:
        print("\n[WARN] Warning: No external services are configured.")
        print("Please set up credentials in the .env file for desired functionality.")
    else:
        print(f"\n[SUCCESS] {len(configured_services)} service(s) ready for use!")

if __name__ == "__main__":
    print_configuration_status()