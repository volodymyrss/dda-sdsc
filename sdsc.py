import dataanalysis.caches.cache_core as caches_core


class BlobStorage(object):
    blobs={}

    def put_blob(self,key,blob):
        self.blobs[key]=blob

    def get_blob(self, key):
        return self.blobs[key]

    def purge(self):
        self.blobs={}

blob_store=BlobStorage()

class SDSCCache(caches_core.Cache):
    #def store(self):
    #    pass

    #def restore(self):
    #def store(self):
    def store_object_content(self,hashe,obj):
        blob=self.assemble_blob(hashe,obj).read()
        blob_store.put_blob(hashe,blob) # deliver blob

    def make_record(self,*args,**kwargs):
        pass
