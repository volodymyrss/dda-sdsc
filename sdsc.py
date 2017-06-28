import dataanalysis.caches.cache_core as caches_core
import ddosa
import requests
import os

class BlobStorage(object):
    blobs={}

    def put_blob(self,key,blob):
        self.blobs[key]=blob

    def get_blob(self, key):
        return self.blobs[key]

    def purge(self):
        self.blobs={}

blob_store=BlobStorage()

import urllib

class SDSCStorageInterface:
    keys=[]

    def get_token(self):
        if "OPENID_TOKEN" in os.environ:
            return os.environ["OPENID_TOKEN"]

        if "OPENID_TOKEN_FILE" in os.environ:
            token_file=os.environ["OPENID_TOKEN_FILE"]
        else:
            token_file=os.environ["HOME"] + "/.sdsc-token"

        return open(token_file).read().strip()


    def put_blob(self,key,blob):
        print key
        self.keys.append(key)

        url='https://testing.datascience.ch:9000/write/'+urllib.quote_plus("test/astronomy/integral/"+key)

        res = requests.post(url=url,
                            data=blob,
                            headers={'Content-Type': 'application/octet-stream',
                                     'Authorization':'Bearer '+self.get_token()},verify=False)

        print "uploaded",len(blob)/1024,"kb to",url

    def get_blob(self,key):
        url='https://testing.datascience.ch:9000/read/' + urllib.quote_plus("test/astronomy/integral/"+key)
        res = requests.get(url=url,
                           headers={'Authorization': 'Bearer ' + open(
                               "/home/savchenk/work/sdsc/sdsc/gettoken/token").read().strip()}, verify=False)

        print "downloaded",len(res.content)/1024,"kb from",url

        return res.content


class SDSCCache(caches_core.Cache):

    blob_store=blob_store

    #def store(self):
    #    pass

    #def restore(self):
    #def store(self):
    def store_object_content(self,hashe,obj):
        key=ddosa.MemCacheIntegralFallback().hashe2signature(hashe)

        blob=self.assemble_blob(hashe,obj).read()

        self.blob_store.put_blob(key,blob) # deliver blob

    def make_record(self,*args,**kwargs):
        pass

import ddosa
import ddosadm

cache=SDSCCache()
cache.blob_store=SDSCStorageInterface()
ddosa.CacheStack[-1].parent=cache

ddosa.CatExtract.write_caches.append(cache.__class__)