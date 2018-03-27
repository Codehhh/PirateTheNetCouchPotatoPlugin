# PirateTheNet CouchPotato Plugin

## Dependencies
| Name     | Install                                            |
| ---------|----------------------------------------------------|
| lxml     | apt-get install libxml2-dev libxslt-dev python-dev |
| requests | pip install requests                               |
| PTN      | pip install parse-torrent-name                     |

## Install
#### Option  1
 - From CouchPotato go to Settings->About->Directories and the second folder is the location of your data folder.
 - In your data folder there will be a custom_plugins folder. Create a new folder in the custom_ plugins folder called piratethenet
 - Simply place `init.py` and `main.py` files inside the piratethenet folder.
 - Restart CouchPotato

#### Option 2 (Requires Git)

   

 - From CouchPotato go to Settings->About->Directories and the second folder is the location of your data folder.
 - In your data folder there will be a custom_plugins folder. Open a terminal at the custom_plugins 
 - From the custom_plugins folder run `git clone https://github.com/Codehhh/PirateTheNetCouchPotatoPlugin.git` 
 - if you ever need to update, you can simply run git pull from the piratethenet folder.
 - Restart CouchPotato


## How To Use
From CouchPotato go to Settings->Searcher to configure just like any other provider. If PirateTheNet doesn't appear as an option, refresh your browser using CTRL + F5 as you may be seeing a cached version.



