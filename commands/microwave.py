import re
import time
from config import CHANNEL, ADMINS


def do_nuke(c):
    c.privmsg(CHANNEL, "        ____________________          ")
    c.privmsg(CHANNEL, "     :-'     ,   '; .,   )  '-:       ")
    c.privmsg(CHANNEL, "    /    (          /   /      \\      ")
    c.privmsg(CHANNEL, "   /  ;'  \\   , .  /        )   \\    ")
    c.privmsg(CHANNEL, "  (  ( .   ., ;        ;  '    ; )    ")
    c.privmsg(CHANNEL, "   \\    ,---:----------:---,    /    ")
    c.privmsg(CHANNEL, "    '--'     \\ \\     / /    '--'     ")
    c.privmsg(CHANNEL, "              \\ \\   / /              ")
    c.privmsg(CHANNEL, "               \\     /                ")
    c.privmsg(CHANNEL, "               |  .  |               ")
    c.privmsg(CHANNEL, "               |, '; |               ")
    c.privmsg(CHANNEL, "               |  ,. |               ")
    c.privmsg(CHANNEL, "               | ., ;|               ")
    c.privmsg(CHANNEL, "               |:; ; |               ")
    c.privmsg(CHANNEL, "      ________/;';,.',\\ ________     ")
    c.privmsg(CHANNEL, "     (  ;' . ;';,.;', ;  ';  ;  )    ")


def cmd(e, c, msg):
        levels = {1: 'Whirr...',
                  2: 'Vrrm...',
                  3: 'Zzzzhhhh...',
                  4: 'SHFRRRRM...',
                  5: 'GEEEEZZSH...',
                  6: 'PLAAAAIIID...',
                  7: 'KKKRRRAAKKKAAKRAKKGGARGHGIZZZZ...',
                  8: 'Insert Nuke Here',
                  9: 'nneeeaaaooowwwwww..... BOOOOOSH BLAM KABOOM',
                  10: 'ssh root@remote.tjhsst.edu rm -rf ~'+e.source.nick}
        if msg == '':
            c.privmsg(CHANNEL, 'What to microwave?')
            return
        match = re.match('([0-9]*) (.*)', msg)
        if not match:
            c.privmsg(CHANNEL, 'Power level?')
        else:
            level = int(match.group(1))
            if level > 10:
                c.privmsg(CHANNEL, 'Aborting to prevent extinction of human race.')
                return
            if level > 7 and e.source.nick not in ADMINS:
                c.privmsg(CHANNEL, "I'm sorry. Nukes are a admin-only feature")
                return
            for i in range(1, level+1):
                if i == 8:
                    do_nuke(c)
                else:
                    c.privmsg(CHANNEL, levels[i])
                time.sleep(1)
            time.sleep(1)
            c.privmsg(CHANNEL, 'Ding, your %s is ready.' % match.group(2))
