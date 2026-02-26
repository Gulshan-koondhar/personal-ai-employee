# AI Employee Configuration Guide

This guide explains how to configure your AI Employee with external services and credentials.

## Environment Variables Setup

The AI Employee uses environment variables for all sensitive configuration. These are loaded from the `.env` file.

### Required Setup Steps

1. **Create your `.env` file** (already created in this project)
2. **Replace placeholder values** with your actual credentials
3. **Ensure `.env` is in `.gitignore`** (already set up)
4. **Install required dependencies**: `pip install python-dotenv`

## Required Credentials by Service

### Email Service
- `EMAIL_API_KEY`: Your email service API key (SendGrid, Mailgun, etc.)
- `EMAIL_SMTP_USERNAME`: Your email address
- `EMAIL_SMTP_PASSWORD`: Your email app password
- `SMTP_HOST`: SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP port (e.g., 587)
- `EMAIL_FROM_ADDRESS`: The email address to send from

### Odoo Accounting System
- `ODOO_URL`: Your Odoo instance URL (self-hosted)
- `ODOO_API_KEY`: Your Odoo API key
- `ODOO_DATABASE`: Your Odoo database name

### Social Media APIs
- `FACEBOOK_API_KEY`: Facebook Page Access Token
- `FACEBOOK_PAGE_ID`: Your Facebook Page ID
- `INSTAGRAM_API_KEY`: Instagram API credentials
- `INSTAGRAM_ACCOUNT_ID`: Your Instagram account ID
- `TWITTER_API_KEY`: Twitter API Key
- `TWITTER_API_SECRET`: Twitter API Secret
- `TWITTER_ACCESS_TOKEN`: Twitter Access Token
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter Access Token Secret
- `LINKEDIN_API_KEY`: LinkedIn API credentials
- `LINKEDIN_ACCESS_TOKEN`: LinkedIn Access token

### Gmail Integration
- `GMAIL_CLIENT_ID`: Google OAuth Client ID
- `GMAIL_CLIENT_SECRET`: Google OAuth Client Secret
- `GMAIL_REFRESH_TOKEN`: Gmail refresh token

### WhatsApp Integration
- `WHATSAPP_API_KEY`: WhatsApp Business API key
- `WHATSAPP_PHONE_NUMBER_ID`: WhatsApp phone number ID

## Security Best Practices

### 🔐 Credential Security
- **Never commit `.env` to version control** (already added to `.gitignore`)
- **Use strong, unique passwords** for each service
- **Rotate credentials regularly** (recommended monthly)
- **Use application-specific passwords** rather than account passwords when available

### 🔍 Permission Limits
- **Grant minimum required permissions** to each API key
- **Use dedicated service accounts** rather than personal accounts
- **Enable 2FA** on all accounts where possible
- **Monitor API usage** regularly

### 🛡️ Environment Setup
```bash
# Install required dependencies
pip install python-dotenv

# Create a backup of your .env file in a secure location
cp .env /secure/location/.env.backup
```

## Testing Configuration

To check your current configuration:

```bash
python config_loader.py
```

This will show you which services are properly configured and which ones are missing credentials.

## Development vs Production

### Development
- Use test credentials and sandbox environments when available
- Enable detailed logging for debugging
- Use separate test accounts for each service

### Production
- Use production credentials only
- Disable detailed error logging
- Implement proper error handling
- Set up monitoring and alerts

## Troubleshooting

### Common Issues
1. **Environment variables not loading**: Make sure the `.env` file is in the correct location
2. **API errors**: Check that credentials are correct and have proper permissions
3. **Connection timeouts**: Verify network connectivity and API endpoint URLs
4. **Permission errors**: Confirm that API keys have required scopes/permissions

### Security Checks
- Verify that sensitive files are not accessible publicly
- Check that logs don't contain sensitive information
- Confirm that `.env` is properly excluded from git