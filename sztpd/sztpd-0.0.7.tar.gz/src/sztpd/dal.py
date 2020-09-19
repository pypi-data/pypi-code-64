# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_t='config-false-prefixes'
_s='table-name-map'
_r='table-keys'
_q='app_ns'
_p='sztpd_meta'
_o='SELECT schema_name FROM information_schema.schemata;'
_n='key'
_m='cert'
_l='postgresql'
_k='Cannot delete: '
_j='[^/]*=[^/]*'
_i='[^:]*:'
_h='yang-library'
_g='" does not exist.'
_f=':tenants/tenant'
_e='opaque'
_d='global-root'
_c='db_ver'
_b='sqlite'
_a=':memory:'
_Z='first'
_Y='Parent node ('
_X='.singletons'
_W='mysql'
_V='" already exists.'
_U='Node "'
_T=':'
_S='.*/'
_R=') does not exist.'
_Q='after'
_P='before'
_O='insert'
_N='last'
_M='jsob'
_L='row_id'
_K='config-true-seq-nodes'
_J='ssl'
_I='pid'
_H='point'
_G='singletons'
_F='=[^/]*'
_E='='
_D=True
_C=False
_B='/'
_A=None
import os,re,sys,json,base64,pickle,yangson,binascii,pkg_resources,sqlalchemy as sa
from enum import IntFlag
from urllib.parse import quote
from sqlalchemy.sql import and_
from urllib.parse import unquote
from dataclasses import dataclass
from sqlalchemy.schema import CreateTable
from .  import db_utils
known_text=b'a secret message'
jsob_type=sa.JSON
class ContentType(IntFlag):CONFIG_TRUE=1;CONFIG_FALSE=2;CONFIG_ANY=3
@dataclass
class DatabasePath:data_path:str=_A;schema_path:str=_A;jsob_data_path:str=_A;jsob_schema_path:str=_A;table_name:str=_A;row_id:int=_A;inside_path:str=_A;path_segments:list=_A;jsob:dict=_A;node_ptr:dict=_A;prev_ptr:dict=_A
class NodeAlreadyExists(Exception):0
class NodeNotFound(Exception):0
class ParentNodeNotFound(Exception):0
class TooManyNodesFound(Exception):0
class InvalidResourceTarget(Exception):0
class CreateCallbackFailed(Exception):0
class ChangeCallbackFailed(Exception):0
class DeleteCallbackFailed(Exception):0
class DataAccessLayer:
	def __init__(A,db_url,cacert_param=_A,cert_param=_A,key_param=_A,yl_obj=_A,app_ns=_A,opaque=_A):
		F=yl_obj;E=key_param;D=cert_param;C=cacert_param;B=db_url;A.app_ns=_A;A.engine=_A;A.metadata=_A;A.leafrefs=_A;A.referers=_A;A.ref_stat_collectors=_A;A.global_root_id=_A;A.table_keys=_A;A.schema_path_to_real_table_name=_A;A.config_false_prefixes=_A;A.post_dal_callbacks=_A;A.config_true_seq_nodes=_A;A.config_true_seq_nodes_dirty=_C
		if F is _A:A._init(B,C,D,E)
		else:A.app_ns=app_ns;A._create(B,C,D,E,F,opaque)
		assert A.app_ns!=_A;assert A.engine!=_A;assert A.metadata!=_A;assert A.leafrefs!=_A;assert A.referers!=_A;assert A.ref_stat_collectors!=_A;assert A.global_root_id!=_A;assert A.table_keys!=_A;assert A.schema_path_to_real_table_name!=_A;assert A.config_false_prefixes!=_A;assert A.config_true_seq_nodes!=_A;A.len_app_ns=len(A.app_ns)
	def opaque(A):
		B=A.metadata.tables[A.schema_path_to_real_table_name[_G]]
		with A.engine.connect()as C:D=C.execute(sa.select([B.c.jsob]).where(B.c.name==_e));return D.first()[0]
	async def num_elements_in_list(A,data_path):
		B=data_path;C=re.sub(_F,'',B)
		if C!=B:assert NotImplementedError("Nested listed arren't supported yet.")
		D=A.schema_path_to_real_table_name[C];E=A.metadata.tables[D]
		with A.engine.connect()as F:G=F.execute(sa.select([sa.func.count()]).select_from(E));H=G.first()[0];return H
	async def get_tenant_name_for_admin(A,email_address):
		K='email-address';G=email_address
		if A.app_ns.endswith('x'):
			B=A.schema_path_to_real_table_name[_B+A.app_ns+':tenants/tenant/admin-accounts/admin-account'];C=A.metadata.tables[B]
			with A.engine.connect()as E:
				D=E.execute(sa.select([C.c.pid]).where(C.c[K]==G));F=D.first()
				if F!=_A:I=F[0];B=A.schema_path_to_real_table_name[_B+A.app_ns+_f];H=A.metadata.tables[B];D=E.execute(sa.select([H.c.name]).where(H.c.row_id==I));J=D.first()[0];return J
		B=A.schema_path_to_real_table_name[_B+A.app_ns+':admin-accounts/admin-account'];C=A.metadata.tables[B]
		with A.engine.connect()as E:
			D=E.execute(sa.select([C.c.pid]).where(C.c[K]==G));F=D.first()
			if F!=_A:return _A
		raise NodeNotFound('Admin "'+G+_g)
	async def get_tenant_name_for_global_key(A,table_name,k):
		B=table_name;C=A.schema_path_to_real_table_name[B];E=A.metadata.tables[C]
		with A.engine.connect()as F:
			D=F.execute(sa.select([E.c.pid]).where(getattr(E.c,A.table_keys[B])==k));G=D.first()
			if G==_A:raise NodeNotFound('key "'+k+'" in table "'+B+_g)
			I=G[0];C=A.schema_path_to_real_table_name[_B+A.app_ns+_f];H=A.metadata.tables[C];D=F.execute(sa.select([H.c.name]).where(H.c.row_id==I));J=D.first()[0];return J
	async def handle_get_opstate_request(B,data_path):
		A=data_path;assert A!='';assert not(A!=_B and A[-1]==_B)
		if A=='/ietf-yang-library:yang-library':
			E=B.schema_path_to_real_table_name[_G];C=B.metadata.tables[E]
			with B.engine.connect()as F:G=F.execute(sa.select([C.c.jsob]).where(C.c.name==_h));return G.first()[0]
		D=re.sub(_F,'',A)
		if 0:return await B._handle_get_data_request(A,D,ContentType.CONFIG_FALSE)
		else:return await B._handle_get_data_request(A,D,ContentType.CONFIG_ANY)
	async def handle_get_config_request(C,data_path):
		A=data_path;assert A!='';assert not(A!=_B and A[-1]==_B);B=re.sub(_F,'',A);F=await C._handle_get_data_request(A,B,ContentType.CONFIG_TRUE);D=re.sub(_S,'',B)
		if not D.startswith(C.app_ns+_T):D=C.app_ns+_T+D
		for E in C.config_false_prefixes:
			if E.startswith(B):
				if B==_B:G=E[1:]
				else:G=E.replace(B,D,1)
				I=_A;J=F
				def H(prev_ptr,curr_ptr,remainder_path):
					D=prev_ptr;B=remainder_path;A=curr_ptr;E=B.split(_B)
					for C in E:
						if type(A)==list:
							for F in A:H(A,F,B)
							return
						elif C in A:D=A;A=A[C];B=B.replace(C+_B,'',1)
						else:return
					D.pop(C)
				H(I,J,G)
			else:0
		return F
	async def _handle_get_data_request(C,data_path,schema_path,content_type):
		M='Node (';G=content_type;F=data_path;E=schema_path
		if G is ContentType.CONFIG_TRUE and any((E.startswith(A)for A in C.config_false_prefixes)):raise NodeNotFound(M+F+_R)
		with C.engine.connect()as H:
			A=C._get_dbpath_for_data_path(F,G,H)
			if A==_A:raise NodeNotFound(M+F+_R)
			B=re.sub(_S,'',E);J=B
			if B=='':D=A.node_ptr
			else:
				if not B.startswith(C.app_ns+_T):B=C.app_ns+_T+B
				D={}
				if A.table_name!=_G and J==A.inside_path:D[B]=[];D[B].append(A.node_ptr);A.node_ptr=D[B][0]
				else:D[B]=A.node_ptr
			K=C._get_list_of_direct_subtables_for_schema_path(E)
			for I in K:L=F+I[len(E):];await C._recursively_attempt_to_get_data_from_subtable(I,A.row_id,E,L,A.node_ptr,G,H)
		return D
	async def _recursively_attempt_to_get_data_from_subtable(C,subtable_name,pid,jsob_schema_path,jsob_data_path,jsob_iter,content_type,conn):
		L=content_type;K=jsob_data_path;G=jsob_schema_path;B=subtable_name
		if not ContentType.CONFIG_FALSE in L:
			if any((B.startswith(A)for A in C.config_false_prefixes)):return
			else:0
		else:0
		S=C._find_rows_in_table_having_pid(B,pid,conn);H=S.fetchall()
		if len(H)==0:return
		D=jsob_iter
		if G==_B:O=B[1:]
		else:assert G.startswith(_B+C.app_ns);O=B.replace(G+_B,'')
		E=re.sub(_S,'',B);I=re.sub(E+'$','',O)
		if I!='':
			I=I[:-1];T=I.split(_B)
			for M in T:
				try:D=D[M]
				except KeyError as Z:assert ContentType.CONFIG_FALSE in L;D[M]={};D=D[M]
		if any((B.startswith(A)for A in C.config_false_prefixes)):
			D[E]=[];U=C.schema_path_to_real_table_name[B];V=C.metadata.tables[U]
			for F in H:
				J={}
				for A in V.c:
					if A.name!=_L and A.name!=_I:
						if type(A.type)is sa.sql.sqltypes.DateTime:J[A.name]=F[A.name].strftime('%Y-%m-%dT%H:%M:%SZ')
						elif type(A.type)is sa.sql.sqltypes.JSON or type(A.type)is sa.sql.sqltypes.PickleType:
							if F[A.name]is not _A and not(type(F[A.name])is list and len(F[A.name])==0):J[A.name]=F[A.name]
						elif F[A.name]is not _A:J[A.name]=F[A.name]
				D[E].append(J)
		else:
			if B in C.config_true_seq_nodes:
				G=re.sub(_F,'',K);P=K+B[len(G):];assert P in C.config_true_seq_nodes[B]
				def W(e):return C.config_true_seq_nodes[B][P].index(e[2])
				H.sort(key=W)
			else:0
			Q=0
			for N in H:
				R=N[_M];E=next(iter(R))
				if E not in D:D[E]=[]
				D[E].append(R.pop(E));X=C._get_list_of_direct_subtables_for_schema_path(B)
				for Y in X:await C._recursively_attempt_to_get_data_from_subtable(Y,N[0],B,K+_E+N[2],D[E][Q],L,conn)
				Q+=1
	async def handle_post_config_request(A,data_path,query_dict,request_body,create_callbacks,change_callbacks,opaque):
		E=request_body;B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B);assert'?'not in B;assert type(E)==dict
		with A.engine.begin()as C:
			F=A._get_dbpath_for_data_path(B,ContentType.CONFIG_TRUE,C)
			if F==_A:raise ParentNodeNotFound(_Y+B+_R)
			await A._handle_post_config_request(F,query_dict,E,create_callbacks,change_callbacks,opaque,C)
			if A.post_dal_callbacks is not _A:
				for D in A.post_dal_callbacks:
					try:await D[0](D[1],C,D[2])
					except Exception as G:A.post_dal_callbacks=_A;raise G
				A.post_dal_callbacks=_A
	async def _handle_post_config_request(A,parent_dbpath,query_dict,request_body,create_callbacks,change_callbacks,opaque,conn):
		Y=change_callbacks;T=opaque;S=create_callbacks;J=conn;H=query_dict;F=request_body;B=parent_dbpath;K=B.data_path;Z=re.sub(_F,'',K);E=next(iter(F))
		if K==_B:C=E;I=_B+C
		else:C=re.sub(_i,'',E);I=K+_B+C
		D=re.sub(_F,'',I);O=A._get_table_name_for_schema_path(D);assert O!=_A
		if O==B.table_name:
			if C in B.node_ptr:
				if type(B.node_ptr[C])!=list:raise NodeAlreadyExists(_U+C+_V)
				assert len(F[E])==1
				if F[E][0]in B.node_ptr[C]:raise NodeAlreadyExists(_U+F[E][0]+_V)
				if D not in A.config_true_seq_nodes:B.node_ptr[C].append(F[E][0])
				else:
					G=_N
					if _O in H:G=H[_O]
					if G==_Z:assert _H not in H;B.node_ptr[C].insert(0,F[E][0])
					elif G==_N:assert _H not in H;B.node_ptr[C].append(F[E][0])
					else:
						assert G in(_P,_Q);assert _H in H;P=H[_H].rsplit(_E,1)[1];P=unquote(P);L=B.node_ptr[C].index(P)
						if G==_P:0
						elif G==_Q:L=L+1
						B.node_ptr[C].insert(L,F[E][0])
				if D in S:
					for W in S[D]:await W(I+_E+F[E][0],B.jsob,B.jsob_data_path,T,J)
			else:B.node_ptr[C]=F.pop(E);a=await A._recursively_post_subtable_data(B.row_id,I,B.node_ptr[C],B.jsob,B.jsob_data_path,S,T,J)
			A._update_jsob_for_row_id_in_table(B.table_name,B.row_id,B.jsob,J)
		else:
			assert D in A.table_keys
			if C not in B.node_ptr:
				B.node_ptr[C]=[];A._update_jsob_for_row_id_in_table(B.table_name,B.row_id,B.jsob,J)
				if D in A.config_true_seq_nodes:
					if I not in A.config_true_seq_nodes[D]:A.config_true_seq_nodes[D][I]=[];A.config_true_seq_nodes_dirty=_D
			U={};assert len(F[E])==1;U[C]=F[E][0];Q=F[E][0][A.table_keys[O]];V={};V[_I]=B.row_id;V[A.table_keys[O]]=Q;V[_M]={};R=A.schema_path_to_real_table_name[O];M=A.metadata.tables[R]
			try:X=J.execute(M.insert().values(**V))
			except sa.exc.IntegrityError:raise NodeAlreadyExists(_U+C+_V)
			I+=_E+str(Q);a=await A._recursively_post_subtable_data(X.inserted_primary_key[0],I,U[C],U,I,S,T,J);R=A.schema_path_to_real_table_name[O];M=A.metadata.tables[R];J.execute(M.update().where(M.c.row_id==X.inserted_primary_key[0]).values(jsob=U))
			if D in A.config_true_seq_nodes:
				if K==_B:N=_B+C
				else:N=K+_B+C
				assert N in A.config_true_seq_nodes[D];c=A.config_true_seq_nodes[D][N];G=_N
				if _O in H:G=H[_O]
				if G==_Z:assert _H not in H;A.config_true_seq_nodes[D][N].insert(0,Q);A.config_true_seq_nodes_dirty=_D
				elif G==_N:assert _H not in H;A.config_true_seq_nodes[D][N].append(Q);A.config_true_seq_nodes_dirty=_D
				else:
					assert G in(_P,_Q);assert _H in H;P=H[_H].rsplit(_E,1)[1];L=A.config_true_seq_nodes[D][N].index(P)
					if G==_P:0
					elif G==_Q:L=L+1
					A.config_true_seq_nodes[D][N].insert(L,Q);A.config_true_seq_nodes_dirty=_D
			else:0
		if A.config_true_seq_nodes_dirty==_D:R=A.schema_path_to_real_table_name[_B];M=A.metadata.tables[R];X=J.execute(sa.update(M).where(M.c.name==_K).values(jsob=A.config_true_seq_nodes));A.config_true_seq_nodes_dirty=_C
		b=re.sub(_F,'',K)
		if b in Y:
			for W in Y[Z]:await W(K,B.jsob,B.jsob_data_path,T)
	async def _recursively_post_subtable_data(A,pid,data_path,req_body_iter,jsob,jsob_data_path,create_callbacks,opaque,conn):
		P=pid;M=jsob_data_path;L=jsob;J=opaque;F=conn;E=create_callbacks;D=data_path;C=req_body_iter;B=re.sub(_F,'',D)
		if type(C)==dict:
			if B in E:
				for Q in E[B]:await Q(D,L,M,J,F)
			for N in C.copy():
				if N.startswith(A.app_ns):G=D+_B+N[A.len_app_ns+1:]
				else:G=D+_B+N
				R=await A._recursively_post_subtable_data(P,G,C[N],L,M,E,J,F)
		elif type(C)==list:
			if B in A.table_keys:
				if B in A.config_true_seq_nodes:
					if D not in A.config_true_seq_nodes[B]:A.config_true_seq_nodes[B][D]=[];A.config_true_seq_nodes_dirty=_D
					else:0
				while C:
					H=C.pop(0);assert type(H)==dict;U=re.sub(_S,'',B);O={};O[U]=H;I=A.table_keys[B];K={};K[_I]=P;K[I]=H[I];K[_M]=O;V=A.schema_path_to_real_table_name[B];W=A.metadata.tables[V]
					try:S=F.execute(W.insert().values(**K))
					except sa.exc.IntegrityError as X:raise NodeAlreadyExists(_U+I+'" with value "'+K[I]+_V)
					G=D+_E+str(H[I])
					if B in A.config_true_seq_nodes:assert D in A.config_true_seq_nodes[B];A.config_true_seq_nodes[B][D].append(H[I]);A.config_true_seq_nodes_dirty=_D
					R=await A._recursively_post_subtable_data(S.inserted_primary_key[0],G,H,O,G,E,J,F);A._update_jsob_for_row_id_in_table(B,S.inserted_primary_key[0],O,F)
				assert type(C)==list;assert len(C)==0
			else:
				assert type(C)==list
				if not(len(C)==1 and C[0]==_A):
					for T in C:G=D+_E+T;R=await A._recursively_post_subtable_data(P,G,C[C.index(T)],L,M,E,J,F)
				else:0
		elif B in E:
			for Q in E[B]:await Q(D,L,M,J,F)
		if B in A.table_keys:return _D
		return _C
	async def handle_post_opstate_request(A,data_path,request_body):
		P='Unrecognized resource schema path: ';I=request_body;B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B);C=re.sub(_F,'',B);F=next(iter(I))
		if C==_B:G=F;D=_B+G
		else:G=re.sub(_i,'',F);D=C+_B+G
		J=A._get_table_name_for_schema_path(D)
		if J!=D:raise NodeNotFound(P+D)
		E=I[F];K=re.findall(_j,B)
		if len(K)==0:E[_I]=A.global_root_id
		else:
			L=A._get_table_name_for_schema_path(C)
			if L==_A:raise ParentNodeNotFound(P+C)
			M=K[-1].split(_E)
			with A.engine.connect()as H:E[_I]=A._get_row_id_for_key_in_table(L,M[1],H)
			if E[_I]==_A:raise ParentNodeNotFound('Nonexistent parent resource: '+B)
		N=A.schema_path_to_real_table_name[J];O=A.metadata.tables[N]
		with A.engine.connect()as H:Q=H.execute(O.insert().values(**E))
	async def handle_put_config_request(A,data_path,query_dict,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque):
		B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B)
		with A.engine.begin()as D:
			E=await A._handle_put_config_request(B,query_dict,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,D)
			if A.post_dal_callbacks is not _A:
				for C in A.post_dal_callbacks:
					try:await C[0](C[1],D,C[2])
					except Exception as F:A.post_dal_callbacks=_A;raise F
				A.post_dal_callbacks=_A
			return E
	async def _handle_put_config_request(B,data_path,query_dict,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		R=delete_callbacks;Q=opaque;P=change_callbacks;O=create_callbacks;H=data_path;F=query_dict;D=conn;C=request_body;G=re.sub(_F,'',H);assert type(C)==dict
		if H==_B:
			A=B._get_dbpath_for_data_path(_B,ContentType.CONFIG_ANY,D);assert A!=_A;await B.recursive_compare_and_put(A.row_id,_B,C,A.node_ptr,_A,A,O,P,R,Q,D);I=B.schema_path_to_real_table_name[A.table_name];E=B.metadata.tables[I];D.execute(E.update().where(E.c.row_id==A.row_id).values(jsob=A.jsob))
			if B.config_true_seq_nodes_dirty==_D:I=B.schema_path_to_real_table_name[_B];E=B.metadata.tables[I];T=D.execute(sa.update(E).where(E.c.name==_K).values(jsob=B.config_true_seq_nodes));B.config_true_seq_nodes_dirty=_C
			return _C
		assert len(C)==1;assert G!=_B;A=B._get_dbpath_for_data_path(H,ContentType.CONFIG_ANY,D)
		if A==_A:
			assert H!=_B;M,V=H.rsplit(_B,1)
			if M=='':M=_B
			A=B._get_dbpath_for_data_path(M,ContentType.CONFIG_ANY,D)
			if A==_A:raise ParentNodeNotFound(_Y+M+_R)
			await B._handle_post_config_request(A,F,C,O,P,Q,D);B._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,D);return _D
		U=next(iter(C));C=C[U]
		if type(C)==list:assert len(C)==1;C=C[0]
		await B.recursive_compare_and_put(A.row_id,H,C,A.node_ptr,A.prev_ptr,A,O,P,R,Q,D)
		if G in B.config_true_seq_nodes and F!=_A:
			if type(A.prev_ptr)==list:A.prev_ptr.remove(A.node_ptr)
			else:assert type(A.prev_ptr)==dict;J,N=H.rsplit(_E,1);assert J in B.config_true_seq_nodes[G];B.config_true_seq_nodes[G][J].remove(N);B.config_true_seq_nodes_dirty=_D
			K=_N
			if _O in F:K=F[_O]
			if K==_Z:
				assert _H not in F
				if type(A.prev_ptr)==list:A.prev_ptr.insert(0,A.node_ptr)
				else:B.config_true_seq_nodes[G][J].insert(0,N)
			elif K==_N:
				assert _H not in F
				if type(A.prev_ptr)==list:A.prev_ptr.append(A.node_ptr)
				else:B.config_true_seq_nodes[G][J].append(N)
			else:
				assert K in(_P,_Q);assert _H in F;S=unquote(F[_H].rsplit(_E,1)[1])
				if type(A.prev_ptr)==list:L=A.prev_ptr.index(S)
				else:L=B.config_true_seq_nodes[G][J].index(S)
				if K==_P:0
				elif K==_Q:L=L+1
				if type(A.prev_ptr)==list:A.prev_ptr.insert(L,A.node_ptr)
				else:B.config_true_seq_nodes[G][J].insert(L,N)
		I=B.schema_path_to_real_table_name[A.table_name];E=B.metadata.tables[I];D.execute(E.update().where(E.c.row_id==A.row_id).values(jsob=A.jsob))
		if B.config_true_seq_nodes_dirty==_D:I=B.schema_path_to_real_table_name[_B];E=B.metadata.tables[I];T=D.execute(sa.update(E).where(E.c.name==_K).values(jsob=B.config_true_seq_nodes));B.config_true_seq_nodes_dirty=_C
		return _C
	async def recursive_compare_and_put(C,pid,data_path,req_body_iter,dbpath_curr_ptr,dbpath_prev_ptr,dbpath,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		X=dbpath_prev_ptr;Q=pid;N=delete_callbacks;M=change_callbacks;L=create_callbacks;J=conn;I=opaque;H=dbpath;F=dbpath_curr_ptr;D=req_body_iter;B=data_path;assert type(D)==type(F);E=re.sub(_F,'',B)
		if B==_B:0
		if type(D)==dict:
			S=set(list(D.keys()));T=set(list(F.keys()))
			for A in [A for A in S if A not in T]:
				if type(D[A])==list:
					U=_B+A if B==_B else B+_B+A;V=re.sub(_F,'',U)
					if V in C.table_keys:await C.recursive_compare_and_put(Q,U,D[A],[],_A,H,L,M,N,I,J);F[A]=[]
					else:F[A]=[];await C.recursive_compare_and_put(Q,U,D[A],F[A],F,H,L,M,N,I,J)
				else:
					E=re.sub(_F,'',B);V=_B+A if E==_B else E+_B+A;assert type(D)!=list;G=_B+A if B==_B else B+_B+A;F[A]=D[A];a=await C._recursively_post_subtable_data(Q,G,D[A],H.jsob,H.jsob_data_path,L,I,J)
					if a==1:assert type(D)==dict;assert type(D[A])==list;assert len(D[A])==0;D.pop(A);F.pop(A)
			for A in T-S:
				if _C:U=_B+A if B==_B else B+_B+A;await C.recursive_compare_and_put(Q,U,[],F[A],F,H,L,M,N,I,J);del F[A]
				else:
					V=_B+A if E==_B else E+_B+A
					if V in C.config_false_prefixes:0
					else:G=_B+A if B==_B else B+_B+A;await C._recursively_delete_subtable_data(H.row_id,G,F[A],N,I,J);del F[A]
			Y=_C
			for A in T&S:
				G=_B+A if B==_B else B+_B+A;V=re.sub(_F,'',G);b=await C.recursive_compare_and_put(Q,G,D[A],F[A],F,H,L,M,N,I,J)
				if b==_D:Y=_D
			if T-S or(S-T or Y==_D):
				if E in M:
					for R in M[E]:await R(B,H.jsob,H.jsob_data_path,I)
			return _C
		elif type(D)==list:
			if E in C.table_keys:
				W=[A[C.table_keys[E]]for A in D];O=set(W);K=set([A[0]for A in C._get_keys_in_table_having_pid(E,Q,J)])
				for A in [A for A in W if A not in K]:assert B!=_B;G=B+_E+A;c=[B for B in D if B[C.table_keys[E]]==A][0];d=[c];g=await C._recursively_post_subtable_data(Q,B,d,_A,_A,L,I,J)
				for A in K-O:G=B+_E+A;h,Z=B.rsplit(_B,1);assert Z!='';await C._recursively_delete_subtable_data(H.row_id,G,X[Z],N,I,J)
				for A in K&O:G=B+_E+A;P=C._get_dbpath_for_data_path(G,ContentType.CONFIG_TRUE,J);assert P!=_A;e=[B for B in D if B[C.table_keys[E]]==A][0];await C.recursive_compare_and_put(P.row_id,G,e,P.node_ptr,P.prev_ptr,P,L,M,N,I,J);C._update_jsob_for_row_id_in_table(P.table_name,P.row_id,P.jsob,J)
				if E in C.config_true_seq_nodes:
					assert B in C.config_true_seq_nodes[E]
					if W!=C.config_true_seq_nodes[E][B]:C.config_true_seq_nodes[E][B]=W;C.config_true_seq_nodes_dirty=_D
				if O-K or K-O:return _D
				return _C
			else:
				O=set(D);K=set(F);F.clear();F.extend(D)
				for A in O-K:
					G=B+_E+unquote(A)
					if E in L:
						for R in L[E]:await R(G,H.jsob,H.jsob_data_path,I,J)
				for A in K-O:
					G=B+_E+unquote(A)
					if E in N:
						for R in N[E]:await R(G,I)
				if O-K or K-O:return _D
				return _C
		else:
			if F!=D:
				f=re.sub('^.*/','',B);X[f]=D
				if E in M:
					for R in M[E]:await R(B,H.jsob,H.jsob_data_path,I)
			else:0
			return _C
		raise NotImplementedError('logic never reaches this point')
	async def handle_put_opstate_request(E,data_path,request_body):
		C=data_path;B=request_body;assert C!='';assert not(C!=_B and C[-1]==_B)
		with E.engine.begin()as G:
			D,F=C.rsplit(_B,1);assert F!=''
			if D=='':D=_B
			A=E._get_dbpath_for_data_path(D,ContentType.CONFIG_ANY,G)
			if A==_A:raise ParentNodeNotFound(_Y+D+_R)
			if type(B)==str:assert type(A.node_ptr)==dict;A.node_ptr[F]=B
			else:assert type(A.node_ptr)==dict and type(B)==dict;A.node_ptr[F]=B[next(iter(B))]
			E._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,G)
	async def handle_delete_config_request(A,data_path,delete_callbacks,change_callbacks,opaque):
		B=data_path;assert B!='';assert B!=_B;assert B[-1]!=_B
		with A.engine.begin()as D:
			await A._handle_delete_config_request(B,delete_callbacks,change_callbacks,opaque,D)
			if A.post_dal_callbacks is not _A:
				for C in A.post_dal_callbacks:
					try:await C[0](C[1],D,C[2])
					except Exception as E:A.post_dal_callbacks=_A;raise E
				A.post_dal_callbacks=_A
	async def _handle_delete_config_request(B,data_path,delete_callbacks,change_callbacks,opaque,conn):
		I=opaque;H=change_callbacks;E=conn;D=data_path;F,G=D.rsplit(_B,1)
		if F=='':F=_B
		A=B._get_dbpath_for_data_path(F,ContentType.CONFIG_TRUE,E)
		if A==_A:raise NodeNotFound(_k+D)
		if _E in G:C,Q=G.rsplit(_E,1)
		else:C=G
		assert type(A.node_ptr)==dict
		if C not in A.node_ptr:raise NodeNotFound('Cannot delete '+D+'.')
		await B._recursively_delete_subtable_data(A.row_id,D,A.node_ptr[C],delete_callbacks,I,E)
		if type(A.node_ptr[C])==list:
			J=re.sub(_F,'',D)
			if J in B.table_keys:
				M=B._find_rowids_in_table_having_pid(J,A.row_id,E);N=M.fetchall()
				if len(N)==0:assert type(A.node_ptr[C])==list;assert len(A.node_ptr[C])==0;A.node_ptr.pop(C)
			elif len(A.node_ptr[C])==0:A.node_ptr.pop(C)
		else:A.node_ptr.pop(C)
		B._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,E)
		if B.config_true_seq_nodes_dirty==_D:O=B.schema_path_to_real_table_name[_B];K=B.metadata.tables[O];R=E.execute(sa.update(K).where(K.c.name==_K).values(jsob=B.config_true_seq_nodes));B.config_true_seq_nodes_dirty=_C
		L=re.sub(_F,'',F)
		if L in H:
			for P in H[L]:await P(F,A.jsob,A.jsob_data_path,I)
	async def _recursively_delete_subtable_data(A,pid,data_path,curr_data_iter,delete_callbacks,opaque,conn):
		J=opaque;G=conn;F=delete_callbacks;E=pid;C=data_path;B=curr_data_iter;H=re.sub(_F,'',C)
		if type(B)==list:
			if H in A.table_keys:
				assert B==[];O,K=C.rsplit(_B,1)
				async def L(pid,data_path,delete_callbacks,opaque,conn):
					F=conn;C=data_path;B=re.sub(_F,'',C);D=A._get_dbpath_for_data_path(C,ContentType.CONFIG_TRUE,F)
					if D==_A:raise NodeNotFound(_k+C)
					I=next(iter(D.jsob));J=D.jsob[I];await A._recursively_delete_subtable_data(D.row_id,C,J,delete_callbacks,opaque,F);K=A.schema_path_to_real_table_name[B];G=A.metadata.tables[K];L=F.execute(sa.delete(G).where(G.c.row_id==D.row_id));assert L.rowcount==1
					if B in A.config_true_seq_nodes:
						E,H=C.rsplit(_E,1);assert E in A.config_true_seq_nodes[B];assert H in A.config_true_seq_nodes[B][E];A.config_true_seq_nodes[B][E].remove(H);A.config_true_seq_nodes_dirty=_D
						if len(A.config_true_seq_nodes[B][E])==0:A.config_true_seq_nodes[B].pop(E);A.config_true_seq_nodes_dirty=_D
				if _E in K:await L(E,C,F,J,G)
				else:
					P=[B[0]for B in A._get_keys_in_table_having_pid(H,E,G)]
					for D in P:I=C+_E+D;await L(E,I,F,J,G)
			elif any((H.startswith(B)for B in A.config_false_prefixes)):assert B==[];Q=A.schema_path_to_real_table_name[H];M=A.metadata.tables[Q];S=G.execute(sa.delete(M).where(M.c.pid==E))
			else:
				O,K=C.rsplit(_B,1)
				if _E in K:D=unquote(K.rsplit(_E)[1]);assert D in B;I=C;await A._recursively_delete_subtable_data(E,I,D,F,J,G);B.remove(D)
				else:
					while len(B)!=0:
						D=B[0]
						if D is _A:break
						I=C+_E+D;await A._recursively_delete_subtable_data(E,I,D,F,J,G);B.pop(0)
		elif type(B)==dict:
			for N in B.keys():assert C!=_B;I=C+_B+N;await A._recursively_delete_subtable_data(E,I,B[N],F,J,G)
		else:0
		if not type(B)==list and not any((H.startswith(B)for B in A.config_false_prefixes)):
			if H in F:
				for R in F[H]:await R(C,J)
	def _find_rows_in_table_having_pid(B,table_name,pid,conn):C=B.schema_path_to_real_table_name[table_name];A=B.metadata.tables[C];D=conn.execute(sa.select([A]).where(A.c.pid==pid).order_by(A.c.row_id));return D
	def _find_rowids_in_table_having_pid(B,table_name,pid,conn):C=B.schema_path_to_real_table_name[table_name];A=B.metadata.tables[C];D=conn.execute(sa.select([A.c.row_id]).where(A.c.pid==pid).order_by(A.c.row_id));return D
	def _get_keys_in_table_having_pid(A,table_name,pid,conn):B=table_name;D=A.schema_path_to_real_table_name[B];C=A.metadata.tables[D];E=conn.execute(sa.select([getattr(C.c,A.table_keys[B])]).where(C.c.pid==pid));return E
	def _get_list_of_direct_subtables_for_schema_path(D,schema_path):
		A=schema_path
		if A!=_B:assert A[-1]!=_B;A+=_B
		C=[]
		for B in sorted(D.schema_path_to_real_table_name.keys()):
			if str(B).startswith(A):
				if not any((A for A in C if str(B).startswith(A+_B))):
					if str(B)!=_B:C.append(str(B))
					else:0
				else:0
		return C
	def _get_row_id_for_key_in_table(B,table_name,key,conn):
		C=table_name;E=B.schema_path_to_real_table_name[C];D=B.metadata.tables[E];F=conn.execute(sa.select([D.c.row_id]).where(getattr(D.c,B.table_keys[C])==key));A=F.fetchall();assert A is not _A
		if len(A)==0:return _A
		if len(A)>1:raise TooManyNodesFound()
		return A[0][0]
	def _get_jsob_iter_for_path_in_jsob(D,jsob,path):
		B=path;assert jsob!=_A;assert B[0]!=_B;A=jsob
		if B!='':
			for C in B.split(_B):
				if C!=''and C not in A:return _A
				A=A[C]
				if type(A)==list:assert len(A)==1;A=A[0]
		return A
	def _get_jsob_for_row_id_in_table(C,table_name,row_id,conn):
		F=row_id;D=table_name;K=C.schema_path_to_real_table_name[D];A=C.metadata.tables[K]
		if D in C.table_keys:E=conn.execute(sa.select([A.c.jsob]).where(A.c.row_id==F));G=E.first();assert G!=_A;return G[0]
		else:
			E=conn.execute(sa.select([A]).where(A.c.row_id==F));H=E.first();assert H!=_A;I=D.rsplit(_B,1)[1];J={I:{}}
			for B in A.c:
				if B.name!=_L and B.name!=_I:J[I][B.name]=H[B.name]
			return J
	def _insert_jsob_into_table(A,pid,table_name,new_jsob,conn):
		D=table_name;B=new_jsob;G=A.schema_path_to_real_table_name[D];H=A.metadata.tables[G];E=next(iter(B));C={};C[_I]=pid
		if D in A.table_keys:C[A.table_keys[D]]=B[E][A.table_keys[D]];C[_M]=B
		else:
			for F in B[E].keys():C[F]=B[E][F]
		I=conn.execute(H.insert().values(**C));return I.inserted_primary_key[0]
	def _reload_ordered_by_data(A,conn):B=A.metadata.tables[A.schema_path_to_real_table_name[_G]];C=conn.execute(sa.select([B.c.jsob]).where(B.c.name==_K));A.config_true_seq_nodes=C.first()[0];A.config_true_seq_nodes_dirty=_C
	def _update_jsob_for_row_id_in_table(A,table_name,row_id,new_jsob,conn):C=A.schema_path_to_real_table_name[table_name];B=A.metadata.tables[C];D=conn.execute(sa.update(B).where(B.c.row_id==row_id).values(jsob=new_jsob))
	def _get_table_name_for_schema_path(D,schema_path):
		B=len(_B);C=_G
		for A in D.schema_path_to_real_table_name.keys():
			if schema_path.startswith(A)and len(A)>B:B=len(A);C=A
		return C
	def _get_row_data_for_list_path(A,data_path,conn):
		B=data_path;assert B[0]==_B;assert B!=_B;assert B[-1]!=_B;G=B[1:].split(_B);assert _E in G[-1];D='';H=A.global_root_id
		for E in G:
			if _E in E:
				K,L=E.split(_E);D+=_B+K;I=A._get_table_name_for_schema_path(D);M=A.schema_path_to_real_table_name[I];C=A.metadata.tables[M];J=conn.execute(sa.select([C.c.row_id,C.c.pid]).where(and_(C.c.pid==H,getattr(C.c,A.table_keys[I])==L)));F=J.fetchone()
				if F==_A:return _A
				assert J.fetchone()==_A;H=F[_L]
			else:D+=_B+E
		return F
	def _get_dbpath_for_data_path(B,data_path,content_type,conn):
		D=conn;C=data_path;A=DatabasePath();A.data_path=C;A.schema_path=re.sub(_F,'',C);A.table_name=B._get_table_name_for_schema_path(A.schema_path)
		if A.table_name==_A:return _A
		if A.table_name==_G:A.jsob_data_path=_B;A.jsob_schema_path=_B
		else:
			A.jsob_data_path=C;A.jsob_schema_path=re.sub(_F,'',A.jsob_data_path)
			while A.jsob_schema_path!=A.table_name and A.jsob_schema_path!=_B:L=A.jsob_data_path;A.jsob_data_path=re.sub('(.*=[^/]*)/.*','\\g<1>',A.jsob_data_path);assert A.jsob_data_path!=L;A.jsob_schema_path=re.sub(_F,'',A.jsob_data_path)
		if ContentType.CONFIG_FALSE in content_type and any((A.table_name.startswith(C)for C in B.config_false_prefixes)):raise InvalidResourceTarget("RFC 8040 does not allow queries on lists directly and, because SZTPD doesn't support keys on 'config false' lists, it is never possible to query for 'dbpath.table_name' to be returned.  The 'val' layer should've rejected this query... ")
		if A.jsob_schema_path==_B:A.row_id=B.global_root_id
		else:
			assert A.jsob_schema_path in B.table_keys;assert _E in A.jsob_data_path;G=A.jsob_data_path.split(_B);assert _E in G[-1];E=G[-1].split(_E)
			try:A.row_id=B._get_row_id_for_key_in_table(A.table_name,E[1],D)
			except TooManyNodesFound:
				H=B._get_row_data_for_list_path(A.jsob_data_path,D)
				if H is _A:A.row_id=_A
				else:A.row_id=H[_L]
			if A.row_id==_A:return _A
		assert A.data_path.startswith(A.jsob_data_path);I=A.data_path[len(A.jsob_data_path):];assert A.schema_path.startswith(A.jsob_schema_path);J=A.schema_path[len(A.jsob_schema_path):]
		if A.table_name==_G:A.inside_path=A.schema_path[1:]
		else:K=re.findall(_j,A.jsob_data_path);assert len(K)!=0;E=K[-1].split(_E);A.inside_path=E[0];M=re.sub('^'+A.table_name,'',A.schema_path);assert M==J;A.inside_path+=J
		assert A.inside_path==''or A.inside_path[0]!=_B;A.jsob=B._get_jsob_for_row_id_in_table(A.table_name,A.row_id,D);A.node_ptr=A.jsob;A.prev_ptr=_A
		if A.inside_path=='':A.path_segments=[''];return A
		A.path_segments=A.inside_path.split(_B);N=''
		for F in A.path_segments:
			N+=_B+F
			if type(A.node_ptr)==list:A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[0]
			if F not in A.node_ptr:return _A
			else:A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[F]
		if type(A.node_ptr)==list:
			assert _E in I;O=unquote(I.rsplit(_E,1)[1])
			try:P=A.node_ptr.index(O)
			except:return _A
			A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[P]
		return A
	def _init(A,url,cacert_param,cert_param,key_param):
		J=key_param;I=cert_param;H=cacert_param;G=url
		if not(G.startswith('sqlite:///')or G.startswith(_W)or G.startswith(_l)):raise SyntaxError('The database url contains an unrecognized dialect.')
		F={}
		if H is not _A:
			F[_J]={};F[_J]['ca']=H
			if I is not _A:F[_J][_m]=I
			if J is not _A:F[_J][_n]=J
		A.engine=sa.create_engine(G,connect_args=F);A.db_schema=_A;A.table_keys={};A.config_false_prefixes={};A.config_true_seq_nodes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		if A.engine.url.database==_a or not db_utils.database_exists(A.engine.url,connect_args=F):A.engine=_A;raise NotImplementedError
		if A.engine.dialect.name==_b:A.schema_path_to_real_table_name[_B]=_G;A.schema_path_to_real_table_name[_G]=_G
		else:
			A.db_schema=A.engine.url.database;A.schema_path_to_real_table_name[_B]=A.db_schema.join(_X);A.schema_path_to_real_table_name[_G]=A.db_schema+_X;M=A.engine.execute(_o);K=M.fetchall();N=[K[A][0]for A in range(len(K))]
			if A.db_schema not in N:A.engine.execute(sa.schema.CreateSchema(A.db_schema));raise NotImplementedError
		A.metadata=sa.MetaData(bind=A.engine,schema=A.db_schema);A.metadata.reflect()
		for O in A.metadata.tables.values():
			for D in O.c:
				if type(D.type)is sa.sql.sqltypes.BLOB or type(D.type)is sa.sql.sqltypes.PickleType:D.type=sa.PickleType()
				if A.engine.dialect.name==_W and type(D.type)is sa.dialects.mysql.types.LONGTEXT:D.type=sa.JSON()
				elif type(D.type)is sa.sql.sqltypes.JSON:D.type=sa.JSON()
		B=A.metadata.tables[A.schema_path_to_real_table_name[_G]]
		with A.engine.connect()as E:
			C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_p));L=C.first()[0]
			if L[_c]!=1:raise AssertionError('The database version ('+L[_c]+') is unexpected.')
			C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_q));A.app_ns=C.first()[0];C=E.execute(sa.select([B.c.row_id]).where(B.c.name==_d));A.global_root_id=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_r));A.table_keys=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_s));A.schema_path_to_real_table_name=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_t));A.config_false_prefixes=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_K));A.config_true_seq_nodes=C.first()[0]
	def _create(A,url,cacert_param,cert_param,key_param,yl_obj,opaque):
		V='default startup endpoint';U='endpoint';T='SZTPD_TEST_PATH';S='_sztp_ref_stats_stmt';R='_sztp_globally_unique_stmt';J=key_param;I=cert_param;H=cacert_param;G='name';F=yl_obj;E={}
		if H is not _A:
			E[_J]={};E[_J]['ca']=H
			if I is not _A:E[_J][_m]=I
			if J is not _A:E[_J][_n]=J
		A.engine=sa.create_engine(url,connect_args=E)
		if A.engine.url.database!=_a and db_utils.database_exists(A.engine.url,connect_args=E):raise AssertionError('Database already exists (call init() first).')
		if A.engine.url.database!=_a:
			if A.engine.dialect.name==_W:db_utils.create_database(A.engine.url,encoding='utf8mb4',connect_args=E)
			else:db_utils.create_database(A.engine.url,connect_args=E)
		A.db_schema=_A
		if A.engine.dialect.name in(_W,_l):
			A.db_schema=str(A.engine.url.database);D=A.engine.execute(_o);K=D.fetchall();M=[K[A][0]for A in range(len(K))]
			if A.db_schema not in M:A.engine.execute('CREATE SCHEMA IF NOT EXISTS %s;'%A.db_schema)
		A.metadata=sa.MetaData(bind=A.engine,schema=A.db_schema);C=sa.Table(_G,A.metadata,sa.Column(_L,sa.Integer,primary_key=_D),sa.Column(_I,sa.Integer,unique=_D),sa.Column(G,sa.String(250),unique=_D),sa.Column(_M,jsob_type));A.metadata.create_all()
		with A.engine.connect()as B:B.execute(C.insert(),name=_p,jsob={_c:1});B.execute(C.insert(),name=_q,jsob=A.app_ns);B.execute(C.insert(),name=_h,jsob=F);B.execute(C.insert(),name=_e,jsob=opaque)
		A.table_keys={_G:G,_B:G};A.config_true_seq_nodes={};A.config_false_prefixes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		if A.engine.dialect.name==_b:A.schema_path_to_real_table_name[_B]=_G;A.schema_path_to_real_table_name[_G]=_G
		else:A.schema_path_to_real_table_name[_B]=A.db_schema+_X;A.schema_path_to_real_table_name[_G]=A.db_schema+_X
		def N(self,stmt,sctx):self.globally_unique=stmt.argument
		setattr(yangson.schemanode.SchemaNode,R,N);yangson.schemanode.SchemaNode._stmt_callback['wn-app:globally-unique']=R
		def O(self,stmt,sctx):self.ref_stats=stmt.argument
		setattr(yangson.schemanode.SchemaNode,S,O);yangson.schemanode.SchemaNode._stmt_callback['wn-app:ref-stats']=S;L=pkg_resources.resource_filename('sztpd','yang/')
		if os.environ.get(T):A.dm=yangson.DataModel(json.dumps(F),[os.environ.get(T),L])
		else:A.dm=yangson.DataModel(json.dumps(F),[L])
		A._gen_tables(A.dm.schema,_G)
		with A.engine.connect()as B:D=B.execute(C.insert(),name=_s,jsob=A.schema_path_to_real_table_name);D=B.execute(C.insert(),name=_r,jsob=A.table_keys);D=B.execute(C.insert(),name=_t,jsob=A.config_false_prefixes);D=B.execute(C.insert(),name=_K,jsob=A.config_true_seq_nodes)
		if os.environ.get('SZTPD_TEST_DAL'):
			with A.engine.connect()as B:D=B.execute(C.insert().values(name=_d,jsob={}))
			A.global_root_id=D.inserted_primary_key[0]
		else:
			with A.engine.connect()as B:D=B.execute(C.insert().values(name=_d,jsob={A.app_ns+':transport':{'listen':{U:[]}},A.app_ns+':audit-log':{}}))
			A.global_root_id=D.inserted_primary_key[0];P=A.schema_path_to_real_table_name[_B+A.app_ns+':transport/listen/endpoint'];Q=A.metadata.tables[P]
			with A.engine.connect()as B:W=B.execute(Q.insert().values(pid=A.global_root_id,name=V,jsob={U:{G:V,'use-for':'native-interface','http':{'tcp-server-parameters':{'local-address':os.environ.get('SZTPD_DEFAULT_ADDR','127.0.0.1')}}}}))
	def _gen_tables(D,node,parent_table_name):
		R='ref_stats';G=parent_table_name;B=node
		if issubclass(type(B),yangson.schemanode.ListNode):
			C=[];C.append(sa.Column(_L,sa.Integer,primary_key=_D));N=D.schema_path_to_real_table_name[G];C.append(sa.Column(_I,sa.Integer,sa.ForeignKey(N+'.row_id'),index=_D,nullable=_C))
			if B.config==_D:
				if len(B.keys)>1:raise NotImplementedError('Only supports lists with at most one key.')
				E=B.get_child(*B.keys[0]);D.table_keys[B.data_path()]=E.name
				if type(E.type)==yangson.datatype.StringType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.Uint32Type:C.append(sa.Column(E.name,sa.Integer,nullable=_C))
				elif type(E.type)==yangson.datatype.IdentityrefType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.UnionType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				else:raise Exception('Unsupported key node type: '+str(type(E.type)))
				if hasattr(E,'globally_unique'):C.append(sa.UniqueConstraint(E.name))
				else:C.append(sa.UniqueConstraint(E.name,_I))
				C.append(sa.Column(_M,jsob_type,nullable=_C))
			else:
				assert B.config==_C;assert hasattr(B,R)==_C
				for A in B.children:
					if issubclass(type(A),yangson.schemanode.LeafNode):
						if type(A.type)==yangson.datatype.StringType:
							if str(A.type)=='date-and-time(string)':C.append(sa.Column(A.name,sa.DateTime,index=_D,nullable=A.mandatory==_C or A.when!=_A))
							else:C.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.Uint16Type:C.append(sa.Column(A.name,sa.SmallInteger,index=_D,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.InstanceIdentifierType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.LeafrefType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.IdentityrefType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.EnumerationType:C.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.UnionType:
							J=0;S=_D
							for K in A.type.types:
								if issubclass(type(K),yangson.datatype.StringType):J+=1
								else:raise Exception('Unhandled union type: '+str(type(K)))
							if J==len(A.type.types):C.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_A))
							else:raise Exception('FIXME: not all union subtypes are stringafiable')
						else:raise Exception('Unhandled leaf type: '+str(type(A.type)))
					elif issubclass(type(A),yangson.schemanode.ChoiceNode):
						H=_D
						for I in A.children:
							assert type(I)==yangson.schemanode.CaseNode
							if len(I.children)>1:H=_C;break
							else:
								for O in I.children:
									if type(O)!=yangson.schemanode.LeafNode:H=_C;break
						if H==_D:C.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_A))
						else:C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.AnydataNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.LeafListNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.ListNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.ContainerNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.NotificationNode):0
					else:raise Exception('Unhandled list child type: '+str(type(A)))
			P=re.sub('^/.*:','',B.data_path()).split(_B)
			if D.engine.dialect.name==_b:F=''
			else:F=D.db_schema+'.'
			for Q in P:F+=Q[0]
			while F in D.schema_path_to_real_table_name.values():F+='2'
			D.schema_path_to_real_table_name[B.data_path()]=F
			if D.db_schema is _A:L=sa.Table(F,D.metadata,*C)
			else:L=sa.Table(re.sub('^'+D.db_schema+'.','',F),D.metadata,*C)
			L.create();G=B.data_path()
		if B.config==_C and issubclass(type(B),yangson.schemanode.DataNode):
			M=B.data_path()
			if not any((M.startswith(A)for A in D.config_false_prefixes)):D.config_false_prefixes[M]=_D
		if B.config==_D and issubclass(type(B),yangson.schemanode.SequenceNode)and B.user_ordered==_D:D.config_true_seq_nodes[B.data_path()]={}
		if hasattr(B,R):D.ref_stat_collectors[B.data_path()]=_A
		if issubclass(type(B),yangson.schemanode.InternalNode):
			if not(type(B)==yangson.schemanode.ListNode and B.config==_C)and not type(B)==yangson.schemanode.RpcActionNode and not type(B)==yangson.schemanode.NotificationNode:
				for A in B.children:D._gen_tables(A,G)