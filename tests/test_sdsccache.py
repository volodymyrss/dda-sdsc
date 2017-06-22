import sys
sys.path.append("/home/savchenk/work/sdsc/sdsc")
sys.path.append("/home/savchenk/work/dda/dda-ddosadm")

def test_store_restore():
    import dataanalysis.core as da
    from sdsc import SDSCCache, blob_store

    cache=SDSCCache()

    class Analysis(da.DataAnalysis):
        cached=True

    A=Analysis()

    A.data="somedata"
    hashe=('testhashe')

    cache.store(hashe,A)

    print(blob_store.blobs)

    #da.reset()

    #B = Analysis()

    #cache.restore(hashe,B)

    #assert B.data == A.data


def test_osa_blob():
    import dataanalysis.core as da

    from sdsc import SDSCCache, blob_store

    blob_store.purge()

    import ddosa

    cache=SDSCCache()

    im=ddosa.ii_skyimage(assume=[ddosa.ScWData(input_scwid="066500220010.001")])
    im.get()
    im.write_caches.append(cache.__class__)

    da.debug_output()
    cache.store(im._da_locally_complete,im)

    assert len(blob_store.blobs)==1

    blob=blob_store.blobs.items()[0][1]

    import tarfile
    import StringIO

    tar=tarfile.open(fileobj = StringIO.StringIO(blob))

    print tar.getnames()

    assert './blob/isgri_sky_res.fits.gz' in tar.getnames()

    #da.reset()

    #B = Analysis()

    #assert B.data == A.data
    #cache.restore(hashe,B)


def test_osa_scw_blob():
    import dataanalysis.core as da
    import subprocess

    from sdsc import SDSCCache, blob_store

    blob_store.purge()
    assert len(blob_store.blobs) == 0

    import ddosa

    import ddosadm


    cache = SDSCCache()

    scw = ddosadm.ScWData(input_scwid="066500220010.001")
    scw.read_caches=[]
    scw.write_caches.append(cache.__class__)

    try:
        scw.get()
    except subprocess.CalledProcessError:
        pass


    da.debug_output()
    cache.store(scw._da_locally_complete, scw)

    assert len(blob_store.blobs) == 1
    print blob_store.blobs.keys()

    blob = blob_store.blobs.items()[0][1]

    import tarfile
    import StringIO

    tar = tarfile.open(fileobj=StringIO.StringIO(blob))

    print tar.getnames()

    #assert './blob/isgri_sky_res.fits.gz' in tar.getnames()

    # da.reset()

    # B = Analysis()

    # assert B.data == A.data
