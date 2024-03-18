import json
from abc import ABC, abstractmethod

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
        self.cookies = []

    def auth(self) -> bool:
        url = f"http://{self.ip}/cgi-bin/luci/"
        data = {'luci_username': self.username, 'luci_password': self.password}
        response = requests.post(url, data=data)
        self.cookies = response.cookies
        if self.cookies:
            return True
        else:
            return False

    def get_sms(self, name: str) -> list:
        url = f"http://{self.ip}/cgi-bin/luci/admin/network/modem/modem1/sms?method=list"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code == 200:
            data = json.loads(response.text)
            messages = [message["storage"]["content"]["text"] for message in data["result"][name]]
        else:
            messages = []
        return messages
