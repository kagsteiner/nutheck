"""Source-only regression checks, with independent MSVC preprocessing when requested."""
import hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Scripts'))
import CreateObjectCatalogue as c

def main():
    rows=c.source_objects();byid={r['id']:r for r in rows}
    assert len(rows)==485 and len(byid)==485
    assert byid['SPE_DIG']['fields']['material']=='LEATHER'
    assert byid['SPE_MAGIC_MISSILE']['fields']['material']=='LEATHER'
    assert byid['SPE_FIREBALL']['fields']['material']=='PAPER'
    assert byid['LONG_SWORD']['source_class']=='WEAPON_CLASS'
    assert byid['PICK_AXE']['source_class']=='TOOL_CLASS'
    assert byid['SCR_MAIL']['scope']=='conditional'
    assert byid['SHIMMERING_DRAGON_SCALES']['scope']=='deferred'
    assert byid['SC01']['record_kind']=='appearance_only' and byid['WAN3']['record_kind']=='appearance_only'
    groups=c.shuffle_groups(rows)
    assert 'POT_WATER' not in groups['potion_appearances'] and 'POT_HEALING' in groups['potion_appearances']
    assert 'SC01' in groups['scroll_appearances'] and 'SCR_BLANK_PAPER' not in groups['scroll_appearances']
    assert 'WAN3' in groups['wand_appearances']
    assert 'SPEED_BOOTS' in groups['speed_boots_appearances'] and 'LOW_BOOTS' not in groups['speed_boots_appearances']
    assert byid['HELM_OF_BRILLIANCE']['id'] not in groups['helmet_appearances']
    old=c.OUT
    with tempfile.TemporaryDirectory() as tmp:
        c.OUT=Path(tmp);c.main();data=json.loads((c.OUT/'objects.json').read_text(encoding='utf-8'))
        assert data['summary']['named_object_types']==440 and data['summary']['verified_object_drafts']==4
        assert data['summary']['official_object_tiles']==483
        assert {r['id'] for r in data['objects'] if r['asset_status']=='generated and verified static draft'}=={'LARGE_BOX','CHEST','GOLD_PIECE','CORPSE'}
        appearances=json.loads((c.OUT/'appearances.json').read_text(encoding='utf-8'))['appearances'];assert len(appearances)==463
        assert next(a for a in appearances if a['source_slot_id']=='POT_HEALING')['label']=='purple-red'
        assert next(r for r in data['objects'] if r['id']=='SPE_POLYMORPH')['official_tile']['file_local_index']==401
        assert next(r for r in data['objects'] if r['id']=='WAN_POLYMORPH')['official_tile']['file_local_index']==424
        art=json.loads((c.OUT/'artifacts.json').read_text())['artifacts'];assert sum(a['scope']=='normal' for a in art)==33
        assert next(a for a in art if a['id']=='ART_EXCALIBUR')['base_object_id']=='LONG_SWORD'
    c.OUT=old
    if '--cpp' in sys.argv:
        compiler=Path(sys.argv[sys.argv.index('--cpp')+1])
        def cpp(mode,mail):
            return subprocess.run([str(compiler),'/nologo','/EP','/TC','/D'+mode]+(['/DMAIL_STRUCTURES'] if mail else [])+[str(c.ROOT/'upstream/NetHack/include/objects.h')],capture_output=True,text=True,check=True).stdout
        for mail in [False,True]:
            active=[r for r in rows if r['scope']!='deferred' and (mail or r['id']!='SCR_MAIL')]
            actual=re.findall(r'\{\s*([A-Z][A-Z0-9_]*)\s*,\s*"[A-Z0-9_]+"\s*\}',cpp('DUMP_ENUMS',mail))
            assert actual==[r['id'] for r in active],(len(actual),len(active))
            pairs=[]
            for body in re.findall(r'\{([^{}]*)\}',cpp('OBJECTS_DESCR_INIT',mail)):
                args=c.split_args(body)
                if len(args)==2:
                    pair=[c.cstring(x) for x in args]
                    if pair!=[None,None]:pairs.append(pair)
            assert pairs==[[r['name'],r['default_description']] for r in active],(len(pairs),len(active))
        print('OBJECT_CPP_CROSSCHECK_PASS both MAIL_STRUCTURES configurations; every active enum/name/description')
    print('OBJECT_CATALOGUE_TESTS_PASS source_expansion appearance_pools tiles scopes artifacts existing_drafts')

if __name__=='__main__':main()
