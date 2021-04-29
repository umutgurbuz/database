import requests

class couchbase_server:
  def __init__(self,ip_address,user_name,password):
    self.ip_address = ip_address
    self.user_name = user_name
    self.password = password
  def bucket_details(self): #bucket details function that makes a get requests to /pools/default/buckets and returns the response
    url="http://{}:8091/pools/default/buckets".format(self.ip_address)
    return requests.get(url, auth=(self.user_name, self.password)).json()


cluster1 = couchbase_server('localhost','node1','password') # creating an object of couchbase_server class
print(cluster1.bucket_details()) 


