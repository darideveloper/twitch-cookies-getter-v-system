import os
import requests
from dotenv import load_dotenv

API_HOST = os.getenv("API_HOST")
TOKEN = os.getenv("TOKEN")

class Api ():

    def __requests_url__(self, endpoint: str) -> requests.get:
        """ Request data from specific endpoint and and quit if error happens

        Args:
            endpoint (str): endpoint to request, like "users" or "settings"

        Returns:
            requests.get: response of requests to the endpoint
        """

        # Request data to specific url
        url = f"{API_HOST}/{endpoint}/?token={TOKEN}"
        res = requests.get(url)

        if res.status_code == 200:
            return res
        else:
            print("Error requesting data from API. Check your token.")
            quit()

    def get_proxy (self) -> dict:
        """ get a random proxy from the API

        Returns:
            dict: proxy data (host and port)
            
            Example:
            
            {
                "proxy": {
                    "host": "0.0.0.0",
                    "port": 80,
                }
            }
        """
        
        # Get data from api
        res = self.__requests_url__("proxy")
        return res.json()
    
    def get_users (self) -> dict:
        """ users and passwords from the API

        Returns:
            dict: proxy data (host and port)
            
            Example:
            
            {
                "users": [
                    {
                        "username": "sample user",
                        "password": "sample password",
                    }
                    ...
                ]
            }
        """
        
        # Get data from api
        res = self.__requests_url__("users")
        return res.json()

if __name__ == "__main__":
    api = Api()
    data = api.get_users ()
    print (data)