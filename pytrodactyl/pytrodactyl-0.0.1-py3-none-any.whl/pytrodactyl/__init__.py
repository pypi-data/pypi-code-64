import requests
import json
import sys


class Application:
	def __init__(self, url, api_key):
		self.url = url
		self.api_key = api_key
		self.headers = {
		  'Accept': 'Application/vnd.pterodactyl.v1+json',
		  'Content-Type': 'application/json',
		  'Authorization': f'Bearer {self.api_key}'
		}
		response = requests.get(url=self.url + "/api/application/servers", headers=self.headers)
		if response.status_code != 200:
			print(response.json())
			sys.exit()

	def _api_request(self, url):
		response = requests.get(url=url, headers=self.headers)
		return response.json()

	def show_all_servers(self):
		meta_data = self._api_request(url=f"{self.url}/api/application/servers")
		b = []
		for i in range(meta_data['meta']['pagination']['total_pages']):
			b.append(self._api_request(url=f"{self.url}/api/application/servers?page={i}"))
		return b
