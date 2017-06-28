import tarfile
import StringIO
import sys
sys.path.append("/home/savchenk/work/sdsc/sdsc")
sys.path.append("/home/savchenk/work/dda/dda-ddosadm")


def test_store_restore():
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



