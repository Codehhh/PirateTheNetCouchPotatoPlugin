from .main import PirateTheNet


def autoload():
    return PirateTheNet()


config = [{
              'name': 'piratethenet',
              'groups': [
                  {
                      'tab': 'searcher',
                      'list': 'torrent_providers',
                      'name': 'PirateTheNet',
                      'description': 'See <a href="http://piratethe.net/">PirateTheNet</a>',
                      'wizard': True,
		      'icon': '',
                      'options': [
                          {
                              'name': 'enabled',
                              'type': 'enabler',
                              'default': False,
                          },
                          {
                              'name': 'key',
                              'default': '',
                          },
                          {
                              'name': 'password',
                              'default': '',
                              'type': 'password',
                          },
                          {
                              'name': 'skw',
                              'label': 'SKALiWAGZ Only',
                              'default': False,
                              'type': 'bool',
                              'description': 'Only searches for SKALiWAGZ torrents.',
                          },
                      ],
                  },
              ],
          }]
