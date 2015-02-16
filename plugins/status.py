"""!status shows the current status of the Realm"""

import humanize
import re

from model import Session, Realm
from config import wowconfig
from sqlalchemy.orm.exc import NoResultFound

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!status( .*)?", text)
    if not match: return

    session = Session()
    
    try:
        realm = session.query(Realm).filter(Realm.name == wowconfig["realm"]).one()
        
        status = u"Currently *{0}* is ".format(realm.name)
        
        if realm.online:
            status += "online (last check: {0})".format(
                humanize.naturaltime(realm.lastchecked)
            )
            status += "\n\n*Battleground status*:\n```"
            for area in realm.areas:
                status += "{0} : {1} controlled : {2} : next in {3}\n".format(
                   area.name,
                   area.faction,
                   area.status,
                   humanize.naturaldelta(area.next),
                )
            status += "```"
        else:
            status += "offline (last check: {0}, last seen: {1})".format(
                humanize.naturaltime(realm.lastchecked), 
                humanize.naturaltime(realm.lastseen)
            )
        
        return status 
    except NoResultFound:
        return u"No status known on *{0}*".format(wowconfig["realm"])