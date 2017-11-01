from __future__ import print_function

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
    
    
    def get_bucket(self):
        buckets=[]
        for bucket in client.buckets.list():
            print(bucket)
            buckets.append(bucket)

        bucket_of_choice=buckets[0]

        print("choosing bucket:",bucket_of_choice)

        return bucket_of_choice

    def filename_for_key(self,key):
        return "test/astronomy/integral/" + key

    def put_blob(self,key,blob):
        print(key)
        self.keys.append(key)

        bucket=self.get_bucket()
        filename=self.filename_for_key(key)

        with bucket.files.open(filename, 'w') as fp:
            fp.write(blob)

        print("uploaded",len(blob)/1024,"kb to",filename,"at",bucket)

    def get_blob(self,key):
        print(key)
        self.keys.append(key)

        bucket = self.get_bucket()
        filename = self.filename_for_key(key)

        with bucket.files.open(filename) as fp:
            blob=fp.read()

        print("downloaded",len(blob)/1024,"kb from",filename,"at",bucket)

        return blob


class SDSCCache(caches_core.Cache):

    blob_store=blob_store

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