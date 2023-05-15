from flask import Flask, render_template, request
import pandas as pd
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read the uploaded Excel file
        file = request.files['file']
        df = pd.read_excel(file)

        # Extract the column names and data
        columns = df.columns.tolist()
        data = df.values.tolist()

        subject = request.form['subject']
        sender_email = request.form['sender_email']
        recipient_email = request.form['recipient_email']

        # Format the data as a string
        formatted_data = '\n'.join(['\t'.join(map(str, row)) for row in data])

        return render_template('index.html', columns=columns, data=data, subject=subject, sender_email=sender_email, recipient_email=recipient_email, formatted_data=formatted_data)

    return render_template('index.html')

@app.route('/send-mail', methods=['POST'])
def send_mail():
    subject = request.form['subject']
    sender_email = request.form['sender_email']
    recipient_email = request.form['recipient_email']
    formatted_data = request.form['formatted_data']

    # Prepare the email content
    email_content = f"Subject: {subject}\nFrom: {sender_email}\nTo: {recipient_email}\n\n{formatted_data}"

    # Use Sendmail to send the email
    try:
        sendmail = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE)
        sendmail.communicate(email_content.encode('utf-8'))
        sendmail.wait()
        message = "Email sent successfully!"
    except Exception as e:
        message = f"Failed to send email: {str(e)}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run()
