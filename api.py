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
            self.api_token = tokens[project]
        
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

    def __requests_url__(self, endpoint:str, method:str="get", json_data:dict={}) -> requests.get:
        """ Request data from specific endpoint and and quit if error happens

        Args:
            endpoint (str): endpoint to request, like "users" or "settings"
            method (str, optional): request method, like "get" or "post". Defaults to "get".
            json_data (dict, optional): json data to send in post request. Defaults to {}.

        Returns:
            requests.get: response of requests to the endpoint
        """

        # Generate endpoint
        url = f"{API_HOST}/{self.project}/{endpoint}/?token={TOKEN}"
        
        # Submit request 
        if method == "get":
            res = requests.get(url)
        else:
            res = requests.post(url, json=json_data)

        if res.status_code == 200:
            return res
        else:
            print("Error requesting data from API. Check your token.")
            quit()

    def get_proxy (self) -> dict:
        """ get a random proxy 

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
        proxy = random.choice (self.proxies)
        return {
            "host": proxy["proxy_address"],
            "port": proxy["port"],
        }
    
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
        
        if self.project == "botcheers":
            res = self.__requests_url__("users")
            
            # Format response
            return res.json()["users"]
        else:
            res = self.__requests_url__("users")
            
            # Format response
            json = res.json()
            users = list(map(lambda user: user["fields"], json))
            users_formatted = list(map(lambda user: {
                "username": user["name"],
                "password": user["password"],
            }, users))
            
            return users_formatted
    
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
    
    print ()