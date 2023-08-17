import os
from dotenv import load_dotenv
from cookies_getter import CookiesGetter
load_dotenv ()

PROJECTS = os.getenv ("PROJECTS").split (",")
if PROJECTS == [""]:
    PROJECTS = []

for project in PROJECTS:
    cookies_getter = CookiesGetter (project)
    cookies_getter.auto_run ()