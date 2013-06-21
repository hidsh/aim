# -*- coding: utf-8 -*-

import gdata.youtube
import gdata.youtube.service

client = gdata.youtube.service.YouTubeService()
query = gdata.youtube.service.YouTubeVideoQuery()

query.vq = 'ガールズ＆パンツァー girls und panzer'
query.max_results = 25
query.start_index = 1
query.racy = 'exclude'
#query.format = 6 # 1 # 5
query.orderby = 'relevance'

feed = client.YouTubeQuery(query)

for entry in feed.entry:
	print entry.title.text
print '-- Found %d entries' % len(feed.entry)
