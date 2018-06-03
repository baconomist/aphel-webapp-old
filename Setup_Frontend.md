## SETUP ##

	[GO TO BIT BUCKET](https://bitbucket.org/Thetoxickiller/webapp/downloads/)
	and download the server code.

## DEPENDENCIES ##
- python **3.6**
- flask(python library)
- jsonpickle(python library)



## RUNNING THE SERVER ##
- Navigate to the root directory of the project and, assuming you have
python installed, just double click main.py
- Go to your browser and in the address bar put: 127.0.0.1

#### Note: ####
- When actually running the server also run backup.py which will backup the databases and images every 12 hours

## BOOTSTRAP STUDIO ##
When using bootstrap studio go to **export -->
export settings --> advanced options --> export script** and choose the export_script.exe located in the "**export__script/dist/**" folder in the root project directory.

Then click "**save**" to save the export script option.

Now you can click **export whenever you want to** make changes with the server.

#### Note: ####
The server **automatically** updates **exported data**. This means there is **no need** to restart the server every time **changes are made**.


## TODO ##
- Run the server, explore the webpage and style accordingly

#### Specifics: ####
	- On the signup page, whenever you don't meet password requirements or email
	requirements the errors which show up displace the rest of the signup form.(fix this)

	- Style the announcements on the dashboard and on the user_announcements page.
	(make some template for announcements that works on desktop and mobile)

#### Note: #####
There are some hidden elements on some pages such as:

- An announcement_edit template on the "user__announcements" page
- Possibly a div for the text editor on the "create_announcement" page
