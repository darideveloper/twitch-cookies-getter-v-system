import os
from time import sleep
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
    
    def __init__ (self, project:str):
        """ Init class
        
        Args:
            project (str): project name to update cookies
        """
        
        print (f"\nStarting cookies getter for project: {project.upper()}...\n")
        
        self.project = project
        
        # Connect to api
        self.api = Api(project)
        
        # Scraping variables
        self.selectors = {
            "login_user": '#login-username',
            "login_password": '#password-input',
            "login_button": '[data-a-target="passport-login-button"]',
            "login_token": '.Layout-sc-1xcs6mc-0.bnzvpg.tw-form-group',
            "login_error": ".server-message-alert",
            "twitch_logo": '[data-a-target="home-link"]'
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
        
    def __login__ (self, user_name:str, user_password:str):
        """ Login to twitch with user and password

        Args:
            user_name (str): twitch user name
            user_password (str): twitch password
        """
        
        # Delete old cookies 
        self.set_page (self.pages["login"])
        self.delete_cookies ()
        
        # Login form
        self.set_page (self.pages["login"])
        self.send_data (self.selectors["login_user"], user_name)
        self.send_data (self.selectors["login_password"], user_password)
        self.click (self.selectors["login_button"])
        sleep (5)
        
        # Catch token validation
        token_text = self.get_text (self.selectors["login_token"])
        if "token" in token_text.lower():
            print ("\tToken validation required")
            return False
        
        # Catch invalid credentials
        error_text = self.get_text (self.selectors["login_error"])
        if error_text.lower():
            print ("\tInvalid credentials")
            return False
        
        # Validate home page
        logo = self.count_elems (self.selectors["twitch_logo"])
        if not logo:
            print ("\tLogin failed. Unknown error")
            return False
        
        return True
    
    def __update_cookies__ (self, user_name:str):
        """ Get current cookies and sent to backend 
        
        Args:
            user_name (str): user name
        """
        
        print ("\tUpdating cookies...")
    
        # Get twitch cookies
        cookies = self.get_cookies ()
        cookies_formatted = {
            "cookies": cookies
        }
        res = self.api.post_cookies (user_name, cookies_formatted)
        
        if res["status"] == "ok":
            print ("\tCookies updated")
        else:
            print (f"\tError updating cookies: {res['message']}")
            
    def auto_run (self):
        """ Get users and passwords from api and login to twitch
        """
        
        # Get and loop users
        users = self.api.get_users ()
        for user in users:
            
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
                continue
            
            logged = self.__login__ (user_name, user_password)
            if not logged:
                continue
            
            self.__update_cookies__ (user_name)