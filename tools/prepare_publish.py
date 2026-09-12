"""Prepare bounded Git tree input for the authenticated connector; never handle credentials."""
from pathlib import Path
import hashlib,json,subprocess
from project_control import ROOT,tracked_files,check

def prepare(root):
    problems=check(root)
    if problems:raise ValueError('publication gates failed: '+str(problems))
    parent=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    current=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
    rows=[]
    for p in tracked_files(root):
        rel=str(p.relative_to(root));data=p.read_bytes()
        sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        old=subprocess.run(['git','rev-parse',parent+':'+rel],cwd=root,capture_output=True,text=True)
        if old.returncode==0 and old.stdout.strip()==sha:continue
        row={'path':rel,'mode':'100644','type':'blob'}
        try:row['content']=data.decode('utf-8')
        except UnicodeDecodeError:row['sha']=sha
        rows.append(row)
    for name in current:
        if name and not (root/name).exists():rows.append({'path':name,'mode':'100644','type':'blob','sha':None})
    folder=root/'.tools/publish';folder.mkdir(parents=True,exist_ok=True)
    batches=[];batch=[];size=0
    for row in rows:
        length=len(json.dumps(row,ensure_ascii=False).encode())
        if batch and size+length>400000:batches.append(batch);batch=[];size=0
        batch.append(row);size+=length
    if batch:batches.append(batch)
    for i,batch in enumerate(batches):(folder/f'tree-{i}.json').write_text(json.dumps(batch,ensure_ascii=False))
    summary={'repository':'rotprods/-','expected_parent':parent,'changed_files':len(rows),'batches':len(batches),'binary_blobs_to_reconcile':[r for r in rows if r.get('sha')],'directory':str(folder)}
    (folder/'prepared.json').write_text(json.dumps(summary,indent=2)+'\n');return summary
if __name__=='__main__':print(json.dumps(prepare(ROOT),indent=2))
