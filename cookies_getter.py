import os
from time import sleep
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper
from api import Api

# Environment variables
load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")
DEBUG_USERS = os.getenv ("DEBUG_USERS").split (",")
if DEBUG_USERS == [""]:
    DEBUG_USERS = []
LOGS_PREFIX = "(getter)"

class CookiesGetter (ChromDevWrapper):
    """ Login to twitch with user and password, get cookies and
    save them in backend
    """
    
    def __init__ (self, project:str):
        """ Init class
        
        Args:
            project (str): project name to update cookies
        """
        
        print (f"\n{LOGS_PREFIX} Starting cookies getter for project: {project.upper()}...\n")
        
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
        proxy_host = proxy["host"]
        proxy_port = proxy["port"]
        
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
            print (f"\t{LOGS_PREFIX} Token validation required")
            return False
        
        # Catch invalid credentials
        error_text = self.get_text (self.selectors["login_error"])
        if error_text.lower():
            print (f"\t{LOGS_PREFIX} Invalid credentials")
            return False
        
        # Validate home page
        logo = self.count_elems (self.selectors["twitch_logo"])
        if not logo:
            print (f"\t{LOGS_PREFIX}Login failed. Unknown error")
            return False
        
        return True
    
    def __update_cookies__ (self, user_data:str):
        """ Get current cookies and sent to backend 
        
        Args:
            user_data (dict): id, username and password of user
        """
        
        print (f"\t{LOGS_PREFIX} Updating cookies...")
    
        # Get twitch cookies
        cookies = self.get_cookies ()
        res = self.api.update_cookies (user_data, cookies)
        
        if res["status"] == "ok":
            print (f"\t{LOGS_PREFIX} Cookies updated")
        else:
            print (f"\t{LOGS_PREFIX} Error updating cookies: {res['message']}")
            
    def auto_run (self):
        """ Get users and passwords from api and login to twitch
        """
        
        # Get and loop users
        users = self.api.get_users ()        
        for user in users:
            
            user_name = user["user"]
            user_password = user["password"]
            print (f"{LOGS_PREFIX} User: {user_name}")
            
            # Skip users in debug mode
            if DEBUG_USERS and user_name not in DEBUG_USERS:
                continue
            
            # Skip users with empty password
            if user_password.strip() == "":
                print (f"\t{LOGS_PREFIX} Empty password, user skipped")
                continue
            
            # Login
            print (f"\t{LOGS_PREFIX} Login...")
            self.__start_chrome__ ()
            
            proxy_valid = self.valid_proxy ()
            if not proxy_valid:
                continue
            
            logged = self.__login__ (user_name, user_password)
            if not logged:
                continue
            
            self.__update_cookies__ (user)