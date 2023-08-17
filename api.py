import os
import sys
import json
import random
import requests

API_HOST = os.getenv("API_HOST")
TOKEN = os.getenv("TOKEN")
TOKEN_WEBSHARE = os.getenv("TOKEN_WEBSHARE")

class Api ():
    
    def __init__ (self, project):
        """ Init class

        Args:
            project (str): project name to update cookies
        """
        
        self.project = project
        self.proxies = []
        
        # Get and validate token
        tokens_path = os.path.join (os.path.dirname (__file__), "tokens.json")
        with open (tokens_path, "r") as file:
            tokens = json.load (file)
            
        if project not in tokens:
            print (f"Error: token not found for project '{project}'")
            quit ()
        else:
            token = tokens[project]
            self.headers = {
                "token": token
            }
        
        # Load proxies
        self.__load_proxies__ ()

    def __load_proxies__ (self):
        """ Query proxies from the webshare api, and save them
        """
        
        # Get proxies
        res = requests.get (
            "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100", 
            headers = { 
                "Authorization": f"Token {TOKEN_WEBSHARE}"
            }
        )
        if res.status_code != 200:
            print (f"Error getting proxies: {res.status_code} - {res.text}")
            quit ()

        try:
            json_data = res.json ()
            self.proxies = json_data['results']
        except Exception as error:
            print (f"Error getting proxies: {error}")
            
            quit ()

    def get_proxy (self) -> dict:
        """ get a random proxy 

        Returns:
            dict: proxy data (host and port)
            
            Example:
            {
                "host": "0.0.0.0",
                "port": 80,
            }
        """
        
        # Get data from api
        proxy = random.choice (self.proxies)
        return {
            "host": proxy["proxy_address"],
            "port": proxy["port"],
        }
    
    def get_users (self) -> list:
        """ users and passwords from the API

        Returns:
            dict: user data (username and password)
            
            Example:
            [    
                {
                    "username": "sample 1 user",
                    "password": "sample 1 password",
                },
                {
                    "username": "sample 2 user",
                    "password": "sample 2 password",
                }
            ]

        """
        
        # Get data from api
        res = requests.get (
            f"{API_HOST}/{self.project}/bots/", 
            headers=self.headers
        )
        res.raise_for_status ()
        json = res.json ()
        
        # Validate response
        if json["status"] != "ok":
            print (f"Error getting users: {json['message']}")
            quit ()
        
        users = json["data"]
        
        # Formatd ata
        users = list(map (lambda user: {
            "username": user["user"],
            "password": user["password"],
        }, users))
        
        return users
    
    def post_cookies (self, user:str, cookies) -> dict:
        """ Update cookies of specific user

        Args:
            user (str): user name

        Returns:
            dict: response data from API
            
            Example:
            
            {
                "status": "ok",
                "message": "Cookies updated" 
            }
        """
        
        res = self.__requests_url__(f"update-cookies/{user}", method="post", json_data=cookies)
        return res.json()
        
if __name__ == "__main__":
    api = Api("viwers")
    proxy = api.get_proxy()
    users = api.get_users()
    
    print ()