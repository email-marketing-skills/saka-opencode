#!/usr/bin/env python3
"""Check public Saka contracts without credentials, account data or purchases."""
import json, subprocess

def fetch(url, body=None):
    args=['curl','--fail-with-body','--silent','--show-error','--max-time','30',url]
    if body is not None:
        args+=['-H','Content-Type: application/json','--data',json.dumps(body)]
    return json.loads(subprocess.check_output(args,text=True))

if __name__=='__main__':
    q=fetch('https://saka.run/api/sandbox/quote',{'kind':'basic','limit':2,'filters':{'country':['US'],'category':['Plumbing']}})
    assert q['sandbox'] is True and q['can_purchase'] is False and q['charged_micro']==0,q
    for suffix in ['api/mcp','api/library/mcp']:
        r=fetch('https://saka.run/.well-known/oauth-protected-resource/'+suffix)
        assert r['resource']=='https://saka.run/'+suffix and r['authorization_servers'],r
    print('PASS: fictional sandbox, zero charge, purchasing disabled, both OAuth resource audiences.')
