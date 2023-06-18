import os
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper
from api import Api

# Environment variables
load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")

class CookiesGetter (ChromDevWrapper):
    """ Login to twitch with user and password, get cookies and
    save them in backend
    """
    
    def __init__ (self):
        """ Init class
        """
        
        # Connect to api
        self.api = Api()
        
        # Scraping variables
        self.selectors = {
                
        }
        
        self.pages = {
            "login": "https://www.twitch.tv/login"
        }
        
    def __start_chrome__ (self):
        """ Start chrome with proxy, killing old chrome instances
        """
        
        # Get proxy
        proxy = self.api.get_proxy ()
        proxy_host = proxy["proxy"]["host"]
        proxy_port = proxy["proxy"]["port"]
        
        # Connect to chrome
        super().__init__(
            proxy_host=proxy_host, 
            proxy_port=proxy_port, 
        )
    
    def auto_run (self):
        """ Get users and passwords from api and login to twitch
        """
        
        # Get and loop users
        users = self.api.get_users ()
        for user in users["users"]:
            
            user_name = user["username"]
            user_password = user["password"]
            print (f"User: {user_name}")            
            
            # Skip users with empty password
            if user_password.strip() == "":
                print ("\tEmpty password, user skipped")
                continue
            
            # Login
            print ("\tLogin...")
            self.__start_chrome__ ()
            proxy_valid = self.valid_proxy ()
            if not proxy_valid:
                print (f"proxy not working: {self.proxy}")
                continue
            self.__login__ (user_name, user_password)
                
            
            
        
        
        
        

        
cookies_getter = CookiesGetter ()
cookies_getter.auto_run ()