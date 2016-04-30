from lxml import html
from couchpotato.core.helpers.encoding import tryUrlencode, toUnicode
from couchpotato.core.helpers.variable import tryInt, getIdentifier
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
import traceback
import re
import time
import requests
import sys
import PTN

log = CPLog(__name__)

class TorrentDetails(object):
    def __init__(self, seeders, leechers, downlink, torrentname, filesize, quality, resolution, imdb, group, detail):
                self.seeders = seeders
                self.leechers = leechers
                self.downlink = downlink
                self.torrentname = torrentname
                self.filesize = filesize
                self.quality = quality
                self.resolution = resolution
                self.imdb = imdb
                self.group = group
                self.detail = detail
 
class PirateTheNet(TorrentProvider, MovieProvider):
    default_search_params = {
        'sort': 'browsedate',
        'skw': 'showall',
        'compression': 'unraredonly',
        'packs': 'torrentsonly',
        'titleonly': 'true',
        'subscriptions': 'showall',
        'visibility': 'aliveonly',
        'visiblecategories': 'Action,Adventure,Animation,Biography,Comedy,Crime,Documentary,Drama,Eastern,Family,Fantasy,'
                            'History,Holiday,Horror,Kids,Musical,Mystery,Romance,Sci-Fi,Short,Sports,Thriller,War,Western',
        'hiddenqualities': 'FLAC,MP3',
        'order': 'DESC',
        'action': 'torrentstable',
        'bookmarks': 'showall',
        'viewtype': 1,
        'page': 1
        }

    urls = {
        'baseurl': 'http://piratethe.net',
	'login': 'http://piratethenet.org/takelogin.php',
	'login_check': 'http://piratethe.net/index.php',
        'search': 'http://piratethenet.org/torrentsutils.php'
        }

    session = requests.Session()

    def _searchOnTitle(self, title, movie, quality, results):
        if not self.session.cookies or not self.session.passkey:
            try:
                r = self.session.post(self.urls['login'], data=self.getLoginParams(), verify=False)
            except requests.RequestException as e:
                log.info('Error while logging in to PtN: %s', e)
            passkey = re.search('passkey=([\d\w]+)"', r.text)
            if passkey:
                self.session.passkey = passkey.group(1)
            else:
                log.info('PtN cookie info invalid')
        search_params = self.default_search_params.copy()

        search_params['searchstring'] = title

        # SKW?
        if(self.conf('skw')):
            search_params['skw'] = 'skwonly'
            log.info("Searching for SKALiWAGZ only")
        try:
            r = self.session.get(self.urls['search'], params=search_params)
        except requests.RequestException as e:
            log.info('Error searching ptn: %s' % e)
            log.info(str(tree))

        tree = html.fromstring(r.content)
        # Get number of seeders
        seederList = tree.xpath('//a[@alt="Number of Seeders"]/text()')
            
        # Get number of leechers (doesn't work)
        leecherList = tree.xpath('//span[@alt="Number of Leechers"]/text()')

        # Get torrent size
        sizeList = tree.xpath('//span[@alt="Torrent size"]/text()')
            
        # Get download links and IMDB ID
        tDownload = tree.xpath('//a//@href')
        downloadList = []
        imdbDict = {}
        imdbCount = 0
        imdbList = []
        maxRun = 0
        detailList = []
        for dl in tDownload:
            if maxRun >= 20:
                break
            if "redir.php?url=http://imdb.com/title/" in dl:
                imdbDict.update({str(imdbCount) : dl[-9:]})
                imdbCount += 1
            if "download" in dl:
                downloadList.append(self.urls['baseurl']+dl)
                maxRun += 1
                imdbList.append(imdbDict[str(imdbCount-1)])
            if "detail.php" in dl and "&" not in dl:
                detailList.append(self.urls['baseurl']+dl[:7]+'s'+dl[7:])


            
        # Get torrent name
        tID = tree.xpath('//a[@class="lightview"]/text()')
        idList = []
        maxRun = 0
        for dl in tID:
            if maxRun >= 20:
                break
            if len(dl) > 5:
                idList.append(dl)
                maxRun += 1
        torrentList = []
        maxRun = min(len(seederList),maxRun)
        for i in range(0,maxRun):
            tmp = PTN.parse(idList[i])
            torrentdata = TorrentDetails(0,0,'','','','','','','','')
            torrentdata.seeders = int(seederList[i])
            torrentdata.leechers = 0
            torrentdata.downlink = str(downloadList[i])
            torrentdata.torrentname = str(idList[i])
            torrentdata.size = str(sizeList[i])
            torrentdata.detail = str(detailList[i])
            
            if("quality" in tmp):
                torrentdata.quality = str(tmp["quality"])
            if("resolution" in tmp):
                torrentdata.resolution = str(tmp["resolution"])
            if("group" in tmp):
                torrentdata.group = str(tmp["group"])
            torrentdata.imdb = str(imdbList[i])
            if(torrentdata.resolution == quality["custom"]["quality"] and torrentdata.imdb == movie["identifiers"]["imdb"]):
                torrentList.append(torrentdata)


        log.info('Found %d torrents' % len(torrentList))
        for torrent in torrentList:
            log.info('PirateTheNet found ' + torrent.torrentname)
            results.append({
                'leechers' : torrent.leechers,
                'seeders' : torrent.seeders,
                'name' : torrent.torrentname,
                'url' : torrent.downlink,
                'detail_url' : torrent.detail,
                'id' : '',
                'size' : self.parseSize(torrent.size)
                })

    def getLoginParams(self):
        return {
		'password': str(self.conf('password')),
		'loginkey': str(self.conf('key'))
               }
