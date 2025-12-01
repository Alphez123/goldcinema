# 📧 Email Configuration Setup Guide - Gold Cinema

## Overview
This guide will help you set up email functionality for:
- ✅ **User Registration Confirmation** - Welcome emails sent to new users
- ✅ **Password Reset** - Secure password reset via email

---

## 🔐 Step 1: Get Your SMTP Credentials

### For Gmail Users:

1. **Enable 2-Factor Authentication** (if not already enabled)
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or Other)
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### For Other Email Providers:

- **Outlook/Hotmail**: Use `smtp.office365.com` on port `587`
- **Yahoo**: Use `smtp.mail.yahoo.com` on port `587`
- **Custom Domain**: Contact your hosting provider for SMTP details

---

## 🛠️ Step 2: Configure Environment Variables

### Option A: Using .env File (Recommended for Local Development)

1. **Install python-decouple** (if not already installed):
   ```bash
   pip install python-decouple
   ```

2. **Create a `.env` file** in your project root:
   ```bash
   # Navigate to project root
   cd c:\Users\alpha\Downloads\goldcinema-main
   
   # Create .env file
   type nul > .env
   ```

3. **Add your credentials to `.env`**:
   ```env
   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_USE_SSL=False
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   DEFAULT_FROM_EMAIL=Gold Cinema <your-email@gmail.com>
   ```

4. **Update settings.py** to use decouple:
   ```python
   from decouple import config
   
   EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
   EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
   ```

### Option B: Using Windows Environment Variables

1. **Open System Properties**:
   - Press `Win + R`
   - Type `sysdm.cpl` and press Enter
   - Go to "Advanced" tab → "Environment Variables"

2. **Add User Variables**:
   - Click "New" under "User variables"
   - Add each variable:
     ```
     Variable name: EMAIL_HOST_USER
     Variable value: your-email@gmail.com
     
     Variable name: EMAIL_HOST_PASSWORD
     Variable value: your-16-char-app-password
     
     Variable name: EMAIL_HOST
     Variable value: smtp.gmail.com
     
     Variable name: EMAIL_PORT
     Variable value: 587
     ```

3. **Restart your terminal/IDE** for changes to take effect

### Option C: Direct Configuration (NOT RECOMMENDED - Security Risk!)

**⚠️ WARNING: Only use this for testing! Never commit passwords to Git!**

Edit `backend/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password-here'
```

---

## 🧪 Step 3: Test Email Functionality

### Test Registration Email:

1. **Start your server**:
   ```bash
   python manage.py runserver
   ```

2. **Register a new account**:
   - Go to: http://localhost:8000/users/register/
   - Fill in the form with a **real email address**
   - Submit the form

3. **Check your email**:
   - You should receive a welcome email within 1-2 minutes
   - Check spam folder if not in inbox

### Test Password Reset:

1. **Go to login page**:
   - Visit: http://localhost:8000/users/login/

2. **Click "Forgot Password?"**

3. **Enter your email** and submit

4. **Check your email** for the reset link

5. **Click the link** and set a new password

---

## 🐛 Troubleshooting

### Error: "SMTPAuthenticationError"
**Solution**: 
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that the email and password are correct

### Error: "Connection refused" or "Timeout"
**Solution**:
- Check your internet connection
- Verify firewall isn't blocking port 587
- Try using port 465 with `EMAIL_USE_SSL=True` instead

### Emails not arriving:
**Solution**:
- Check spam/junk folder
- Verify the recipient email is correct
- Check Django console for error messages
- Test with a different email provider

### Error: "Environment variable not found"
**Solution**:
- Restart your terminal/IDE after setting environment variables
- Verify variable names match exactly (case-sensitive)
- Use Option A (.env file) for easier management

---

## 📝 Email Templates

The system includes two beautiful HTML email templates:

### 1. **Registration Welcome Email**
- Professional Gold Cinema branding
- Welcome message with user's name
- List of features they can use
- Call-to-action button to start booking
- Contact information

### 2. **Password Reset Email**
- Security warning if user didn't request reset
- Secure reset link with token
- 24-hour expiration notice
- Clear instructions
- Professional styling

---

## 🔒 Security Best Practices

1. **Never commit `.env` file to Git**:
   ```bash
   # Add to .gitignore
   echo .env >> .gitignore
   ```

2. **Use App Passwords** instead of account passwords

3. **Rotate passwords** regularly

4. **Monitor email sending** for unusual activity

5. **Set rate limits** to prevent abuse (optional)

---

## 🚀 Production Deployment

### For Render/Heroku:

1. **Set environment variables** in dashboard:
   - Go to your app settings
   - Add each EMAIL_* variable
   - Restart the app

### For PythonAnywhere:

1. **Go to Web tab**
2. **Scroll to Environment Variables**
3. **Add each variable**
4. **Reload web app**

---

## 📊 Features Implemented

✅ Registration confirmation emails with HTML templates  
✅ Password reset via email with secure tokens  
✅ Token expiration (24 hours)  
✅ Beautiful, responsive email designs  
✅ Fallback to plain text for email clients without HTML support  
✅ Error handling and logging  
✅ Security best practices  
✅ User-friendly error messages  

---

## 🎯 Next Steps

1. **Test thoroughly** with different email providers
2. **Customize email templates** in `users/email_utils.py`
3. **Add email verification** (optional - require users to verify email before login)
4. **Set up email logging** for production monitoring
5. **Configure SPF/DKIM** records for better deliverability (production)

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Django console for error messages
3. Verify all environment variables are set correctly
4. Test with a simple email first

---

**Status**: ✅ **FULLY IMPLEMENTED AND READY TO USE**

**Last Updated**: December 1, 2025
