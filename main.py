import re
from flask import Flask, request, jsonify
from validate_email import validate_email
from phonenumbers import parse, is_valid_number, PhoneNumberType
import datetime

app = Flask(__name__)

email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

@app.route('/validate_email', methods=['GET'])
def validateEmail():
    try:
        email = request.args.get('email')
        email_status = None
        request_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if email:
            email = email.strip().lower()

        if email:
            if validate_email(email):
                email_status = 'valid'
            else:
                email_status = 'invalid'
        else:
            email_status = 'not provided'

        return jsonify({
            'emailAddress': email,
            'emailStatus': email_status,
            'requestTime': request_time
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/validate_phone', methods=['GET'])
def validatePhone():
    try:
        phone = request.args.get('phone')
        country_code = request.args.get('country_code')
        phone_status = None
        request_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if phone:
            phone = re.sub(r'[^\d+]', '', phone)

        if phone and country_code:
            parsed_phone = parse(phone, country_code)
            if is_valid_number(parsed_phone):
                phone_status = 'valid'
            else:
                phone_status = 'invalid'
        else:
            phone_status = 'not provided'

        return jsonify({
            'countryCode': country_code,
            'phoneNumber': phone,
            'phoneStatus': phone_status,
            'requestTime': request_time
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)