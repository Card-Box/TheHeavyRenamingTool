from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import vlc
from datetime import datetime
import json
from ttkthemes import ThemedTk, THEMES
import os
import sv_ttk
import pywinstyles, sys
from tkinter import messagebox

# This function is derived from the Sun Valley Tkinter Theme github by rdbende.
# The function utilized pywindstyles to stylize the window's bar color to match the currently selected darkmode setting.

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

# Opens and handles most of everything encapsulated inside of the settings window.

def openSettings():

    # Opens and handles most of everything encapsulated in the game destroying window.

    def openGameDestroyer():

        # Checks if gameInput consists of a game in the listOfGames. If so, removes the game from the list & updates the gameList.txt file.

        def destroyAGame():
            global listOfGames
            if (gameInput.get() in listOfGames):
                listOfGames.remove(gameInput.get())
                gameNameSelector['values'] = listOfGames
                
                with open("gameList.txt", "w") as f:
                    print("Opened the gameList file.")
                    for game in listOfGames:
                        f.write(game + "\n")
                    f.flush()
                    

            print(f"The text file was probably sent to {os.getcwd()}")

            print(f"New game list: {listOfGames}")
            gameDestroyer.destroy()

        # Checks if the entered game is in the list (and thus destroyable.) Updates gamerLabel accordingly.

        def isDestroyable(wow):
            global listOfGames

            if gameInput.get() in listOfGames:
                gamerLabel["text"] = "Game is destroyable."
            else:
                gamerLabel["text"] = "Game is not destroyable."

        gameDestroyer = Toplevel(root)
        gameDestroyer.title("Remove a game")
        gameDestroyer.columnconfigure(0, weight=1)

        gameDestroyer.protocol("WM_DELETE_WINDOW", destroyAGame)

        gamePanel = ttk.Frame(gameDestroyer, padding="15 15 15 15")
        gamePanel.grid(row=0, column=0, sticky=(N, S, E, W))

        gamerLabel = ttk.Label(gamePanel, text="Enter in the exact title of the game you want to remove.")
        gamerLabel.grid(row=0, column=0, sticky=(N, S, E, W))

        gameInput = ttk.Entry(gamePanel)
        gameInput.grid(row=1, column=0, sticky=(N, S, E, W))

        gameDestroyer.bind("<KeyRelease>", isDestroyable)

    # Handles everything in the credits window.

    def credits():
        thanks = Toplevel(root)
        thanks.title("Credits")
        thanks.columnconfigure(0, weight=1)

        thanksPanel = ttk.Frame(thanks, padding="25 25 25 25")
        thanksPanel.grid(row=0, column=0, sticky=(N, W, S, E))

        thanks_messages = [
    "Thank you, thank you, thank you and thank you so much to rdbende and his work on the Sun Valley ttk theme.\nhttps://github.com/rdbende/Sun-Valley-ttk-theme?tab=readme-ov-file\nI super ultra mega really did NOT want to have to style this program, and the sunvalley theme was the perfect solution to my plight.",
    "Most of the gui and back end were developed by me, but many elements of the back-end are sourced from stack overflow articles, including;",
    "Jay, for the file sorting code",
    "(https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python)"
]
        safafefa = 0

        for x in thanks_messages:
            label = ttk.Label(thanksPanel, text=x, padding="5, 5, 5, 5")
            label.grid(column=0, row=safafefa, sticky=(N, E, W, S))
            safafefa += 1

    # Checks the darkMode booleanVar object and changes the theme accordingly.

    def updateLightMode():

        global root

        if darkMode.get():
            sv_ttk.set_theme("dark")
            apply_theme_to_titlebar(root)
        else:
            sv_ttk.set_theme("light")
            apply_theme_to_titlebar(root)

    # Updates the settings json after the settings window is closed.
    # REMEMBER THAT THESE VARIABLES ARE ACTUALLY stringVar OBJECTS, WHICH IS WHY WE USE .get()

    def updateSettings():
        global dashesImplemented, duplciatedImplemented, americaMode, folderShowsWholeDirectory, dontAddNewGames, darkMode
        
        data = {"dashesImplemented": dashesImplemented.get(), 
                "duplciatedImplemented": duplciatedImplemented.get(),
                "americaMode": americaMode.get(),
                "folderShowsWholeDirectory": folderShowsWholeDirectory.get(),
                "dontAddNewGames": dontAddNewGames.get(),
                "darkMode": darkMode.get()
                }

        with open("settings.json", "w") as f:
            json.dump(data, f)
        
        settingsWindow.destroy()

    print("Opening settings.")
    global dashesImplemented, duplciatedImplemented, americaMode, folderShowsWholeDirectory, dontAddNewGames, darkMode
    
    settingsWindow = Toplevel(root)
    settingsWindow.title("Settings")

    settingsWindow.protocol("WM_DELETE_WINDOW", updateSettings)

    settingsFrame = ttk.Frame(settingsWindow, padding="3 3 12 12")
    settingsFrame.grid(column=0, row=0, sticky=(N, W, E, S))

    settingsWindow.columnconfigure(0, weight=1)
    settingsWindow.rowconfigure(0, weight=1)
    
    dashCheck = ttk.Checkbutton(settingsFrame, text='Dashes between each "piece"', variable=dashesImplemented, onvalue=True, offvalue=False)
    dashCheck.grid(column=0, row=0)

    duplicateCheck = ttk.Checkbutton(settingsFrame, text='Duplicates ascend in the super awesome format', variable=duplciatedImplemented, onvalue=True, offvalue=False)
    duplicateCheck.grid(column=0, row=1)

    americaCheck = ttk.Checkbutton(settingsFrame, text='Activate American Mode', variable=americaMode, onvalue=True, offvalue=False)
    americaCheck.grid(column=0, row=2)

    folderCheck = ttk.Checkbutton(settingsFrame, text='"Current Folder" shows whole directory', variable=folderShowsWholeDirectory, onvalue=True, offvalue=False)
    folderCheck.grid(column=0, row=3)

    dontAddNewGamesCheck = ttk.Checkbutton(settingsFrame, text='Manually adding gamename does not add to game list', variable=dontAddNewGames, onvalue=True, offvalue=False)
    dontAddNewGamesCheck.grid(column=0, row=4)

    darkModeCheck = ttk.Checkbutton(settingsFrame, text='Toggle Darkmode', variable=darkMode, onvalue=True, offvalue=False, command=updateLightMode)
    darkModeCheck.grid(column=0, row=5)

    reomveGameButton = ttk.Button(settingsFrame, text="Remove a game", command=openGameDestroyer)
    reomveGameButton.grid(column=0, row=6)

    thankYouButton = ttk.Button(settingsFrame, text="Credits", command=credits)
    thankYouButton.grid(column=0, row=7)

# Handles the playing of a specified video. "thigny" must be the file path which leads to the video file in question.

def play_video(thigny):
    global player, media
    media = instance.media_new(thigny)
    player.set_media(media)
    player.set_hwnd(videoFrame.winfo_id())  # Set the window handle
    pauseButton["text"] = "Pause"
    player.play() 
    
# Basic function that asks for a directory and changes it accordingly.
    
def askDialog():
    global directoryName, currentFolderLabel, filesList, fileChoiceVar, fileNameList
    directoryName = filedialog.askdirectory()

    switchDirectory()

    filesListBox.selection_clear(0, len(filesList))
    filesListBox.selection_set(0, 0)
    switchVideo("")

# Switches the directory to view all files in.
    
def switchDirectory():

    global directoryName, currentFolderLabel, filesList, fileChoiceVar, fileNameList
    folder_name = os.path.basename(directoryName)

    if folderShowsWholeDirectory.get():
        currentFolderLabel["text"] = ("Current DIRECTORY: " + directoryName)
    else:
        currentFolderLabel["text"] = ("Current folder: " + folder_name)

    # Changing the working directory to the directory specified makes it simpler to create the list of video paths for the filesList object.

    os.chdir(directoryName)

    """ Card_Box Note:
    
        This code is courtesy of Jay from this stackOverflow post: https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python

        While I don't understand it through and through, as a general note for myself;
        Filter turns the filelist into an iterator, not a list. It is converted back into list format in the following line where it goes through each file and joins the path to it;
        alongisde filtering the desktop.ini file that every windows folder usually has.
        It's afterwards sorted with the lambda as a key, creating a function that sorts by modification time.
        I think?

    """

    filesList = filter(os.path.isfile, os.listdir(directoryName))
    filesList = [os.path.join(directoryName, f) for f in filesList if f != 'desktop.ini'] # add path to each file
    filesList.sort(key=lambda x: os.path.getmtime(x))
    

    fileNameList = []

    for filename in filesList:
        filename = os.path.basename(filename)
        fileNameList.append(filename)

    fileChoiceVar.set(fileNameList)

    # Changing the working directory back to the original directory is vital in ensuring that the paths remain consistent for the rest of the code.
    
    os.chdir(originalDirectory)



# Handles most functionality related to the current time of the video.

def refreshTime():
    global timeStamp, player, vidLength, timeScale, clipAdvanceTriggered
    timeStamp = player.get_time()

    # Updates the timescale graphically to mirror the video length and time.

    timeScale["value"] = player.get_time()
    timeScale["to"] = player.get_length()

    currentTime["text"] = f"{round(float(player.get_time()) * 0.001)} / {round(float(player.get_length()) * 0.001)}"

    # If the video nears its completion, to the last 0.5 second.
    ## This was made as a precaution due to frequent errors with the video stopping itself after reaching the end of the video.

    if(player.get_time() > player.get_length() - 500):

        if clipAdvanceTriggered == False:
            clipAdvanceTriggered = True

            # Now useless code for customizable behavior at the end of a video. Scrapped due to issues with more than one clip being skipped at once.

            if loopSetting.get() == "Loop":
                timeStamp = 0
                player.set_time(0)
            elif loopSetting.get() == "Advance":
                
                # Realistically, only this branch of the selector will ever see use.

                print("Skipping to next clip since the clip ended and the setting is set to advance.")
                progressToNextClip()
            elif loopSetting.get() == "Stop":
                print("Oh god! STOP!")
                togglePause()

    else:
        clipAdvanceTriggered = False

    root.after(50, refreshTime)

# Updates whenever the slider was tampered with; changing the timestamp accordingly.

def sliderRefreshedTime(thing):
    global timeStamp, player
    timeStamp = round(float(thing))
    player.set_time(timeStamp)

# Skips the clip time forward by the skipInterval increment. If this action would go past the video length, progresses to next clip instead.

def skipForward():
    global skipInterval, timeStamp, player
    if (timeStamp + round(float(skipInterval.get()) * 1000)) < (player.get_length() - 500):
        timeStamp = timeStamp + round(float(skipInterval.get()) * 1000)
        player.set_time(timeStamp)
    else:
        progressToNextClip()

# Skips the clip time backwards by the skipInterval increment. If this action would go past the video length, goes to past clip instead.

def skipBackward():
    global skipInterval, timeStamp, player
    if (timeStamp - round(float(skipInterval.get()) * 1000)) > 0:
        timeStamp = timeStamp + round(float(skipInterval.get()) * -1000)
        player.set_time(timeStamp)
    else:
        progressToPastClip()
    
# Handles most of everything relating to the video being switched, including updating labels & updating the selectedVideo variable.

def switchVideo(forcedPickup):
    global player, media, filesListBox, fileNameList, selectedVideo, selectedIndex, fileExt
    print(f" Reading file {filesListBox.curselection()[0]}")
    selectedIndex = filesListBox.curselection()[0]
    selected = filesListBox.curselection()[0]
    selectedVideo = filesList[selected]
    print(f"Current selected video: {selectedVideo}")
    fileExt = os.path.splitext(selectedVideo)[1]
    play_video(selectedVideo)
    player.set_time(0)
    fileCounter["text"] = "File " + str(selected + 1) + " / " + str(len(filesList))
    if americaMode.get():
        dateTakenLabel["text"] = "Date Taken: " + datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%m-%d-%Y %H:%M:%S")
    else:
        dateTakenLabel["text"] = "Date Taken: " + datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%Y-%m-%d %H:%M:%S")
    currentFileLabel["text"] = "Currently Reading: " + fileNameList[selected]
    reassembleFinalName("")
    commentEntry.focus_set()

# Handles the addition of new games that are potentially not in the listOfGames via the game combo box.

def gamePlayUpdated():
    global gameName, gameNameSelector, listOfGames

    if dontAddNewGames.get():
        print("Not adding new games to the list thanks to dontAddNewGames.")

    else:
        if not (gameName.get() in listOfGames):
            print(f"{gameName} is definely not in the list of games ({listOfGames}). Keke")
            listOfGames.append(gameName.get())
            gameNameSelector['values'] = listOfGames
            with open("gameList.txt", "w") as f:
                print("Opened the gameList file.")
                for game in listOfGames:
                    f.write(game + "\n")
                f.flush()

            print(f"The text file was probably sent to {os.getcwd()}")

            print(f"New game list: {listOfGames}")

    reassembleFinalName("")
            
# Called pretty much all the time, whenever any sort of name-altering action is made.
# Reassembles the final name that the file will eventually be renamed to.
# Also handles the updating of the box labels.

def reassembleFinalName(forcedIntake):
    global finalName, fileExt, box1, box2, box3, box4, box5, finalNameLabel, gameName, specialComment, gameNameSelector, specialComment, fileNameList

    print(f"To reiterate, we are using {selectedVideo}.")

    try:

        boxesList = [box1.get(), box2.get(), box3.get(), box4.get(), box5.get()]
        boxLabelList = [box1Output, box2Output, box3Output, box4Output, box5Output]

        print(f"Aw yeah reassembling time (The extension is {fileExt}, by the way.)")


        finalName = ""
        index = 0
        partToAdd = ""

        for value in boxesList:

            partToAdd = ""

            if not ("None" in value):
                if ("Game Name" in value):

                    partToAdd = gameName.get()

                elif ("Date Taken" in value):

                    if dashesImplemented.get():

                        if americaMode.get():
                            partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%m-%d-%Y")
                        else:
                            partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%Y-%m-%d")

                    else:

                        if americaMode.get():
                            partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%m%d%Y")
                        else:
                            partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%Y%m%d")
                    
                elif ("Time Taken" in value):

                    if dashesImplemented.get():
                        partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%H-%M-%S")
                    else:
                        partToAdd = datetime.fromtimestamp(os.path.getmtime(selectedVideo)).strftime("%H%M%S")
                elif ("Special Comment" in value):
                    partToAdd = specialComment.get()
                else:
                    partToAdd = ""
                
                if dashesImplemented.get():
                    if not (index == 4):
                        if( not ("None" in boxesList[index + 1])):
                            partToAdd += "-"

                finalName += partToAdd
            #else:
                #print(f"Skipped box {index} since it was a None")

            if partToAdd == "":
                boxLabelList[index]["text"] = " - "
            else:
                boxLabelList[index]["text"] = partToAdd
            index += 1

        nameTaken = True
        soupDex = 0
        potentialFinalName = ""



        if (finalName + fileExt) in fileNameList:

            if(duplciatedImplemented.get()):

                while nameTaken:
                    soupDex += 1
                    print("I think there's something like this already here...")
                    print("Updating the final name to include a number.")
                    potentialFinalName = (finalName + str(soupDex) + fileExt)
                    if potentialFinalName in fileNameList:
                        nameTaken = True
                    else:
                        nameTaken = False
                
                finalName = finalName + str(soupDex) + fileExt
            else:
                finalName += fileExt
        else:
            finalName += fileExt
        finalNameLabel["text"] = "Final Name: " + finalName


    except Exception as e:

        print("Something wrong happened inside the reassembling function.")
        print(e)

# Toggles whether the player is playing or pausing.

def togglePause():
    global player
    if player.is_playing():
        player.pause()
        pauseButton["text"] = "Play"
    else:
        player.play()
        pauseButton["text"] = "Pause"

# Refreshes the labels on the skipInterval buttons.

def refreshInterval(thing):
    global skipInterval
    goBackButton["text"] = f"Go back by {skipInterval.get()}"
    goForwardButton["text"] = f"Go forward by {skipInterval.get()}"

# Returns the video back to the beginning of the video, or backtracking to the previous clip if too little time has passed.

def backToStart():
    global skipInterval, timeStamp, player

    if((player.get_time() - 1000) < 0):
        print("Time to go back!")
        progressToPastClip()
    else:
        timeStamp = 0
        player.set_time(0)

# Now-useless code for a potential video end-behavior function. Scrapped due to issues with more than one clip being skipped at once.

"""

def cycleLoopSetting():
    global loopSetting

    if loopSetting.get() == "Loop":
        loopSetting.set("Advance")
        loopSettingButton["text"] = "Advance"
    elif loopSetting.get() == "Advance":
        loopSetting.set("Stop")
        loopSettingButton["text"] = "Stop"
    elif loopSetting.get() == "Stop":
        loopSetting.set("Loop")
        loopSettingButton["text"] = "Loop"

"""

# Progresses to the next clip. Note how it directly manipulated the fileListBox's selection.

def progressToNextClip():

    b4file = filesListBox.curselection()[0] + 1
    filesListBox.selection_clear(0, len(filesList))
    filesListBox.selection_set(b4file, b4file)
    switchVideo("")

# Backtracks to the previous clip. Note how it directly manipulated the fileListBox's selection.

def progressToPastClip():

    b4file = filesListBox.curselection()[0] - 1
    filesListBox.selection_clear(0, len(filesList))
    filesListBox.selection_set(b4file, b4file)
    switchVideo("")

# Where the magic happens. Handles everything related to the actual renaming of the file.

def renameFile():

    global selectedVideo, finalName, fileExt

    indexKeepInMind = selectedIndex

    reassembleFinalName("")

    finalPath = os.path.join(directoryName, finalName)

    gamePlayUpdated()

    #choice = input(f"Are you sure you should do this? Renaming {selectedVideo} to {finalPath}")

    print(f"Renaming {selectedVideo} to {finalPath}")

    player.stop()
    try:

        os.rename(selectedVideo, finalPath)
        switchDirectory()
        filesListBox.selection_clear(0, len(filesList))
        filesListBox.selection_set(indexKeepInMind, indexKeepInMind)
    
    except Exception as e:
        print("Renaming failed, perhaps the file name already exists?")
        messagebox.showwarning(message="The reanming process failed. You may be trying to name a file with a name identical to another in this directory. Which is bad.")
        print(e)
    
    switchVideo("")

# Does the same thing as rename file. but also moves to the next clip without dwelling on the same one.

def renameAndNext():

    global filesListBox, clipAdvanceTriggered

    renameFile()

    if not clipAdvanceTriggered:
        clipAdvanceTriggered = True
        curIndex = filesListBox.curselection()[0]
        filesListBox.selection_clear(0, len(filesList))
        filesListBox.selection_set(curIndex + 1, curIndex + 1)
        switchVideo("")
        clipAdvanceTriggered = False
    else:
        print("Someone's already trying to advance the clip.")


root = ThemedTk()
root.title("The Heavy Renaming Tool")

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

originalDirectory = os.getcwd()
selectedIndex = -1
clipAdvanceTriggered = False

s = ttk.Style()


# Important Variables

dashesImplemented = BooleanVar()
duplciatedImplemented = BooleanVar()
americaMode = BooleanVar()
folderShowsWholeDirectory = BooleanVar()
dontAddNewGames = BooleanVar()
loopSetting = StringVar()
darkMode = BooleanVar()
loopSetting.set("Loop")

fileExt = ""

# If the settings.json doesn't exist, just create a new one!

if not (os.path.exists("settings.json")):
    with open("settings.json", "w") as f:
        data = {"dashesImplemented": True, "duplciatedImplemented": False, "americaMode": False, "folderShowsWholeDirectory": False, "dontAddNewGames": False, "darkMode": True}
        json.dump(data, f)

# Updates the settings based on the values of the JSON.

with open("settings.json", "r") as f:
    data = json.load(f)
    dashesImplemented.set(data["dashesImplemented"])
    duplciatedImplemented.set(data["duplciatedImplemented"])
    americaMode.set(data["americaMode"])
    folderShowsWholeDirectory.set(data["folderShowsWholeDirectory"])
    dontAddNewGames.set(data["dontAddNewGames"])
    darkMode.set(data["darkMode"])



# Top Half Frame

topHalfFrame = ttk.Frame(mainframe, padding="3 3 3 3")
topHalfFrame.grid(column=0, row=0, sticky=(N, W, E, S))

topHalfFrame.columnconfigure(0, weight=1)
topHalfFrame.columnconfigure(1, weight=20)
topHalfFrame.rowconfigure(1, weight=1)

cardboxTag = ttk.Label(topHalfFrame, text="The Heavy Renaming Tool \nBy Card_Box", anchor="center", padding="6 6 6 6")
cardboxTag.grid(column=0, row=0, sticky=(N, W, E, S))

# File Info Frame

currentFileFrame = ttk.Frame(mainframe, padding="3 3 3 3")
currentFileFrame.grid(column=0, row=1, sticky=(N, W, E, S))
currentFileFrame.columnconfigure(0, weight=1)
currentFileFrame.columnconfigure(1, weight=1)
currentFileFrame.rowconfigure(0, weight=1)

currentFileLabel = ttk.Label(currentFileFrame, padding="3 3 3 3", text="Currently Reading: No files yet!")
currentFileLabel.grid(column=0, row=0, sticky=(N, E))

dateTakenLabel = ttk.Label(currentFileFrame, padding="3 3 3 3", text="Date Taken: I have no idea!")
dateTakenLabel.grid(column=1, row=0, sticky=(N, W))


# Video Frame

selectedVideo = ""

videoFrame = ttk.Frame(topHalfFrame, padding="3 3 3 3", width=1200, height=675)
videoFrame.grid(column=1, row=1, sticky=(N, W, E, W))
videoFrame.grid_propagate(False) 


"""
imageLabel = ttk.Label(videoFrame, padding="3 3 3 3")
imageLabel.grid(column=0, row=0, sticky=N)
image = PhotoImage(file="16x9_by_Pengo.png")
imageLabel['image'] = image
"""

instance = vlc.Instance()
player = instance.media_player_new()

# Skip Settings Frame

skipSettingsFrame = ttk.Frame(topHalfFrame, padding="3 3 3 3")
skipSettingsFrame.grid(column=0, row=2, sticky=(N, W, E))

skipSettingsFrame.columnconfigure(1, weight=1)

skipSettingLabel = ttk.Label(skipSettingsFrame, text="Skip by _ seconds:", anchor="center")
skipSettingLabel.grid(column=0, row=0, sticky=(N))

skipInterval = StringVar()
skipInterval.set("5")
skipSettingInput = ttk.Entry(skipSettingsFrame, width=5, textvariable=skipInterval)
skipSettingInput.grid(column=1, row=0, sticky=(N, E, W))

skipSettingInput.bind("<KeyRelease>", refreshInterval)

# Now unused code for a potential video end-behavior settings section. Scrapped due to issues with more than one clip being skipped at once.

"""
loopSettingLabel = ttk.Label(skipSettingsFrame, text="Loop Setting:", anchor="center")
loopSettingLabel.grid(column=0, row=1, sticky=(N))

loopSetting = StringVar()
loopSetting.set("Loop")
loopSettingButton = ttk.Button(skipSettingsFrame, text=loopSetting.get(), command=cycleLoopSetting)
loopSettingButton.grid(column=1, row=1, sticky=(N, E, W))
"""

"""
skipSettingInput.bind("<Key>", reassembleFinalName)
skipSettingInput.bind("<FocusOut>", reassembleFinalName)
"""

# Video Controls Frame

videoControlsFrame = ttk.Frame(topHalfFrame, padding="3 3 3 3")
videoControlsFrame.grid(column=1, row=2, sticky=(N, E, W))

videoControlsFrame.columnconfigure(0, weight=1, minsize=40)
videoControlsFrame.columnconfigure(1, weight=1, minsize=40)
videoControlsFrame.columnconfigure(2, weight=3, minsize=40)
videoControlsFrame.columnconfigure(3, weight=1, minsize=40)
videoControlsFrame.columnconfigure(4, weight=1, minsize=40)

timeStamp = DoubleVar()
vidLength = DoubleVar()

timelineFrame = ttk.Frame(videoControlsFrame)
timelineFrame.grid(column=0, row=0, sticky=(N, W, E), columnspan=5)

timelineFrame.columnconfigure(1, weight=1)

currentTime = ttk.Label(timelineFrame, text="X / Y")
currentTime.grid(column=0, row=0, sticky=(N, W, E))

timeScale = ttk.Scale(timelineFrame, from_=0, to=100, orient=HORIZONTAL, command=sliderRefreshedTime)
timeScale.grid(column=1, row=0, sticky=(N, W, E))

beginningButton = ttk.Button(videoControlsFrame, text="Beginning", command=backToStart)
beginningButton.grid(column=0, row=1, sticky=(N, E, W))

goBackButton = ttk.Button(videoControlsFrame, text=f"Go back by {skipInterval.get()}", command=skipBackward)
goBackButton.grid(column=1, row=1, sticky=(N, W, E))

pauseButton = ttk.Button(videoControlsFrame, text="Pause", command=togglePause)
pauseButton.grid(column=2, row=1, sticky=(N, W, E))

goForwardButton = ttk.Button(videoControlsFrame, text=f"Go forward by {skipInterval.get()}", command=skipForward)
goForwardButton.grid(column=3, row=1, sticky=(N, W, E))

advanceButton = ttk.Button(videoControlsFrame, text=f"Next File", command=progressToNextClip)
advanceButton.grid(column=4, row=1, sticky=(N, W, E))

# Text Boxes Frame

textBoxesFrame = ttk.Frame(mainframe, padding="3 3 3 3")
textBoxesFrame.grid(column=0, row=2, sticky=(N, W, E))

textBoxesFrame.columnconfigure(0, weight=1)
textBoxesFrame.columnconfigure(1, weight=1)


specialCommentLabel = ttk.Label(textBoxesFrame, text="Special Comment:", anchor="center")
specialCommentLabel.grid(column=0, row=0, sticky=(N))

specialComment = StringVar()
commentEntry = ttk.Entry(textBoxesFrame, textvariable=specialComment)
commentEntry.grid(column=0, row=1, sticky=(N, W, E))

commentEntry.bind("<KeyRelease>", reassembleFinalName)
commentEntry.bind("<FocusOut>", reassembleFinalName)

gameNameLabel = ttk.Label(textBoxesFrame, text="Game Name:", anchor="center")
gameNameLabel.grid(column=1, row=0, sticky=(N))

# Creats the listOfGames used for the gameNameSelector, including reading the gameList.txt file.

listOfGames = []

try:
    f = open("gameList.txt", "r")
    f.close()
except:
    f = open("gameList.txt", "w")
    f.close()

with open("gameList.txt", "r") as f:
    for line in f:
        if line.strip() != "":
            listOfGames.append(line.strip())

gameName = StringVar()
gameNameSelector = ttk.Combobox(textBoxesFrame, textvariable=gameName)
gameNameSelector.grid(column=1, row=1, sticky=(N, W, E))
gameNameSelector['values'] = listOfGames
gameNameSelector.set("GameName")

gameNameSelector.bind("<KeyRelease>", reassembleFinalName)
gameNameSelector.bind("<Button-1>", reassembleFinalName)

# Adds a lil bit of padding to every element in the text boxes frame.

for child in textBoxesFrame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Name Order Frame

nameOrderingFrame = ttk.Frame(mainframe, padding="3 3 3 3")
nameOrderingFrame.grid(column=0, row=3, sticky=N)

nameOrderingFrame.columnconfigure(0, weight=1)
nameOrderingFrame.columnconfigure(1, weight=1)
nameOrderingFrame.columnconfigure(2, weight=1)
nameOrderingFrame.columnconfigure(3, weight=1)
nameOrderingFrame.columnconfigure(4, weight=1)

box1 = StringVar()
box1Selector = ttk.Combobox(nameOrderingFrame, textvariable=box1, state="readonly")
box1Selector.grid(column=0, row=0, sticky=(N))
box1Selector['values'] = ("Default (None)", "Game Name", "Date Taken", "Time Taken", "Special Comment", "None")
box1Selector.set("Default (None)")

box1Output = ttk.Label(nameOrderingFrame, text=" - ")
box1Output.grid(column=0, row=1, sticky=(N))

box2 = StringVar()
box2Selector = ttk.Combobox(nameOrderingFrame, textvariable=box2, state="readonly")
box2Selector.grid(column=1, row=0, sticky=(N))
box2Selector['values'] = ("Default (Game Name)", "Game Name", "Date Taken", "Time Taken", "Special Comment", "None")
box2Selector.set("Default (Game Name)")

box2Output = ttk.Label(nameOrderingFrame, text=" - ")
box2Output.grid(column=1, row=1, sticky=(N))

box3 = StringVar()
box3Selector = ttk.Combobox(nameOrderingFrame, textvariable=box3, state="readonly")
box3Selector.grid(column=2, row=0, sticky=(N))
box3Selector['values'] = ("Default (Date Taken)", "Game Name", "Date Taken", "Time Taken", "Special Comment", "None")
box3Selector.set("Default (Date Taken)")

box3Output = ttk.Label(nameOrderingFrame, text=" - ")
box3Output.grid(column=2, row=1, sticky=(N))

box4 = StringVar()
box4Selector = ttk.Combobox(nameOrderingFrame, textvariable=box4, state="readonly")
box4Selector.grid(column=3, row=0, sticky=(N))
box4Selector['values'] = ("Default (Time Taken)", "Game Name", "Date Taken", "Time Taken", "Special Comment", "None")
box4Selector.set("Default (Time Taken)")

box4Output = ttk.Label(nameOrderingFrame, text=" - ")
box4Output.grid(column=3, row=1, sticky=(N))

box5 = StringVar()
box5Selector = ttk.Combobox(nameOrderingFrame, textvariable=box5, state="readonly")
box5Selector.grid(column=4, row=0, sticky=(N))
box5Selector['values'] = ("Default (None)", "Game Name", "Date Taken", "Time Taken", "Special Comment", "None")
box5Selector.set("Default (None)")

box5Output = ttk.Label(nameOrderingFrame, text=" - ")
box5Output.grid(column=4, row=1, sticky=(N))

# If any of these boxes for any reason are selected, the reassembleFinalName function is ran to ensure the user knows what they just did.

box1Selector.bind("<<ComboboxSelected>>", reassembleFinalName)
box2Selector.bind("<<ComboboxSelected>>", reassembleFinalName)
box3Selector.bind("<<ComboboxSelected>>", reassembleFinalName)
box4Selector.bind("<<ComboboxSelected>>", reassembleFinalName)
box5Selector.bind("<<ComboboxSelected>>", reassembleFinalName)

for child in nameOrderingFrame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Folder Frame

folderFrame = ttk.Frame(topHalfFrame, padding="0 0 0 0")
folderFrame.grid(column=0, row=1, sticky=(N, S, W, E))

folderFrame.columnconfigure(0, weight=1)
folderFrame.rowconfigure(4, weight=1)

settingsButton = ttk.Button(folderFrame, text="Settings", padding="3 3 3 3", command=openSettings)
settingsButton.grid(column=0, row=0, sticky=(N))

currentFolderLabel = ttk.Label(folderFrame, padding="3 3 3 3", text="Current folder:")
currentFolderLabel.grid(column=0, row=1, sticky=N)

switchFolderButton = ttk.Button(folderFrame, text="Change Folder", command=askDialog)
switchFolderButton.grid(column=0, row=2, sticky=N)

fileCounter = ttk.Label(folderFrame, padding="3 3 3 3", text="File X / Y")
fileCounter.grid(column=0, row=3, sticky=N)

fileNameList = []

# Files List Frame
fileListFrame = ttk.Frame(folderFrame, style="vidControl.TFrame")
fileListFrame.grid(column=0, row=4, sticky=(N, S, W, E))

fileListFrame.columnconfigure(0, weight=1)
fileListFrame.rowconfigure(0, weight=1)

# Adding a bunch of pokemon (and beasties) to the initialization of the filesList is completely unncessesary.
# Feel free to empty this list for a more ergonomic user experience.

filesList = [
    "Cinderace", "Ribombee", "Cincinno", "Meowstic", "Lanturn", "Maractus", 
    "Serperior", "Emolga", "Audino", "Frillish", "Boldour", "Gurdurr", 
    "Meowscarda", "Pawmot", "Garganacl", "Armarogue", "Palafin", "Maushold",
    "Venasaur", "Raichu", "Butterfree", "Flareon", "Dewgong", "Clefable", 
    "Empoleon", "Pachurisu", "Lopunny", "Mismagius", "Roserade", "Chatot", 
    "Delphox", "Furfrou", "Vivillion", "Azumarill", "Toxicroak", "Aurorus",
    "Bandicraft", "Illigus", "Zepfyre", "Supliero", "Fetcham"
]
fileChoiceVar = StringVar(value=filesList)
filesListBox = Listbox(fileListFrame, listvariable=fileChoiceVar, selectmode=BROWSE, width=30)
filesListBox.grid(column=0, row=0, sticky=(N, S, E, W))

filesListScrollbar = ttk.Scrollbar(fileListFrame, orient=VERTICAL, command=filesListBox.yview)  
filesListScrollbar.grid(column=1, row=0, sticky=(N, S, E))
filesListBox['yscrollcommand'] = filesListScrollbar.set

filesListBox

filesListBox.bind('<<ListboxSelect>>', switchVideo)

# Final Frame

finalName = ""

finalFrame = ttk.Frame(mainframe, padding="3 3 3 3")
finalFrame.grid(column=0, row=4, sticky=(N, S))

finalNameLabel = ttk.Label(finalFrame, padding="3 3 3 3", text="Final Name: ???")
finalNameLabel.grid(column=1, row=0, sticky=(N, S))

finalConfirmButton = ttk.Button(finalFrame, padding="3 3 3 3", text="Rename and Stay", command=renameFile)
finalConfirmButton.grid(column=0, row=0, sticky=(N, S))

finalConfirmNextButton = ttk.Button(finalFrame, padding="3 3 3 3", text="Rename and Progress", command=renameAndNext)
finalConfirmNextButton.grid(column=2, row=0, sticky=(N, S))


root.bind('<Left>',  lambda event: skipBackward())
root.bind('<Right>',  lambda event: skipForward())
root.bind('<Up>',  lambda event: progressToPastClip())
root.bind('<Down>',  lambda event: progressToNextClip())
root.bind('<Return>',  lambda event: renameAndNext())
root.bind("<Button-1>", reassembleFinalName)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

print(f"Current working directory: {os.getcwd()}")

# Updates the theme of the GUI.
sv_ttk.set_theme("dark")
apply_theme_to_titlebar(root)

# Calls the refreshTime function, which will constantly repeat itself.
refreshTime()

root.mainloop()