import tarfile
import StringIO
import sys
sys.path.append("/home/savchenk/work/sdsc/sdsc")
sys.path.append("/home/savchenk/work/dda/dda-ddosadm")


def test_store_restore():
    return

    import dataanalysis.core as da
    from sdsc import SDSCCache, blob_store, SDSCStorageInterface
    import ddosa
    import ddosadm
    import subprocess

    cache=SDSCCache()
    cache.blob_store=SDSCStorageInterface()

    im = ddosadm.ScWData(input_scwid="066500230010.001")
    #im = ddosa.BinEventsImage(assume=[ddosa.ScWData(input_scwid="066500220010.001")])

    try:
        im.get()
    except subprocess.CalledProcessError:
        pass
    im.write_caches.append(cache.__class__)

    cache.store(im._da_locally_complete, im)

    assert len(cache.blob_store.keys) == 1

    key=cache.blob_store.keys[0]
    print "key:",key

    blob=cache.blob_store.get_blob(key)

    tar = tarfile.open(fileobj=StringIO.StringIO(blob))

    print tar.getnames()



def test_store_restore_in_analysis():
    import dataanalysis.core as da
    import sdsc
    import ddosa
    import ddosadm
    import subprocess

    scw = ddosadm.ScWData(input_scwid="066500230010.001")
    obj = ddosa.BinEventsImage(assume=[ddosa.ScWData(input_scwid="066500220010.001")])

    c=obj.cache
    found_sdsc=False
    while c is not None:
        print("cache:",c)
        c=c.parent
        if c==sdsc.cache: found_sdsc=True

    assert found_sdsc
    assert sdsc.cache.__class__  in obj.write_caches
    assert obj.cached

    try:
        obj.get()
    except subprocess.CalledProcessError:
        pass

    key=sdsc.cache.blob_store.keys[0]
    print "key:",key

    blob=sdsc.cache.blob_store.get_blob(key)

    tar = tarfile.open(fileobj=StringIO.StringIO(blob))

    print tar.getnames()



