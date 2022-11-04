# trello2markdown

This script will download all your trello boards, lists and cards, archived or not and will save them into markdown with the following structure
* board folder
	* list_file.md
		* card title as heading1
			* Description as inside text
			* Comments as heading2 with author and date
	* Attachments in attachements folder
		* Attachments treated as image + link as default

Archived items will add *_archived* to the folder and file name

# Usage
python3 trello2markdown.py destination_folder key token

# Get key and token

* Log into [https://trello.com/app-key](https://trello.com/app-key)
	* Grab a key
* Go to [https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=trello2markdown&key=YOURKEY](https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=trello2markdown&key=YOURKEY)
	* Get the token

