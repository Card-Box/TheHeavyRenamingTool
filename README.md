
# The Heavy Renaming Tool

The Heavy Renaming Tool is a program I wrote in Python that uses Tkinter alongside the VLC python library to streamline the process of renaming lots of videofiles at the same time.

There's a couple bells and whistles here and there but it's overall pretty robust and only really meant to do what it was designed for.

I apologize in advance for any issues regarding my programming, it's pretty obvious I was learning tkinter along the way and I wish any people trying to decipher it the best of luck.

( Its probably not even that bad, but I'm just being careful. )

See this video; https://youtu.be/IfByXh1n-6w for more information.


## What can I do on it?

Running the .py opens up a window which displays pretty much everything you'll need while using the tool.

- Opening a folder / directory to get the list of clips from
- Picking through a list of video clips in the folder (in order of date of modification)
- Basic video playback controls
- The game name combo-box to rename the file by 
    - You can either enter in a game name manually (saving it to your list of games) or use the built in dropdown to select from your games list. 
- A special comment input box to tag certain clips with an addition to the name
- 5 drop down boxes to change the naming  / order of all your files. Choose from a variety of parameters such as:
    - Game name
    - Date of creation
    - Time of creation
    - Special comment
    - None
- Buttons to rename the selected file (and optionally progress to next clip)

## Settings

- Dashes between each "piece" - Adds dashes between the elements of the final name AND adds dashes between each piece of the date and time parameters.
- American Mode - Makes the program slightly more patriotic. (YYYY-MM-DD -> MM-DD-YYYY)
- "Current Folder" shows whole directory - Changes the "current folder" label on the program to show the whole directory rather than just the directory basename.
- Manually addding gamename does not add to game list - Prevents manual additions to the gamename (through typing in the gamename box) from adding said game into the list.
- Toggle Darkmode - Toggles darkmode.
- Remove a game - Removes some element from the gameList list.


## How to use on my own system

Uhhh, I don\'t know yet!
I wrote this ReadMe the day of publishing the showcase video and haven't experimented with turning it into a .exe for easier use yet.

Since the virtual environment was inclduded in the repository I'm pretty sure the used packages should be there. I think.

If not, I'll go ahead and list them off here;
- Cython      3.0.11
- numpy       2.2.1
- packaging   24.2
- pillow      11.1.0
- pip         24.3.1
- python-vlc  3.0.21203
- pywinstyles 1.8
- setuptools  65.5.0
- sv-ttk      2.6.0
- tk          0.1.0
- ttkthemes   3.2.2

Good luck trying to use this before I make it usable!

## Credits


- rdbende - For the creation of the Sun Valley TTK theme, because I really did not want to have to work on a customizable light-dark mode myself.
- Jay (from this post https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python) - For the file "sort by modication" code.

Credits can also be found in the program's credits button in the setting.






