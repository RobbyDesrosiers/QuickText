import twilio.base.exceptions
from twilio.rest import Client

class ContactList(list):
    pass


class Contact:
    contact_list = ContactList()
    account_sid = ""
    auth_token = ""
    try:
        client = Client(account_sid, auth_token)
    except twilio.base.exceptions.TwilioException:
        print("input creds")

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