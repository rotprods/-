import hashlib,io,pathlib,sys,tempfile,unittest,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tools'))
from bootstrap_godot import install

class Bootstrap(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.dest=pathlib.Path(self.temp.name)
        self.payload=b'qualified test executable';data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:z.writestr('engine',self.payload);z.writestr('../escape','forbidden')
        self.archive=data.getvalue()
        self.lock={'url':'https://example.invalid/fixture','binary':'engine','binary_sha256':hashlib.sha256(self.payload).hexdigest(),'archive_sha256':hashlib.sha256(self.archive).hexdigest(),'archive_size':len(self.archive)}
    def tearDown(self):self.temp.cleanup()
    def opener(self,*args,**kwargs):return io.BytesIO(self.archive)
    def test_valid_extract_only_expected_executable(self):
        out=install(self.dest,self.lock,self.opener);self.assertEqual(out.read_bytes(),self.payload);self.assertEqual(list(self.dest.iterdir()),[out])
    def test_archive_checksum_rejected(self):
        self.lock['archive_sha256']='0'*64
        with self.assertRaises(ValueError):install(self.dest,self.lock,self.opener)
        self.assertFalse((self.dest/'engine').exists())
    def test_binary_checksum_rejected(self):
        self.lock['binary_sha256']='0'*64
        with self.assertRaises(ValueError):install(self.dest,self.lock,self.opener)
        self.assertFalse((self.dest/'engine').exists())
    def test_truncated_download_rejected(self):
        with self.assertRaises(ValueError):install(self.dest,self.lock,lambda *a,**kw:io.BytesIO(self.archive[:-10]))
    def test_existing_foreign_binary_preserved(self):
        (self.dest/'engine').write_bytes(b'user binary')
        with self.assertRaises(ValueError):install(self.dest,self.lock,self.opener)
        self.assertEqual((self.dest/'engine').read_bytes(),b'user binary')
    def test_matching_install_does_not_redownload(self):
        install(self.dest,self.lock,self.opener)
        def fail(*a,**kw):raise AssertionError('unexpected download')
        self.assertEqual(install(self.dest,self.lock,fail).read_bytes(),self.payload)
    def test_oversized_download_rejected(self):
        self.lock['archive_size']-=1
        with self.assertRaises(ValueError):install(self.dest,self.lock,self.opener)

if __name__=='__main__':unittest.main()
