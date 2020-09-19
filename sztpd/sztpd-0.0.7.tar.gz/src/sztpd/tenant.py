# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_U='wn-sztpd-x:'
_T='Unable to parse "input" JSON document: '
_S='malformed-message'
_R='wn-sztpd-x'
_Q='/wn-sztpd-x:tenants/tenant=[^ ]*'
_P='/wn-sztpd-x:tenants/tenant=[^/]*/'
_O='Top node names must begin with the "wn-sztpd-1" prefix.'
_N='application'
_M='wn-sztpd-1'
_L='name'
_K='wn-sztpd-1:'
_J='/wn-sztpd-x:tenants/tenant/0/'
_I='Non-root data_paths must begin with "/wn-sztpd-1:".'
_H='wn-sztpd-x:tenant'
_G='invalid-value'
_F='protocol'
_E=':'
_D='/wn-sztpd-x:tenants/tenant='
_C=None
_B='/wn-sztpd-1:'
_A='/'
import re,json,datetime,basicauth
from aiohttp import web
from passlib.hash import sha256_crypt
from .  import yl
from .  import dal
from .  import utils
from .rcsvr import RestconfServer
from .handler import RouteHandler
class TenantViewHandler(RouteHandler):
	def __init__(A,native):A.native=native
	async def _check_auth(C,request):
		K='access-denied';J='comment';I='failure';H='outcome';E=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A['method']=E.method;A['path']=E.path;L=E.headers.get('AUTHORIZATION')
		if L is _C:A[H]=I;A[J]='No authorization specified in the HTTP header.';await C.native._insert_audit_log_entry(_C,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		F,O=basicauth.decode(L);R=_C
		try:G=await C.native.dal.get_tenant_name_for_admin(F)
		except dal.NodeNotFound as S:A[H]=I;A[J]='Unknown admin: '+F;await C.native._insert_audit_log_entry(_C,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		if G==_C:A[H]=I;A[J]='Host-level admins cannot use tenant interface ('+F+').';await C.native._insert_audit_log_entry(_C,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		P=_A+C.native.dal.app_ns+':tenants/tenant='+G+'/admin-accounts/admin-account='+F+'/password';Q=await C.native.dal.handle_get_config_request(P);M=Q[C.native.dal.app_ns+':password'];assert M.startswith('$5$')
		if not sha256_crypt.verify(O,M):A[H]=I;A[J]='Password mismatch for admin '+F;await C.native._insert_audit_log_entry(G,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		A[H]='success';await C.native._insert_audit_log_entry(G,A);N=web.Response(status=200);N.text=G;return N
	async def handle_get_opstate_request(E,request):
		F=request;B,K=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_operational:]);A=await E._check_auth(F)
		if A.status==401:return A
		G=A.text;A=await E.native.check_headers(F)
		if A!=_C:return A
		if B=='/ietf-yang-library:yang-library':D=web.Response(status=200);D.content_type='application/yang-data+json';D.text=getattr(yl,'nbi_x_tenant')();return D
		assert B==_A or B.startswith(_B)
		if B==_A:L=_D+G
		else:
			if not B.startswith(_B):D=web.Response(status=400);P=utils.gen_rc_errors(_F,_G,error_message=_I);D.text=json.dumps(P);return D
			S,M=B.split(_E,1);assert M!=_C;L=_D+G+_A+M
		N=dict()
		for O in K.keys():N[O]=re.sub(_B,_D+G+_A,K[O])
		A,C=await E.native.handle_get_opstate_request_lower_half(L,N)
		if C!=_C:
			assert A.status==200;H={}
			if B==_A:
				for I in C[_H][0].keys():
					if I==_L:continue
					H[_K+I]=C[_H][0][I]
			else:J=next(iter(C));assert J.count(_E)==1;Q,R=J.split(_E);assert Q==_R;assert type(C)==dict;assert len(C)==1;H[_K+R]=C[J]
			A.text=json.dumps(H,indent=2)
		return A
	async def handle_get_config_request(D,request):
		E=request;C,J=utils.parse_raw_path(E._message.path[RestconfServer.len_prefix_running:]);A=await D._check_auth(E)
		if A.status==401:return A
		F=A.text;A=await D.native.check_headers(E)
		if A!=_C:return A
		assert C==_A or C.startswith(_B)
		if C==_A:K=_D+F
		else:
			if not C.startswith(_B):L=web.Response(status=400);P=utils.gen_rc_errors(_F,_G,error_message=_I);L.text=json.dumps(P);return L
			S,M=C.split(_E,1);assert M!=_C;K=_D+F+_A+M
		N=dict()
		for O in J.keys():N[O]=re.sub(_B,_D+F+_A,J[O])
		A,B=await D.native.handle_get_config_request_lower_half(K,N)
		if B!=_C:
			assert A.status==200;G={}
			if C==_A:
				for H in B[_H][0].keys():
					if H==_L:continue
					G[_K+H]=B[_H][0][H]
			else:I=next(iter(B));assert I.count(_E)==1;Q,R=I.split(_E);assert Q==_R;assert type(B)==dict;assert len(B)==1;G[_K+R]=B[I]
			A.text=json.dumps(G,indent=2)
		return A
	async def handle_post_config_request(F,request):
		D=request;G,J=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_running:]);B=await F._check_auth(D)
		if B.status==401:return B
		H=B.text;B=await F.native.check_headers(D)
		if B!=_C:return B
		if G==_A:K=_D+H
		else:
			if not G.startswith(_B):A=web.Response(status=400);C=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(C);return A
			S,L=G.split(_E,1);assert L!=_C;K=_D+H+_A+L
		M=dict()
		for N in J.keys():M[N]=re.sub(_B,_D+H+_A,J[N])
		try:E=await D.json()
		except json.decoder.JSONDecodeError as O:A=web.Response(status=400);C=utils.gen_rc_errors(_F,_S,error_message=_T+str(O));A.text=json.dumps(C);return A
		assert type(E)==dict;assert len(E)==1;I=next(iter(E));assert I.count(_E)==1;P,Q=I.split(_E)
		if P!=_M:A=web.Response(status=400);C=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(C);return A
		R={_U+Q:E[I]};A=await F.native.handle_post_config_request_lower_half(K,M,R)
		if A.status!=201:
			if'/wn-sztpdex:tenants/tenant/0/'in A.text:A.text=A.text.replace(_J,_B)
			elif _D in A.text:A.text=re.sub(_P,_B,A.text);A.text=re.sub(_Q,_B,A.text)
		return A
	async def handle_put_config_request(H,request):
		E=request;F,L=utils.parse_raw_path(E._message.path[RestconfServer.len_prefix_running:]);C=await H._check_auth(E)
		if C.status==401:return C
		G=C.text;C=await H.native.check_headers(E)
		if C!=_C:return C
		if F==_A:M=_D+G
		else:
			if not F.startswith(_B):A=web.Response(status=400);B=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(B);return A
			V,N=F.split(_E,1);assert N!=_C;M=_D+G+_A+N
		O=dict()
		for P in L.keys():O[P]=re.sub(_B,_D+G+_A,L[P])
		try:D=await E.json()
		except json.decoder.JSONDecodeError as Q:A=web.Response(status=400);B=utils.gen_rc_errors(_F,_S,error_message=_T+str(Q));A.text=json.dumps(B);return A
		if F==_A:
			I={_H:[{_L:G}]}
			for J in D.keys():
				assert J.count(_E)==1;R,S=J.split(_E)
				if R!=_M:A=web.Response(status=400);B=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(B);return A
				I[_H][0][S]=D[J]
		else:
			assert type(D)==dict;assert len(D)==1;K=next(iter(D));assert K.count(_E)==1;T,U=K.split(_E)
			if T!=_M:A=web.Response(status=400);B=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(B);return A
			I={_U+U:D[K]}
		A=await H.native.handle_put_config_request_lower_half(M,O,I)
		if A.status!=201 and A.status!=204:
			if _J in A.text:A.text=A.text.replace(_J,_B)
			elif _D in A.text:A.text=re.sub(_P,_B,A.text);A.text=re.sub(_Q,_B,A.text)
		return A
	async def handle_delete_config_request(C,request):
		D=request;E,J=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_running:]);B=await C._check_auth(D)
		if B.status==401:return B
		F=B.text;B=await C.native.check_headers(D)
		if B!=_C:return B
		if E==_A:G=_D+F
		else:
			if not E.startswith(_B):A=web.Response(status=400);I=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(I);return A
			K,H=E.split(_E,1);assert H!=_C;G=_D+F+_A+H
		A=await C.native.handle_delete_config_request_lower_half(G)
		if A.status!=204:
			if _J in A.text:A.text=A.text.replace(_J,_B)
			elif _D in A.text:A.text=re.sub(_P,_B,A.text);A.text=re.sub(_Q,_B,A.text)
		return A
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):0