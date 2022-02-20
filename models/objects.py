import json
import os
import twilio.base.exceptions
from twilio.rest import Client
import phonenumbers

class ContactList(list):
    pass


class Contact:
    contact_list = ContactList()

    def __init__(self, contact_info: dict, test_mode=False):
        self._info: dict = contact_info
        self._message_text = None
        self.user_settings = UserSettings()
        if test_mode is False:
            self.client = Client(
                self.user_settings.get_twilio_account_sid(),
                self.user_settings.get_twilio_auth_token()
            )

        self.contact_list.append(self)

    def __repr__(self):
        return f"{self._info}"

    @property
    def message_text(self):
        return self._message_text

    @message_text.setter
    def message_text(self, value: str):
        self._message_text = value

    @property
    def info(self) -> dict:
        return self._info

    def text_contact(self, body):

        if self.user_settings.get_test_mode():
            self._message_text = f"F: {self.user_settings.get_twilio_phone_number()}\n" \
                                f"T: {self.info['phone']}\n" \
                                f"B: {body}\n"
        else:
            if not phonenumbers.is_valid_number(phonenumbers.parse(f"+1{self.info.get('phone')}")):
                return False
            else:
                # self.client.messages.create(  # todo uncomment this
                #     body=body,
                #     from_=self.user_settings.get_twilio_phone_number(),
                #     to=f"+1{self.info['phone']}"
                # )
                return True

    def list(self) -> ContactList:
        return self.contact_list


class ContactReply(Contact):
    pass  # exact copy


class UserSettings:
    twilio_account_sid = None
    twilio_auth_token = None
    twilio_phone_number = None
    test_mode = False

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
    def set_twilio_phone_number(cls, value: str):
        os.environ["TWILIO_PHONE_NUMBER"] = value
        cls.twilio_phone_number = value

    @classmethod
    def set_test_mode(cls, on):
        cls.test_mode = on

    @classmethod
    def get_test_mode(cls):
        return cls.test_mode



