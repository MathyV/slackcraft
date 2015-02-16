# This plug-in is just to do all the processing of the WoW API data 
# asynchronously to prevent flooding the API server and getting you blocked
# It can not be called directly from the bot

import logging
import datetime
import time
import humanize

from battlenet import Connection, EUROPE
from config import wowconfig

from model import Realm, Session, PvPArea

connection = Connection(api_key=wowconfig["apikey"])

def send_message(server, channel, message):
    server["client"].rtm_send_message(channel, message)

def set_pvparea(session, realm, areaInfo):
    area = session.query(PvPArea).filter(PvPArea.realm == realm).filter(PvPArea.id == areaInfo.area).first()
    
    if area is None:
        logging.debug("Never seen PvP area {0} in {1}, creating new cache entry".format(areaInfo.name, realm.name))
        area = PvPArea(realm=realm, id=areaInfo.area, name=areaInfo.name)
        session.add(area)
    
    area.faction = { 0: "Alliance", 1: "Horde", 2: "Neutral"}[areaInfo.faction]
    area.status = { -1: "Unknown", 0: "Idle", 1: "Populating", 2: "Active", 3: "Concluded"}[areaInfo.status]
    area.next = datetime.datetime.fromtimestamp(areaInfo.next / 1000)
    
    
def check_realm(server):
    logging.debug("Checking realm status")
    realmInfo = connection.get_realm(EUROPE, wowconfig["realm"])

    session = Session()
    realm = session.query(Realm).filter(Realm.name == realmInfo.name).first()
    
    if realm is None:
        logging.debug("Never seen realm '{0}', creating new cache entry".format(realmInfo.name))
        realm = Realm(name=realmInfo.name, lastseen=datetime.datetime.now())
        session.add(realm)

    prevonline = realm.online
    prevlastseen = realm.lastseen

    realm.online = realmInfo.status
    realm.lastchecked = datetime.datetime.now()
    if realm.online:
        realm.lastseen = realm.lastchecked
    
    set_pvparea(session, realm, realmInfo.tolbarad)
    set_pvparea(session, realm, realmInfo.wintergrasp)
    
    session.commit()
    
    if (prevonline != realm.online):
        if realm.online:
            send_message(
                server,
                "announcements",
                u"{0} just came online! (offline for {1})".format(
                    realm.name,
                    humanize.naturaldelta(datetime.datetime.now() - prevlastseen)
                )
            )
        else:
            send_message(
                server,
                wowconfig["announcements"]["realm"],
                u"{0} just went offline".realm.name
            )

# define all the hooks
class Hook:
    def __init__(self, function=None, frequency=60):
        self.function = function
        self.lastrun = 0
        self.frequency = frequency
    
hooks = [
    Hook(check_realm, 60),
]

# actual processing hook called from slask
def on_loop(data, server):
    current_time = time.time()
    
    for hook in hooks:
        if current_time - hook.lastrun > hook.frequency:
            hook.lastrun = current_time
            hook.function(server)
    
