import json
import os
import twilio.base.exceptions
from twilio.rest import Client
import phonenumbers

class ContactList(list):
    pass


class Contact:
    contact_list = ContactList()

    def __init__(self, contact_info, append=True):
        self._info: dict = contact_info
        self.user_settings = UserSettings()
        print(self.user_settings.get_twilio_phone_number())
        self.client = Client(
            self.user_settings.get_twilio_account_sid(),
            self.user_settings.get_twilio_auth_token()
        )
        if append:
            self.contact_list.append(self)

    def __repr__(self):
        return f"{self._info}"

    @property
    def info(self) -> dict:
        return self._info

    def text_contact(self, body):
        # todo add max number
        # todo make srue phone is valid
        try:
            print(f"f: +19513836718\nt: {self.info['phone']}\nb: {body}")
            message = self.client.messages.create(
                body='Hi there',
                from_=self.user_settings.get_twilio_phone_number(),
                to=f"+1{self._phone}"
            )
        except KeyError:
            raise KeyError("No phone in spreadsheet\nPlease ensure phone column is named 'phone'")

    def list(self) -> ContactList:
        return self.contact_list


class UserSettings:
    twilio_account_sid = None
    twilio_auth_token = None
    twilio_phone_number = None

    def __init__(self):
        self._settings = {
            "csvLocation": None,
            "csvLastModDate": None
        }
        self.load_all()

    def __setitem__(self, key, value):
        self._settings[key] = value

    def __getitem__(self, key):
        return self.settings[key]

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    def save(self):
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(self._settings, file)

    @classmethod
    def load_twilio_env_variables(cls):
        cls.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        cls.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        cls.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')


    def load_all(self):
        self.load_twilio_env_variables()

        with open('settings.json', 'r', encoding='utf-8') as file:
            try:
                contents = json.loads(file.read())
                self._settings = contents
                return contents
            except json.decoder.JSONDecodeError:
                print("No json obj: in class user - temp fix")

    @classmethod
    def get_twilio_account_sid(self):
        return self.twilio_account_sid

    @classmethod
    def set_twilio_account_sid(cls, value):
        EMPTY = ""
        if value is None or value is EMPTY:
            raise ValueError("Nonetype cannot be set")
        else:
            os.environ["TWILIO_ACCOUNT_SID"] = value
            cls.twilio_account_sid = value

    @classmethod
    def get_twilio_auth_token(cls):
        return cls.twilio_auth_token

    @classmethod
    def set_twilio_auth_token(cls, value):
        EMPTY = ""
        if value is None or value is EMPTY:
            raise ValueError("Nonetype cannot be set")
        else:
            os.environ["TWILIO_AUTH_TOKEN"] = value
            cls.twilio_auth_token = value

    @classmethod
    def get_twilio_phone_number(cls):
        return cls.twilio_phone_number

    @classmethod
    def set_twilio_phone_number(cls, value):
        # todo make better converter
        if len(value) == 10:
            value = f"+1{value}"
        if len(value) == 11:
            value = f"+{value}"

        value = f"+1{phonenumbers.parse(value).national_number}"

        os.environ["TWILIO_PHONE_NUMBER"] = value
        cls.twilio_phone_number = value



