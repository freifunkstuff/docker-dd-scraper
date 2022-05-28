#!/usr/bin/env python3

import requests, json, datetime
nodes = requests.get("https://meshviewer.freifunk-dresden.de/data/nodes.json").json()
graph = requests.get("https://meshviewer.freifunk-dresden.de/data/graph.json").json()

nodes_le={
    'timestamp': nodes['timestamp'],
    'nodes': [],
    'links': []
}

def nodeid(id):
    id=str(id)
    return 'dd0000000000'[0:12-len(id)]+id

node_ids=[]

for n in nodes['nodes']:
    if n['nodeinfo']['system']['site_code']!='Leipzig':
        node_ids.append(None)
        continue
    node_ids.append(nodeid(n['nodeinfo']['node_id']))
    node={
        'addresses': n['nodeinfo']['network']['addresses'],
        'node_id': nodeid(n['nodeinfo']['node_id']),
        'hostname': n['nodeinfo']['hostname'],
        'firstseen': n['firstseen'],
        'lastseen': n['lastseen'],
        'clients': n['statistics']['clients'],
        'clients_other': 0,
        'clients_wifi5': 0,
        'clients_wifi24': 0,
        'owner': n['nodeinfo']['owner']['contact'],
        'autoupdater': n['nodeinfo']['software']['autoupdater'],
        'is_online': n['flags']['online'],
        'is_gateway': n['flags']['gateway'],
        'domain': 'Leipzig (ddfw)',
        'mac': n['nodeinfo']['node_id'],
        'firmware': n['nodeinfo']['software']['firmware'],
        'autoupdater': n['nodeinfo']['software']['autoupdater'],
        'model': n['nodeinfo']['hardware']['model'],
        'loadavg': n['statistics'].get('loadavg',0.0),
        'memory_usage': n['statistics'].get('memory_usage',0.0),
    }
    if 'location' in n['nodeinfo']:
        node['location']= n['nodeinfo']['location']
    if 'uptime' in n['statistics']:
        node['uptime']=(datetime.datetime.now()-datetime.timedelta(seconds=n['statistics']['uptime'])).strftime('%Y-%m-%dT%H:%M:%S'),
    if 'gateway' in n['statistics']:
        node['gateway']=n['statistics']['gateway']
        node['gateway_nexthop']=n['statistics']['gateway']

    nodes_le['nodes'].append(node)

inverse_links={}

for l in graph['batadv']['links']:
    source_id=node_ids[l['source']]
    if source_id is None:
        continue
    target_id=node_ids[l['target']]
    if target_id is None:
        continue
    if "%s-%s-%s"%(target_id,source_id,l['type']) in inverse_links:
        inverse_links["%s-%s-%s"%(target_id,source_id,l['type'])]['target_tq']=1/l['tq']
        continue;
    link={
        'source': source_id,
        'target': target_id,
        'type': l['type'],
        'source_tq': 1/l['tq'],
        'target_tq': 1/l['tq'],
    }
    nodes_le['links'].append(link)
    inverse_links["%s-%s-%s"%(source_id,target_id,l['type'])]=link


#nodes_le=list(filter(lambda n: n['nodeinfo']['system']['site_code']=='Leipzig',nodes['nodes']))
#nodes['nodes']=nodes_le
#nodes['links']=[]
#node_ids=list(node['node_id'] for node in nodes_le)
#print(node_ids)
#print(json.dumps(graph['batadv']['nodes']))
#print(json.dumps(graph['batadv']['nodes']))

#print(node_ids)

print(json.dumps(nodes_le))

