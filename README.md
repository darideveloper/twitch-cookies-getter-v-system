<div><a href='https://github.com/tree/master/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/tree/master.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/twitch-cookies-getter/blob/master/logo.png?raw=true' alt='Twitch Cookies Getter' height='80px'/>

# Twitch Cookies Getter

Project to login with twitch using proxies, who get the cookies and save it to a private backend service,

Project type: **client**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#relatedprojects'>Related Projects</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#deploy'>Deploy</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://requests.readthedocs.io/en/latest/' target='_blank'> <img src='https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png' alt='Requests' title='Requests' height='50px'/> </a><a href='https://github.com/marty90/PyChromeDevTools' target='_blank'> <img src='https://cdn.svgporn.com/logos/chrome.svg' alt='PyChromeDevTools' title='PyChromeDevTools' height='50px'/> </a></div>

# Related projects

<div align='center'><a href='https://github.com/darideveloper/comunidad-mc' target='_blank'> <img src='https://github.com/darideveloper/comunidad-mc/blob/master/app/static/app/imgs/logo_white.png?raw=true' alt='Comunidad MC' title='Comunidad MC' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-viwer-bot' target='_blank'> <img src='https://github.com/darideveloper/twitch-viwer-bot/blob/master/logo.png?raw=true' alt='Twitch Viwer Bot' title='Twitch Viwer Bot' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-cheer-bot' target='_blank'> <img src='https://github.com/darideveloper/twitch-cheer-bot/blob/master/logo.png?raw=true' alt='Twitch Cheer Bot' title='Twitch Cheer Bot' height='50px'/> </a></div>

# Media

![start-browser](https://github.com/darideveloper/twitch-cookies-getter/blob/master/screenshots/start-browser.png?raw=true)

![validate-proxy](https://github.com/darideveloper/twitch-cookies-getter/blob/master/screenshots/validate-proxy.png?raw=true)

![update-cookies](https://github.com/darideveloper/twitch-cookies-getter/blob/master/screenshots/update-cookies.png?raw=true)

![login](https://github.com/darideveloper/twitch-cookies-getter/blob/master/screenshots/login.png?raw=true)

# Details

## Workflow

1. The project get the data (twitch credentials and proxies) from the backend service.
2. For each user (with username and password), the program opens a chrome window, with proxy already setup.
3. The page [ipinfo.io/json](http://ipinfo.io/json) its loaded to validate the proxy.
4. If the proxy its working, it loads the page [witch.tv/login](https://www.twitch.tv/login),
5. delete the old cookies,
6. reload the page
7. and login with user and password.
8. If any error happen while login, the program catch and show it. 
9. If the login was successful, it get the cookies, and finally
10. Submit the cookies and reactivate the user in the backend.

# Deploy

* [X] Open chrome with proxies
* [X] Login with credentials
* [X] Update cookies in backend

