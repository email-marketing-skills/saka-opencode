import importlib.util,json,tempfile,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('installer',Path(__file__).resolve().parents[1]/'scripts/install-opencode.py')
i=importlib.util.module_from_spec(s);s.loader.exec_module(i)
class InstallTests(unittest.TestCase):
 def test_preserves_existing_and_is_repeatable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'opencode.json').write_text(json.dumps({'model':'owner/model','mcp':{'other':{'type':'remote','url':'https://example.org/mcp'}}}))
   i.install(p);before=(p/'opencode.json').read_bytes();i.install(p)
   self.assertEqual(before,(p/'opencode.json').read_bytes());cfg=json.loads(before)
   self.assertEqual(cfg['model'],'owner/model');self.assertIn('other',cfg['mcp']);self.assertEqual(len(list((p/'.opencode/skills').glob('*/SKILL.md'))),10)
 def test_conflicting_mcp_preserves_everything(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);old='{"mcp":{"saka":{"url":"https://example.org"}}}';(p/'opencode.json').write_text(old)
   with self.assertRaises(ValueError):i.install(p)
   self.assertEqual((p/'opencode.json').read_text(),old);self.assertFalse((p/'.opencode').exists())
 def test_conflicting_skill_is_preflighted(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);dest=p/'.opencode/skills/saka-business';dest.mkdir(parents=True);(dest/'SKILL.md').write_text('owner work')
   with self.assertRaises(ValueError):i.install(p)
   self.assertFalse((p/'opencode.json').exists());self.assertEqual(list((p/'.opencode/skills').iterdir()),[dest])
 def test_jsonc_and_symlink_refused(self):
  for kind in ['jsonc','symlink']:
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)
    if kind=='jsonc':(p/'opencode.jsonc').write_text('// owner comments')
    else:(p/'.opencode').symlink_to(p/'outside')
    with self.assertRaises(ValueError):i.install(p)
    self.assertFalse((p/'opencode.json').exists())
if __name__=='__main__':unittest.main()
