import json
import os
from decouple import config

import twilio.base.exceptions
from twilio.rest import Client

class ContactList(list):
    pass


class Contact:
    contact_list = ContactList()

    def __init__(self, contact_info, append=True):
        self._info: dict = contact_info
        if append:
            self.contact_list.append(self)

    def __repr__(self):
        return f"{self._info}"

    @property
    def info(self) -> dict:
        return self._info

    @info.setter
    def info(self, value: dict):
        self._name = value

    def text_contact(self, body):
        # todo add max number
        try:
            print(f"f: +19513836718\nt: {self.info['phone']}\nb: {body}")
        except KeyError:
            raise KeyError("No phone in spreadsheet\nPlease ensure phone column is named 'phone'")
        # message = self.client.messages.create(
        #     body='Hi there',
        #     from_='+19513836718',
        #     to=f"+1{self._phone}"
        # )

    def list(self) -> ContactList:
        return self.contact_list


class UserSettings:
    twilio_account_sid = None
    twilio_auth_token = None

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
        print(os.getenv('TWILIO_ACCOUNT_SID', None))
        cls.twilio_account_sid = config('TWILIO_ACCOUNT_SID')
        cls.twilio_auth_token = config('TWILIO_AUTH_TOKEN')
        # test

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
            with open('enviroment.env', 'w', encoding='utf-8') as file:
                file.write(value)
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
            os.environ["TWILIO_ACCOUNT_SID"] = value
            cls.twilio_auth_token = value



