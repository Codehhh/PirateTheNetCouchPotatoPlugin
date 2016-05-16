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
                              'type': 'password',
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
			  {
			      'name': 'pref_skw',
			      'label': 'Prefer SKALiWAGZ',
			      'defaults': False,
			      'type': 'bool',
			      'description': 'Prefer SKALiWAGZ torrents.',
			  },
			  {
		              'name': 'extra_score',
			      'advanced': True,
			      'label': 'Extra Score',
			      'type': 'int',
			      'default': 20,
			      'description': 'Starting score for releases found from PirateTheNet',
			  },
                      ],
                  },
              ],
          }]
