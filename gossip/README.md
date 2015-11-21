Format of Config File and Initial Config:
http://docs.hcs.ufl.edu/pubs/GEMS2005.pdf

'''
gossip_list:
    - 1
    - 5
    ...
suspect_list:
    - 0
    - 1
    ...
suspect_matrix:
    -
        - 0
        - 0
        - 1
    -
        - 1
        - 0
        - 1
servers:
    -
        address:
        port:
my_config:
    address:
    port:


'''


Basic Gossip Procedure:
   For Gossiper:
      On each gossip interval, increase the heart beat of nodes you have not talked to
   For Server:
      When you receive a request do the following:
         Update your Gossip list to be min of the two gossip lists
         Update your suspect vector based off of your updated gossip list
         Update your Suspect Matrix based off of suspect matrix and gossip list passed
