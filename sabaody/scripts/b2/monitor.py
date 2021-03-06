# B2 monitor
from __future__ import print_function, division, absolute_import

from sabaody import getQualifiedName

from asciimatics.screen import Screen
from toolz import partial
from pymemcache.client.base import Client
mc_host = 'luna'
mc_port = 11211
client = Client((mc_host,mc_port))

from time import sleep
from json import dumps, loads
from pprint import PrettyPrinter
from time import time

def app(screen):
    while True:
        run = int(client.get('com.how2cell.sabaody.B2.run'))
        run_id = client.get('com.how2cell.sabaody.B2.runId').decode('utf8')
        status = client.get('com.how2cell.sabaody.B2.run.status').decode('utf8').lower()
        started = float((client.get('com.how2cell.sabaody.B2.run.startTime') or b'0').decode('utf8'))
        stopped = float((client.get('com.how2cell.sabaody.B2.run.endTime') or b'0').decode('utf8'))
        active = bool(status == 'active')
        if active:
            runtime = time()-started
        else:
            runtime = stopped-started
        if run_id:
            domain_qualifier = partial(getQualifiedName, 'B2', str(run_id))
            def get(*args):
                return client.get(domain_qualifier(*args))
            island_ids = [i for i in loads(get('islandIds') or '[]')]

            pp = PrettyPrinter(indent=2)

            v = int(screen.height/2)-10
            screen.print_at('Run {}   /   {}    '.format(run, run_id),
                            int(screen.width/2)-65, v,
                            Screen.COLOUR_WHITE)
            v += 1
            screen.print_at('Status: {}    '.format(status.upper()),
                            int(screen.width/2)-65, v,
                            Screen.COLOUR_GREEN if status == 'active' else Screen.COLOUR_WHITE if status == 'finished' else Screen.COLOUR_RED)
            v += 1
            screen.print_at('Run time: {:.0f} s    '.format(runtime),
                            int(screen.width/2)-65, v,
                            Screen.COLOUR_GREEN if status == 'active' else Screen.COLOUR_WHITE if status == 'finished' else Screen.COLOUR_RED)
            v += 1
            screen.print_at('Islands ({}):'.format(len(island_ids)),
                            int(screen.width/2)-65, v,
                            Screen.COLOUR_WHITE)
            v += 1
            for i in island_ids:
                screen.print_at(i, int(screen.width/2)-55, v, Screen.COLOUR_WHITE)
                v+=1
        else:
            screen.print_at('No run id'.format(run),
                            0, 0,
                            colour=Screen.COLOUR_WHITE)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()
        sleep(1)

Screen.wrapper(app)