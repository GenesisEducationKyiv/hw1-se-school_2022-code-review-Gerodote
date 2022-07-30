# for_course
## How to run this?
1.  Install python3 , desirable versions are 3.10.x or 3.9.x . Depending on your system:
      
      1.  Windows, find [installer](https://www.python.org/downloads/windows/) or install [`scoop`](https://scoop.sh/), then `scoop install python` .
      2.  Linux, check is it exist in repositories of your distributive
      3.  MacOs, idk google it. Maybe in [brew](https://formulae.brew.sh/formula/python@3.9) ?
      4.  Android? [Termux](https://github.com/termux/termux-app/releases) is your best friend.
2.  `git clone https://github.com/Gerodote/for_course.git` . If you haven't, install git. Again, in which way to do so depends on what's your system is 
3.  `python -mpip install --upgrade pip` depending on your system, the beginning of the command can be `python3`
3.  `pip install -r requirements.txt` or try `pip install aiofiles binance-connector fastapi uvicorn google-auth-httplib2 google-auth-oauthlib google-api-python-client python-multipart`. If your CPU has ARM architecture, strongly recommend type `pip install wheel` before this command. Especially, if you run in [termux](https://github.com/termux/termux-app/releases)
4.  Setup gmail account as in guide below.
5.  Run HTTP API server: `uvicorn main:API --host 0.0.0.0 --port 80` 
6.  Check how it works with localhost:80/docs

## How to setup a gmail account to send emails?
### Main idea:
  1. Get OAuth2 key ( aka client_secret.json ) from Google Cloud Console
  2. Initialize gmail service by running either `uvicorn main:API`, or `python mail_handler.py` for getting appropriate token with appropriate permissions for using the gmail. 
  3. If you don't delete the `token_gmail_v1.pickle`, you can run this app again without doing what's below.
 
### Let's start:
1. Create a Google account
2. Go to console.cloud.google.com
3. Create an project:

![image](https://user-images.githubusercontent.com/58738099/181842338-c9328c53-d950-46d9-b5bc-dbabb8a01300.png)
![image](https://user-images.githubusercontent.com/58738099/181842652-04f0a47c-bfeb-4f2c-a2be-44b9f04671dc.png)

4. Create OAuth app:

![image](https://user-images.githubusercontent.com/58738099/181843113-2f532ad3-6e96-4501-a628-8b2206856860.png)
![image](https://user-images.githubusercontent.com/58738099/181843160-2524ec35-a8fb-4789-85e8-81a3575400c6.png)
![image](https://user-images.githubusercontent.com/58738099/181843324-48c45d06-4747-46da-9ec2-fad4212c0815.png)
![image](https://user-images.githubusercontent.com/58738099/181843463-84b835dd-42fc-4e0c-802b-6ce5bd50617f.png)
![image](https://user-images.githubusercontent.com/58738099/181843691-b7895133-a2d2-4ec7-af2f-c129aeb9bf77.png)
![image](https://user-images.githubusercontent.com/58738099/181843873-868dc1a9-54eb-470a-b471-c1acfa9cc778.png)
![image](https://user-images.githubusercontent.com/58738099/181843927-fa6a4c9d-94fc-493d-9a65-a016c39a3146.png)
![image](https://user-images.githubusercontent.com/58738099/181843990-752c529d-ed21-4deb-a55e-dba85d8bc646.png)

5. Enable Gmail API:

![image](https://user-images.githubusercontent.com/58738099/181844070-992d1cdf-d517-4e1b-a067-bc7fbb6e1966.png)
![image](https://user-images.githubusercontent.com/58738099/181844178-a2f5a9ee-b4cf-4da3-8938-fc4c85bb2841.png)
![image](https://user-images.githubusercontent.com/58738099/181844222-df4c7a1f-3616-4dfa-bc0f-14384f4ec8c3.png)

6. Add appropriate scope for your OAuth app:

![image](https://user-images.githubusercontent.com/58738099/181844402-0c9272c1-8110-49ca-87bd-181ac5831c17.png)
![image](https://user-images.githubusercontent.com/58738099/181844461-76a3b2bd-c142-4fab-b849-5e22855f7584.png)
![image](https://user-images.githubusercontent.com/58738099/181844501-7f50406b-0b18-4623-a5fc-ff72c4fad973.png)
![image](https://user-images.githubusercontent.com/58738099/181844723-bbf62ebe-e782-471d-af82-5b61d64d3548.png)
![image](https://user-images.githubusercontent.com/58738099/181844902-e5cfe7a1-5dda-4dc8-a6ca-22db7c3df040.png)
![image](https://user-images.githubusercontent.com/58738099/181844926-1c9782d0-54f0-4642-9aed-e43ec421b4dd.png)
![image](https://user-images.githubusercontent.com/58738099/181844979-27bd2a77-08c2-4cbf-b050-9ffddcd7646c.png)
![image](https://user-images.githubusercontent.com/58738099/181845025-ec25439a-ce6d-4912-bb2f-fa7d8c5145b2.png)

7. Create OAuth2 credentials for getting client_secret.json

![image](https://user-images.githubusercontent.com/58738099/181845230-9efb5050-c741-4a7f-aa3c-a3582483738f.png)
![image](https://user-images.githubusercontent.com/58738099/181845258-5b19e09b-513b-4a36-889b-0b8715202470.png)
![image](https://user-images.githubusercontent.com/58738099/181845460-c12fc348-7e05-40b2-8cef-349cbbfc7be8.png)
![image](https://user-images.githubusercontent.com/58738099/181845490-7da61ed7-9dd2-4808-ad2b-443a58489793.png)

8. Copy the file you got to the project folder and rename it to "client_secret.json".
9. Launch mail_handler.py or just run server: `python ./mail_handler.py` or `uvicorn main:API` or something like this, depending on your own system.
10. Either automatically your browser shall be opened, or open the link you shall get in console. Then allow it to work:

![image](https://user-images.githubusercontent.com/58738099/181846595-e376d429-6494-47f1-b039-1771a6d6ff7b.png)
![image](https://user-images.githubusercontent.com/58738099/181846631-1ba9851f-5f36-419f-921a-95164db00e42.png)
![image](https://user-images.githubusercontent.com/58738099/181846696-94044428-1153-412b-8843-5b325539b41c.png)
![image](https://user-images.githubusercontent.com/58738099/181846738-d664b6e9-d340-4e86-8a18-ed1f793a0aa1.png)
![image](https://user-images.githubusercontent.com/58738099/181846850-5e49c811-62e0-4796-9271-d351f2a68ccf.png)

11. If you need, try to re-run `mail_handler.py` or server.

