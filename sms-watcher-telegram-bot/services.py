import json
from abc import ABC, abstractmethod
from typing import Union

import requests


class LteRouter(ABC):
    @abstractmethod
    def auth(self) -> bool:
        """Authorization via POST request and saving Cookies"""
        pass

    @abstractmethod
    def get_sms(self, name: str) -> list:
        """Getting SMS messages"""
        pass


class KroksRouter(LteRouter):
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        self.cookies = None

    def auth(self) -> Union[dict, None]:
        session = requests.Session()
        url = f"http://{self.ip}/cgi-bin/luci/"
        session.post(url, data={'luci_username': self.username, 'luci_password': self.password})
        self.cookies = session.cookies
        if self.cookies:
            return self.cookies.get_dict()
        else:
            return None

    def get_sms(self, name: str) -> dict:
        url = f"http://{self.ip}/cgi-bin/luci/admin/network/modem/modem1/sms?method=list"
        if not self.cookies:
            self.auth()
        response = requests.get(url, cookies=self.cookies)
        if response.status_code == 200:
            try:
                data = json.loads(response.text)
                if data['result']:
                    messages = [message["storage"]["content"]["text"] for message in data["result"][name]]
                else:
                    messages = []
                result = {"status": True, "details": "", "messages": messages}
            except json.decoder.JSONDecodeError:
                result = {"status": False, "details": "JSONDecodeError", "messages": []}
        else:
            result = {"status": False, "details": f"Response code {response.status_code} received", "messages": []}
        return result
