import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
from werkzeug.middleware.proxy_fix import ProxyFix
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET",
                                "fallback-secret-key-for-development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS',
                                            'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL',
                                            'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER',
                                                   app.config['MAIL_USERNAME'])

# Recipients for contact form
app.config['CONTACT_RECIPIENTS'] = os.environ.get('CONTACT_RECIPIENTS',
                                                  '').split(',')
if not app.config['CONTACT_RECIPIENTS'] or app.config[
        'CONTACT_RECIPIENTS'] == ['']:
    app.config['CONTACT_RECIPIENTS'] = [app.config['MAIL_USERNAME']]

mail = Mail(app)


def is_valid_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_form_data(data):
    """Server-side form validation"""
    errors = []

    # Check required fields
    if not data.get('duration', '').strip():
        errors.append('Duration is required')
    elif data.get('duration') not in ['30 minutes', '60 minutes']:
        errors.append('Please select a valid duration')

    if not data.get('email', '').strip():
        errors.append('Email is required')
    elif not is_valid_email(data['email'].strip()):
        errors.append('Please enter a valid email address')

    if not data.get('description', '').strip():
        errors.append('Description is required')

    if not data.get('phone', '').strip():
        errors.append('Phone number is required')

    # Length validation
    if len(data.get('description', '')) > 2000:
        errors.append('Description must be less than 2000 characters')

    if len(data.get('phone', '')) > 20:
        errors.append('Phone number must be less than 20 characters')

    return errors


@app.route('/')
def index():
    """Display the main contact form"""
    return render_template('index.html')


@app.route('/wellnessreading', methods=['POST'])
def wellnessreading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Wellness Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.route('/customreading', methods=['POST'])
def customreading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Custom Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.route('/deityreading', methods=['POST'])
def deityreading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Deity Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.route('/jobreading', methods=['POST'])
def jobreading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Job Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.route('/moneyreading', methods=['POST'])
def moneyreading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Money Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.route('/lovereading', methods=['POST'])
def lovereading():
    """Handle contact form submission"""
    try:
        # Get form data
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone', '').strip()
        form_source = request.form.get('form_source', 'unknown-form').strip()

        # Validate form data
        errors = validate_form_data(request.form)

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        # Create email message
        email_subject = f"Love Reading Purchase - {duration} (from {form_source})"
        email_body = f"""
New contact form submission:

Form Source: {form_source}
Duration: {duration}
Email: {email}
Phone: {phone}

Description:
{description}

---
This message was sent via the contact form on your website.
        """.strip()

        # Send email
        msg = Message(subject=email_subject,
                      recipients=app.config['CONTACT_RECIPIENTS'],
                      body=email_body,
                      reply_to=email)

        mail.send(msg)

        app.logger.info(f"Contact form email sent successfully from {email}")
        flash('Thank you for your message! We\'ll get back to you soon.',
              'success')

    except Exception as e:
        app.logger.error(f"Error sending contact form email: {str(e)}")
        flash(
            'Sorry, there was an error sending your message. Please try again later.',
            'error')

    return redirect(url_for('personal'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/collective')
def collective():
    return render_template('collective.html')


@app.route('/personal')
def personal():
    return render_template('personal.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/lovepayment')
def lovepayment():
    return render_template('lovepayment.html')


@app.route('/moneypayment')
def moneypayment():
    return render_template('moneypayment.html')


@app.route('/deitypayment')
def deitypayment():
    return render_template('deitypayment.html')


@app.route('/jobpayment')
def jobpayment():
    return render_template('jobpayment.html')


@app.route('/wellnesspayment')
def wellnesspayment():
    return render_template('wellnesspayment.html')


@app.route('/custompayment')
def custompayment():
    return render_template('custompayment.html')
