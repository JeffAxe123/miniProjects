# first modules
import logging
import sys
log_file="app.log"

logging.basicConfig(filename="app.log", level=logging.INFO)
try:
    import json
    import os
    import getopt
    import easygui as eg
    import PySimpleGUI as sg
    import threading
    import webbrowser
    import subprocess
    import shutil
    import traceback
    import random
    import requests
    import time
    import re
    import urllib.request
    buildfile=".build"
    argv=sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"b:h:",["bfile=","hfile="])
    except getopt.GetoptError as e:
      print('laucnher.pyw -b <buildfile>')
      print(e)
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-b':
            buildfile=arg
        elif opt=="-h":
            sys.exit('laucnher.pyw -b <buildfile>')
    try:
        with open(buildfile) as corebuild:
            core = json.load(corebuild)
    except FileNotFoundError:
        eg.msgbox(
            "You have attempted to open this application outside of a BUILD environment.\n Make sure there is a file named .build (file type: BUILD) in the same folder as this application.\nThis file contains metadata about the application, visit the github page\n for how to make one, or to download the defualt if it got currupted.\n\n You can also specifty a custom build file by using -build in the launch. ")
        sys.exit(10)
    logging.shutdown()
    if os.path.exists(core["log-file"]):
        os.remove(core["log-file"])
    logging.basicConfig(filename=core["log-file"], level=logging.INFO)
    if not os.path.exists(core["crash-reports-folder"]):
        os.mkdir(core["crash-reports-folder"])

    with open(core["settings"][1]) as options:
        options = json.load(options)

    # crash catching method
    def crash_catch(error):
        try:
            mainWindow.window.close()
        except (AttributeError,NameError):
            pass
        try:
            play.window.close()
        except (AttributeError,NameError):
            pass
        try:
            advancedSettings.window.close()
        except (AttributeError,NameError):
            pass
        logging.info("Process exiting with code " + str(error)+"...")
        logging.shutdown()
        #erros after this point(in this function) are not logged, be warned! (Unless logged with logging. ,  apparently?)
        if str(error) != "0":
            shutil.copyfile(core["log-file"],
                      core["crash-reports-folder"] + "/crash-report-" + str(options["crashes"]) + ".log")
            os.system("start " + core["crash-reports-folder"] + "/crash-report-" + str(options["crashes"]) + ".log")
            options["crashes"] += 1
            with open(core["settings"][1], "w") as update:
                json.dump(options, update, sort_keys=True, indent=4)
        if str(error)=="0" and options["debug-mode"]==True:
            os.system("start "+core["log-file"])    
        sys.exit(error)


    # basic config load
    try:
        with open(core["settings"][0]) as basic:
            config = json.load(basic)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        try:
            shutil.copyfile("backups/" + core["settings"][0] + ".original", core["settings"][0])
            with open(core["settings"][0]) as basic:
                config = json.load(basic)
        except FileNotFoundError:
            url = core["filehost"] + '/backups/' + core["settings"][0] + ".original"
            r = requests.get(url)
            if not os.path.exists("backups/"):
                os.mkdir("backups")
            with open("backups/" + core["settings"][0] + ".original", "wb") as backup:
                backup.write(r.content)
            shutil.copyfile("backups/" + core["settings"][0] + ".original", core["settings"][0])
            with open(core["settings"][0]) as basic:
                config = json.load(basic)

    # config setup
    def reloadConfig():
        with open(core["settings"][0]) as config:
            config = json.load(config)
        with open("backups/" + core["settings"][0] + ".original") as original_config:
            original_config = json.load(original_config)
        folders = config.keys()
        for folder in folders:
            for chars in config[folder]:
                if config[folder] in core["illegal-names"]:
                    logging.info(
                                     config[folder] + " is an illegal name. It is being reverted to default name")
                    config[folder]=original_config[folder]
                if chars in core["illegal-chars"]:
                    logging.info( #"resourecs":{"languages-folder": "languages"},
                        confi[folder] + " contains an illegal char. It is being reverted to default name")
                    config[folder]=original_config[folder]
            if not os.path.exists(config[folder]):
                        os.makedirs(config[folder])
        with open(core["settings"][0], "w") as write:
            json.dump(config, write, sort_keys=True, indent=4)
        return config


    config = reloadConfig()
    if options["debug-mode"]:
        logging.info("DEBUG mode is on")
        logging.getLogger().setLevel(logging.DEBUG)
    

    def saveOptions(options):
        with open(core["settings"][1],"w") as save:
            json.dump(options, save, sort_keys=True, indent=4)
    # lang file load
    try:
        with open(config["languages-folder"] + "/launcher/" + options["lang"] + ".lang") as lang:
            lang = json.load(lang)
    except FileNotFoundError:
        r = requests.get(
            core["filehost"] + "/assets/languages/launcher/" + options["lang"] + ".lang")
        if not os.path.exists(config["languages-folder"] + "/launcher"):
            os.makedirs(config["languages-folder"] + "/launcher")
        if not os.path.exists("assets/"+config["languages-folder"] + "/games/"):
            os.mkdir(config["languages-folder"] + "/games")
        with open(config["languages-folder"] + "/launcher/" + options["lang"] + ".lang", "wb") as save:
            save.write(r.content)
        with open(config["languages-folder"] + "/launcher/" + options["lang"] + ".lang") as lang:
            lang = json.load(lang)

    logging.debug(options["lang"] + " language is initiated")
    def getLang(langCode):
        try:
            returnVal = lang[langCode]
        except KeyError:
            returnVal = langCode
        return returnVal
    # detect launcher update
    if core["dev"]:
        updateFile="launcher-version.dev"
    else:
        updateFile="launcer-version.txt"
    try:  # encase there is no internet connection
        logging.debug("Checking for new launcher versions")
        updateCheck = urllib.request.urlopen(core["filehost"] + "/"+updateFile).read()
        updateCheck = updateCheck.decode("utf-8").replace("\n","")
        if core["version"] != updateCheck:
            logging.info("There is a new launcher update available!"+"("+updateCheck+")")
            sg.Popup(getLang("There is a new launcher update available!")+"("+updateCheck+")")
    except requests.exceptions.ConnectionError:
        logging.info("An error occurred, probably due to no connection")
        logging.error(traceback.format_exc())
    except urllib.error.HTTPError:
        logging.info("The requested file was not found, or the request was invalid")
        logging.critical(traceback.format_exc())

    # setup

    def createLogo():
        if not os.path.exists(config["icons-folder"]+"/app.png"):
            r = requests.get(core["filehost"] + "/assets/icons/app.png")
            with open(config["icons-folder"]+"/app.png", 'wb') as output_file:
                output_file.write(r.content)

    def advanedSettings():
        config=reloadConfig()
        layout = [[sg.Button(getLang("menu.Main"),size=(50,5))],
            [sg.Button(getLang("menu.settings.advanced.debug-mode"),size=(100,5))],
            [sg.Button(getLang("menu.settings.advanced.crashes"),size=(100,5))],
            [sg.Button(getLang("menu.settings.advanced.source.games"),size=(100,5))],
            [sg.Button(getLang("menu.settings.advanced.directory"),size=(100,5))]
                  ]
        window = sg.Window(core["name"] + "(" + getLang("menu.advanced") + ") "+ core["version"], layout).Finalize()
        advanedSettings.window=window
        mainWindow.window = window
        window.Maximize()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                window.close()
                sys.exit(0)
            elif event==getLang("menu.settings.advanced.directory"):
                subprocess.Popen("explorer .")
            elif event==getLang("menu.Main"):
                window.close()
                mainWindow()
            elif event==getLang("menu.settings.advanced.debug-mode"):
                debug=eg.ynbox("Enable Debug Mode?")
                if debug:
                    options["debug-mode"]=True
                    logging.info("DEBUG mode is on")
                    logging.getLogger().setLevel(logging.DEBUG)
                else:
                    options["debug-mode"]=False
            elif event==getLang("menu.settings.advanced.crashes"):
                options["crashes"]=0
                for file in os.listdir(config["crash-reports-folder"]):
                    os.remove(config["crash-reports-folder"]+"/"+file)
                logging.debug("Reset crash count")
                eg.msgbox(lang["menu.settings.advanced.crashes.Message"])
            elif event==getLang("menu.settings.advanced.source.games"):
                config = reloadConfig()
                # this is for the Layout Design of the Window
                layout2 = [[sg.Text(lang['meta.loading'])],
                           [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
                           ]
                # This Creates the Physical Window
                update_window = sg.Window(core["name"], layout2).Finalize()
                progress_bar = update_window.FindElement('progress')

                # This Updates the Window
                # progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
                # update
                try:
                    logging.info('Downloading source code for games...')
                    url = core["filehost"] + '/downloads.txt'
                    r = requests.get(url)
                    for downloads in urllib.request.urlopen(url):
                        downloads=downloads.decode("utf-8")
                        downloads = downloads.split()
                    logging.debug("these games are: "+str(downloads))
                    for file in downloads:
                        logging.debug('Requesting download for soure code of' + file)
                        r = requests.get(core["filehost"] + "/games/" + file+"/src/Main.java")
                        with open("src/"+config["Games-Directory"] + "/"+file+".java", "wb") as io:
                                io.write(r.content)
                        with open("src/"+config["Games-Directory"] + "/"+file+".java","r") as io:
                            found=io.read()
                        if found=="404: Not Found":
                            logging.info("No source code found for "+file)
                            if os.path.exists("src/"+config["Games-Directory"] + "/"+file+".txt"):
                                os.remove("src/"+config["Games-Directory"] + "/"+file+".txt")
                            os.rename("src/"+config["Games-Directory"] + "/"+file+".java","src/"+config["Games-Directory"] + "/"+file+".txt")
                        progress_bar.UpdateBar(downloads.index(file) + 1, len(downloads) + 4)
                    update_window.close()
                except requests.exceptions.ConnectionError:
                    logging.info("Connection failed")
            saveOptions(options)
    def mainWindow():
        global config
        global lang
        global options
        layout = [
            [sg.Text('', size=(28, 1)), sg.Button(getLang("menu.site.homepage"), size=(45, 1)),
             sg.Button(getLang("languages"), size=(45, 1))],
            [sg.Text('', size=(28, 1)),
             sg.Button(getLang("menu.site.issues"), size=(92, 1))],
            [sg.Text('', size=(13, 1)), sg.Image(r''+config["icons-folder"]+'/app.png', size=(999, 500))],
            [sg.Button(getLang("menu.settings.advanced"),size=(10,3)),sg.Button(getLang("menu.settings"), size=(50, 3)), sg.Button(getLang("menu.play"), size=(50, 3)),sg.Button(getLang("menu.close"), size=(50, 3))]
        ]
        createLogo()
        window = sg.Window(core["name"] + "(" + lang["menu.Main"] + ") "+ core["version"], layout).Finalize()
        mainWindow.window = window
        window.Maximize()
        # start event loop
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                window.close()
                sys.exit(0)
            elif event == getLang("languages"):
                if not os.path.exists(config["languages-folder"]+"/languages.json"):
                    r = requests.get(core["filehost"] + "/assets/languages/languages.json")
                    with open(config["languages-folder"]+"/languages.json", "wb") as langU:
                        langU.write(r.content)
                with open(config["languages-folder"]+"/languages.json") as languages:
                    languages = json.load(languages)
                choice = eg.choicebox("Select a language", "Select", languages.keys())
                if choice is not None:
                    choice = languages[choice]
                    options["lang"] = choice
                    with open(core["settings"][0], "w") as save:
                        json.dump(config, save, sort_keys=True, indent=4)
                    # lang file load
                    try:
                        with open(config["languages-folder"]+"/launcher/" + options["lang"] + ".lang") as lang:
                            lang = json.load(lang)
                    except (json.decoder.JSONDecodeError, FileNotFoundError):
                        eg.msgbox(
                            "There was an error initiating your language , or it has not yet been downloaded(" + options[
                                "lang"] + ")")
                        logging.warning(traceback.format_exc())
                        url = core["filehost"] + '/languages/launcher/' + options["lang"] + ".lang"
                        r = requests.get(url)
                        with open(config["languages-folder"] + "/launcher/" + options["lang"] + "lang", "wb") as backup:
                            backup.write(r.content)
                    logging.debug(options["lang"] + " language is initiated")
                    window.close()
                    mainWindow()

            elif event == getLang("menu.site.homepage"):
                webbrowser.open(core["homepage"])
            elif event == getLang("menu.site.issues"):
                webbrowser.open(core["issues"])
            elif event == getLang("menu.close"):
                logging.debug("Closing on user's request")
                sys.exit(0)
            elif event == getLang("menu.play"):
                window.close()
                play()
            elif event == lang["menu.settings"]:
                choice = eg.multenterbox(getLang("menu.settings.message"), core["name"],
                                         ["Games Directory", "folder for unauthorised jars", "folder for resources",
                                          "folder for language files"])
                if choice is None:
                    logging.debug("User cancelled settings tab")
                else:
                    settings = {}
                    # for setts in choice:
                    # settings.update(config.keys()
                    config.update(settings)
                    with open(core["settings"], "w") as reload:
                        json.dump(config, reload, sort_keys=True, indent=4)
                    config = reloadConfig()
            elif event== getLang("menu.settings.advanced"):
                window.close()
                advanedSettings()

    def play():
        config = reloadConfig()
        # this is for the Layout Design of the Window
        layout2 = [[sg.Text(lang['meta.loading'])],
                   [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
                   ]
        # This Creates the Physical Window
        window = sg.Window(core["name"], layout2).Finalize()
        progress_bar = window.FindElement('progress')

        # This Updates the Window
        # progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
        # update
        try:
            logging.info('Downloading new games...')
            url = core["filehost"] + '/downloads.txt'
            r = requests.get(url)
            for downloads in urllib.request.urlopen(url):
                downloads=downloads.decode("utf-8")
                downloads = downloads.split()
                logging.debug("these games are: "+str(downloads))
                installations = [None]
                for i in downloads:
                    installations.append(i+".jar")
                installations.remove(None)
                for filegame in os.listdir(config["Games-Directory"]):
                    logging.debug(filegame +" is being checked against list of valid games")
                    if filegame not in installations:
                        os.rename(config["Games-Directory"] + "/" + filegame,
                                  config["unauthorisedJars-Directory"] + "/" + filegame)
                        logging.info(
                            filegame +" is invalid. Moving it to " + config["unauthorisedJars-Directory"])
                    else:
                        logging.debug(filegame +" is valid")
                progress_bar.UpdateBar(1, 4)
                for file in downloads:
                    if file + ".jar" in os.listdir(config["Games-Directory"]):
                        logging.debug("You already have " + file +", skipping over")
                    else:
                        logging.debug('Requesting download for ' + file)
                        r = requests.get(core["filehost"] + "/games/" + file+"/bin/"+file+".jar")
                        with open(config["Games-Directory"] + "/"+file+ ".jar", "wb") as io:
                            io.write(r.content)
                        try:
                            with open(config["Games-Directory"]+"/"+file+".jar","r") as is_it_real:
                                is_it_real=is_it_real.read()
                            if is_it_real=="404: Not Found":
                                logging.info(file+" was not downloaded properly. Moving...")
                                try:
                                    os.rename(config["Games-Directory"] + "/" + file+".jar",
                                  config["unauthorisedJars-Directory"] + "/" + file+".jar")
                                except FileExistsError:
                                    os.remove(config["unauthorisedJars-Directory"] + "/" + file+".jar")
                                    os.rename(config["Games-Directory"] + "/" + file+".jar",
                              config["unauthorisedJars-Directory"] + "/" + file+".jar")
                        except UnicodeDecodeError:
                            logging.debug("Seams like a legit binary file (likey JAR file)")
                    r = requests.get(core["filehost"] + "/games/"+file+"/bin/"+file+".lang")
                    if not os.path.exists(config["languages-folder"] + "/games"):
                        os.mkdir(config["languages-folder"] + "/games")
                    if not os.path.exists("/"+config["languages-folder"]+"/games/" + file + ".lang"):
                        with open(config["languages-folder"]+"/games/" + file + ".lang", "wb") as io:
                            io.write(r.content)
                            logging.debug("downloading "+file+".lang")
                            with open(config["languages-folder"]+"/games/"+file+".lang","r") as is_it_real:
                                is_it_real=is_it_real.read()
                                if is_it_real=="404: Not Found":
                                    logging.info(file+" was not downloaded properly. Moving...")
                                    os.rename(config["Games-Directory"] + "/" + file,
                                      config["unauthorisedJars-Directory"] + "/" + file)
                                    

                    progress_bar.UpdateBar(downloads.index(file) + 1, len(downloads) + 4)
        except requests.exceptions.ConnectionError:
            logging.info("Connection failed")
        correct_input = False
        window.close()

        vers = os.listdir(config["Games-Directory"])
        insts = []
        layout_selector = [
            [sg.Button(lang["menu.Main"], size=(100, 5))]
        ]
        gamelist = {}
        for i in vers:
            if ".jar" in i:
                i = i.replace(".jar", "")
                with open(config["languages-folder"]+"/games/" + i + ".lang") as langfile:
                    try:
                        game_lang = json.load(langfile)
                    except json.decoder.JSONDecodeError:
                        logging.error("There was an error loading the lang file "+config["languages-folder"]+"/games/"+i+".lang")
                        logging.info(traceback.format_exc())
                        sys.exit(2)
                gamelist.update({game_lang[options["lang"]]: i})
                images=[]
                try:
                    insts.append(game_lang[options["lang"]])
                except KeyError:
                    insts.append(game_lang["en"])
                if not os.path.exists(config["icons-folder"]+"/missing.png"):
                    r = requests.get(core["filehost"] + "/assets/icons/missing.png")
                    with open(config["icons-folder"]+"/missing.png", "wb") as image:
                        image.write(r.content)
                r = requests.get(core["filehost"] + "/assets/icons/games/"+i+".png")
                with open(config["icons-folder"]+"/games/"+i+".png", "wb") as imageio:
                    imageio.write(r.content)
                with open(config["icons-folder"]+"/games/"+i+".png") as io:
                    try:
                        io.read()
                        doIt=True
                    except Exception as e:
                        logging.info(e)
                        doIt=False
                if doIt:
                    os.remove(config["icons-folder"]+"/games/"+i+".png")
                if not os.path.exists(config["icons-folder"]+"/games/"+i+".png"):
                    shutil.copyfile(config["icons-folder"]+"/missing.png", config["icons-folder"]+"/games/" + i + ".png")
                try:
                    layout_selector.append([sg.Image(r''+config["icons-folder"]+'/games/' + i + '.png'),
                                            sg.Button(game_lang[config["lang"]], size=(100, 1))])
                    images.append([sg.Image(r''+config["icons-folder"]+'/games/' + i + '.png')])
                except KeyError:
                    layout_selector.append(
                        [sg.Image(r''+config["icons-folder"]+'/games/' + i + '.png'), sg.Button(game_lang["en"], size=(100, 1))])
                    images.append([sg.Image(r''+config["icons-folder"]+'/games/' + i + '.png')])

        while not correct_input:
            try:
                play.window.close()
            except:
                pass
            progress_bar.UpdateBar(downloads.index(file) + 4, len(downloads) + 4)
            window = sg.Window(core["name"] + "(Playing in /" + config["Games-Directory"] + "/)",
                               layout_selector).Finalize()
            play.window = window
            window.Maximize()
            # start loop
            while True:
                game, values = window.read()
                if game == sg.WIN_CLOSED:
                    window.close()
                    sys.exit(0)
                elif game == lang["menu.Main"]:
                    window.close()
                    mainWindow()
                elif game in insts:
                    with open(
                            config["languages-folder"]+"/" + config["Games-Directory"] + "/" + gamelist[game] + ".lang"):
                        logging.debug(str(game) + " loaded")
                        #call of the game
                        #######################
                        ####################
                        #################
                        ############
                        #######
                        ####
                        ##
                        #
                        value = subprocess.call(['java', '-jar', 'games/' + gamelist[game] + '.jar', '&','pause','&','echo', '%ErrorLevel%',])
                        if value != 0 and value != 3221225786:
                            choice = eg.choicebox(
                                "There was an error executing " + game + ",automatically delete the file from /" +
                                config["Games-Directory"] + "/ (it will  be re-downloaded), or not?", "Error",
                                ["Automatic Recovery", "Cancel"])
                            if choice == "Automatic Recovery":
                                try:
                                    os.remove(config["Games-Directory"] + "/" + gamelist[game] + ".jar")
                                except FileNotFoundError:
                                    logging.info(game + "was deleted from /" + config[
                                        "Games-Directory"] + "/ while play.window was open, so it is being re-downloaded")
                                play()
                        logging.info(gamelist[game] + " exited with code " + str(value))


    # end play
    sg.LOOK_AND_FEEL_TABLE['MyTheme'] = {'BACKGROUND': 'black',
                                         'TEXT': 'white',
                                         'INPUT': 'white',
                                         'TEXT_INPUT': 'white',
                                         'SCROLL': 'white',
                                         'BUTTON': ('white', '#125623'),
                                         'PROGRESS': ('white', 'white'),
                                         'BORDER': 1, 'SLIDER_DEPTH': 0,
                                         'PROGRESS_DEPTH': 0, }
    sg.theme("MyTheme")
    mainWindow()
except SystemExit as e:
    try:
        crash_catch(e)
    except NameError:
        sys.exit(e)
except Exception as e:
    try:
        with open(core["settings"][0], "w") as save:
            json.dump(config, save, sort_keys=True, indent=4)
        logging.exception(e)
        sys.exit(1)
    except SystemExit as e:
        crash_catch(e)

