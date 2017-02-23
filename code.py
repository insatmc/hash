import sys
lines = tuple(open(sys.argv[1], 'r'))

firstLine = lines[0].split(" ")
nbrVideos =  int(firstLine[0])
nbrEndpoints = int(firstLine[1])
nbrReqDesc = int(firstLine[2])
nbrCache = int(firstLine[3])
capacityCache = int(firstLine[4].strip('\n'))

videos = lines[1].strip('\n').split(" ")

linecounter = 2
endpoints = []
for i in xrange(0,int(nbrEndpoints)):
    endpointLine = lines[linecounter].strip('\n').split(" ")
    linecounter = linecounter + 1
    cachesLatencies = []
    for j in xrange(0,int(endpointLine[1])):
        cachesLatencyLine = lines[linecounter].strip('\n').split(" ")
        cachesLatencies.append({
            "id" : cachesLatencyLine[0],
            "latency" : cachesLatencyLine[1]
        })
        linecounter = linecounter + 1
    endpoints.append({
        "latency" : endpointLine[0],
        "caches" : cachesLatencies
    })

requests = []
for i in xrange(0,int(nbrReqDesc)):
    reqDescLine = lines[linecounter].strip('\n').split(" ")
    linecounter = linecounter + 1
    requests.append({
        "id_video" : int(reqDescLine[0]),
        "id_endpoint" : int(reqDescLine[1]),
        "nbr" : int(reqDescLine[2])
    })



print("Reading File ended")

nbrCachesUsed = 0
cachesUse = []



videos_endpoints = []
for x in xrange(0,nbrVideos):
    thisendpoints = []
    for y in xrange(0,len(requests)):
        if requests[y]["id_video"] == x:
            thisendpoints.append({
                "id": requests[y]["id_endpoint"],
                "nbr": requests[y]["nbr"]
            })
    videos_endpoints.append({
        "size": int(videos[x]),
        "endpoints" : thisendpoints
    })

print("Mapping videos with endpoints")


def sumReq(i,j):
    summ = 0
    vid = videos_endpoints[i]
    for x in xrange(0,len(vid["endpoints"])):
        ishere = False
        for y in xrange(0, len( caches_endpoints[j]['endpoints'] ) ):
            if vid["endpoints"][x]["id"] == caches_endpoints[j]['endpoints'][y]['id']:
                ishere = True
                break;
        if ishere:
            summ = summ + vid["endpoints"][x]["nbr"]

caches_endpoints = []
for x in xrange(0,nbrCache):
    thisendpoints = []
    for y in xrange(0,len(endpoints)):
        for w in xrange(0,len(endpoints[y]["caches"])):
            if int(endpoints[y]["caches"][w]["id"]) == x:
                thisendpoints.append({
                    "id": y
                })
    caches_endpoints.append({
        "capacity": capacityCache,
        "endpoints" : thisendpoints
    })


for x in xrange(0,nbrCache):
    videosToAdd = []
    for y in xrange(0,nbrVideos):
        counter = 0
        for i in xrange(0,len(caches_endpoints[x]["endpoints"])):
            for j in xrange(0,len(videos_endpoints[y]["endpoints"])):
                if caches_endpoints[x]["endpoints"][i]["id"] == videos_endpoints[y]["endpoints"][j]["id"]:
                    counter = counter + 1
        if counter > 0:
            if caches_endpoints[x]["capacity"] >= videos_endpoints[y]["size"]:
                videosToAdd.append(y)
                caches_endpoints[x]["capacity"] = caches_endpoints[x]["capacity"] - videos_endpoints[y]["size"]
            else:
                # check if how ahem meli mawjoudin:
                # nbr request akber mel lokhryn

                videosToAdd.append(y)
                X = x
                # sort table by sum of request
                for k in xrange(0,len(videosToAdd)):
                    maxx = k
                    for l in xrange(k,len(videosToAdd)):
                        if sumReq(videosToAdd[l],X) > sumReq(videosToAdd[maxx],X):
                            maxx = l
                    old = videosToAdd[k]
                    videosToAdd[k] = videosToAdd[maxx]
                    videosToAdd[maxx] = old
                newvideosToAdd = []
                load = 0
                i = 0
                while(load <= capacityCache):
                    if i< len(videosToAdd) and load + int(videos[videosToAdd[i]]) <= capacityCache:
                        newvideosToAdd.append(videosToAdd[i])
                        load = load + int(videos[videosToAdd[i]])
                        i = i + 1
                    else:
                        break
                videosToAdd = newvideosToAdd
                caches_endpoints[x]["capacity"] = capacityCache - load


    if len(videosToAdd) > 0:
        nbrCachesUsed = nbrCachesUsed + 1

    cachesUse.append(videosToAdd)

print("Mapping caches with video")


f = open('restout-'+sys.argv[1], 'w')
f.write(str(nbrCachesUsed)+ '\n')
for x in xrange(0,nbrCache):
    if len(cachesUse[x]) > 0:
        videosCh = ""
        for y in xrange(0,len(cachesUse[x])):
            videosCh = videosCh +  str(cachesUse[x][y]) + " "
        f.write( str(x) + ' ' +  videosCh.strip(' ') + '\n')
f.close()
