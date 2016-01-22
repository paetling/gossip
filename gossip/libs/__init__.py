"""
Based off of this paper: http://docs.hcs.ufl.edu/pubs/GEMS2005.pdf
Server configs document looks like the following dictionary:
    {'servers': [{'address': '',
                  'port': ''},
                  ...
                ],
     'gossip_list': [int, ...],
     'suspect_list': [int, ...],
     'suspect_matrix': [[<suspect_list>], ...]}
'servers': contains how to reach each server
'gossip_list': contains last time a particular server talked to the other servers
'suspect_list': contains who a particular server thinks is down
'suspect_matrix': contains what a particular server thinks all servers think about what servers are down
                  (it is an aggregation of all servers suspect list)
NOTE: All lists should be the exact same length

{'server_configs': server_configs}
"""
