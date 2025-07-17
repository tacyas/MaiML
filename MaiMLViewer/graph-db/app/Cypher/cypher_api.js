query_list = {
	get_xmail: {
		/*
		* [UI-1] XMAILデータ一覧
			!! creator, vendor, owner をリストにして複数データに対応

		Args:
		Returns:
				nid         : node-ID of XMAIL
				file        : source name
				xmail_info  : XMAIL本体情報, [uuid, name, description]
				creators    : 各creator情報のリスト, [[uuid, name, description], ...]
				vendors     : 各vendor情報のリスト, [[uuid, name, description], ...]
				owners      : 各owner情報のリスト, [[uuid, name, description], ...]
		*/
		params: [
		],
		cypher_str: `
			match (a:XMAIL)-[:XML_Root]->(d)-[:XML_Child]->(do {__tag: 'document'})
				optional match (do)-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uud)
				optional match (do)-[:XML_Child]->(na {__tag: 'name'})-[:XML_Data]->(nad)
				optional match (do)-[:XML_Child]->(de {__tag: 'description'})-[:XML_Data]->(ded)
			with d, do, [id(a), a.file, uud.value, nad.value, ded.value] as info
				optional match
					(d)-[:XML_Child*]->(ins {__tag: 'insertion'})
					-[:XML_Child]->(insuri {__tag: 'uri'})-[:XML_Data]->(insurid)
				optional match
					(ins)-[:XML_Child]->(insuu {__tag: 'uuid'})-[:XML_Data]->(insuud)
			with do, info, collect([insurid.value, insuud.value]) as insertions
				optional match (do)-[:XML_Child]->(cr {__tag: 'creator'})
				optional match (cr)-[:XML_Child]->(cruu {__tag: 'uuid'})-[:XML_Data]->(cruud)
				optional match (cr)-[:XML_Child]->(crna {__tag: 'name'})-[:XML_Data]->(crnad)
				optional match (cr)-[:XML_Child]->(crde {__tag: 'description'})-[:XML_Data]->(crded)
			with do, info, collect([cruud.value, crnad.value, crded.value]) as creators, insertions
				optional match (do)-[:XML_Child]->(ve {__tag: 'vendor'})
				optional match (ve)-[:XML_Child]->(veuu {__tag: 'uuid'})-[:XML_Data]->(veuud)
				optional match (ve)-[:XML_Child]->(vena {__tag: 'name'})-[:XML_Data]->(venad)
				optional match (ve)-[:XML_Child]->(vede {__tag: 'description'})-[:XML_Data]->(veded)
			with do, info, collect([veuud.value, venad.value, veded.value]) as vendors, creators, insertions
				optional match (do)-[:XML_Child]->(ow {__tag: 'owner'})
				optional match (ow)-[:XML_Child]->(owuu {__tag: 'uuid'})-[:XML_Data]->(owuud)
				optional match (ow)-[:XML_Child]->(owna {__tag: 'name'})-[:XML_Data]->(ownad)
				optional match (ow)-[:XML_Child]->(owde {__tag: 'description'})-[:XML_Data]->(owded)
			with do, info, collect([owuud.value, ownad.value, owded.value]) as owners, creators, vendors, insertions
				optional match (do)-[:XML_Child]->(ln0)
				-[:XML_Child*0..]->(ln)
				-[:XML_Child]->(lnuu {__tag: 'uuid'})-[:XML_Data]->(lnuud)
			where
				(ln0.__tag = 'chain'
					and ln.__tag = 'chain')
				or (ln0.__tag = 'parent'
					and ln.__tag = 'parent')
			with do, info, creators, vendors, owners, insertions, collect([ln.__tag, lnuud.value]) as linkages
			return
				info[0] as nid,
				info[1] as file,
				info[2..5] as xmail_info,
				creators,
				vendors,
				owners,
				linkages,
				insertions;
		`
	},
	get_PN: {
		/*
		* [UI-2] PN図出力 - nodes & edges

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
				nodes       : PN中に存在する place と transition
				edges       : PN中に存在する arc
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->()
				-[:XML_Child*]->(pn {__tag: 'pnml'})
				-[:XML_Child]->(n)
			where
				id(a)=$xmail_nid
				and n.__tag<>'arc'
			optional match
				(n)-[:SAME*0..1]-()
				-[:PN*0.. {__edge_kind: 'arc'}]-(m)
			with collect(distinct m) as nodes
			unwind nodes as nn
			optional match
				(nn)-[r:PN {__edge_kind: 'arc'}]->()
			return nodes, collect(r) as edges;
		`
	},
	get_PNall: {
		/*
		* [UI-2] PN図出力 (全Layer) - nodes & edges

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
				nodes       : PN中に存在する place/transition (L1), *Template (L2)
				edges       : PN中に存在する arc, placeRef, templateRef, SAME
		*/
		params: [
			'xmail_nid'
		],
		/*
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->()
				-[:XML_Child*]->(n:PN)
			where
				id(a)=$xmail_nid
			optional match
				(n)-[:SAME*0..1]-()
				-[:PN*0..]-(m)
			with collect(distinct m) as nodes
			unwind nodes as nn
			optional match
				(nn)-[r:PN|SAME]->()
			return nodes, collect(r) as edges;
		`
		*/

		/*
		// 2023/4/18 add
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->()
				-[:XML_Child*]->(n:PN)
			where
				id(a)=$xmail_nid
				and not (n.__tag='uuid' or n.__tag='name' or n.__tag='description')
			optional match
				(n)-[:SAME*0..1]-()
				-[:PN*0..]-(m)
			with collect(distinct m) as nodes
			unwind nodes as nn
			optional match
				(nn)-[r:PN|SAME]->()
			return nodes, collect(r) as edges;
		`
		*/
		// 2025/7/17 add
		// annotation、insertion、property、content、uncertaintyについても除外
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->()
				-[:XML_Child*]->(n:PN)
			where
				id(a)=$xmail_nid
				and not (n.__tag='uuid' or n.__tag='name' or n.__tag='description' or n.__tag='annotation' or n.__tag='insertion' or n.__tag='property' or n.__tag='content' or n.__tag='uncertainty')
			optional match
				(n)-[:SAME*0..1]-()
				-[:PN*0..]-(m)
			with collect(distinct m) as nodes
			unwind nodes as nn
			optional match
				(nn)-[r:PN|SAME]->()
			return nodes, collect(r) as edges;
		`
	},
	get_PN_single: {
		/*
		* [UI-2] PN図出力 - nodes & edges(同一XMAILのみ出力)

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
				nodes       : PN中に存在する place と transition
				edges       : PN中に存在する arc
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->()
				-[:XML_Child*]->(n:PN)
			where
				id(a)=$xmail_nid
			optional match
				(n)-[:PN*0..]-(m)
			with collect(distinct m) as nodes
			unwind nodes as nn
			optional match
				(nn)-[r:PN]->()
			return nodes, collect(r) as edges;
		`
	},
	get_template: {
		/*
		* [UI-3] nodeに属するtemplateの取得

		Args:
				place_nid   : node-ID of place node
		Returns:
				placeRef_nid    :
				placeRef_id     :
				template_nid    : node-ID of template
				template_tag    :
				template_id     :
				template_uuid   :
				template_name   :
				template_description    :
		*/
		params: [
			'place_nid'
		],
		cypher_str: `
		match
		(pr {__tag: 'protocol'})
		-[:XML_Child]->(me {__tag: 'method'})
		-[:XML_Child*..2]->(pn {__tag: 'pnml'})
		-[:XML_Child]->(pl {__tag: 'place'}),
		(pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
where id(pl)=$place_nid and plR.ref = pl.id
optional match
		(te)-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uud),
		(te)-[:XML_Child]->(na {__tag: 'name'})-[:XML_Data]->(nad),
		(te)-[:XML_Child]->(de {__tag: 'description'})-[:XML_Data]->(ded)
return
		id(plR) as placeRef_nid,
		plR.id as placeRef_id,
		id(te) as template_nid,
		te.__tag as template_tag,
		te.id as template_id,
		uud.value as template_uuid,
		nad.value as template_name,
		ded.value as template_description;
`
	},
	get_template_bylist: {
		/*
		* [UI-3] 複数のnodeに属するtemplateの一括取得

		Args:
				place_nid_list  : node-ID list of place node
		Returns:
				place_nid       :
				place_id        :
				placeRef_nid    :
				placeRef_id     :
				template_nid    : node-ID of template
				template_tag    :
				template_id     :
				template_uuid   :
				template_name   :
				template_description    :
		*/
		params: [
			'place_nid_list'
		],
		cypher_str: `
match
		(pr {__tag: 'protocol'})
		-[:XML_Child]->(me {__tag: 'method'})
		-[:XML_Child*..2]->(pn {__tag: 'pnml'})
		-[:XML_Child]->(pl {__tag: 'place'}),
		(pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
where
		id(pl) in $place_nid_list
		and plR.ref = pl.id
optional match
		(te)-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uud),
		(te)-[:XML_Child]->(na {__tag: 'name'})-[:XML_Data]->(nad),
		(te)-[:XML_Child]->(de {__tag: 'description'})-[:XML_Data]->(ded)
return
		id(pl) as place_nid,
		pl.id as place_id,
		id(plR) as placeRef_nid,
		plR.id as placeRef_id,
		id(te) as template_nid,
		te.__tag as template_tag,
		te.id as template_id,
		uud.value as template_uuid,
		nad.value as template_name,
		ded.value as template_description;
`
	},
	get_details_bylist: {
		/*
		* [UI-3] 複数のnodeに属する詳細情報の一括取得

		Args:
				nid_list  : node-ID list
		Returns:
				nid       :
				id        :
				placeRef_nid    :
				placeRef_id     :
				template_nid    : node-ID of template
				tag    :
				uuid   :
				name   :
				description    :
		*/
		params: [
			'nid_list'
		],
		cypher_str: `
			match
				(n:XMLtag)
			where
				id(n) in $nid_list
			optional match
				(n)-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uud)
			optional match
				(n)-[:XML_Child]->(na {__tag: 'name'})-[:XML_Data]->(nad)
			optional match
				(n)-[:XML_Child]->(de {__tag: 'description'})-[:XML_Data]->(ded)
			return
				id(n) as place_nid,
				n.id as place_id,
				null as placeRef_nid,
				null as placeRef_id,
				null as template_nid,
				n.__tag as template_tag,
				null as template_id,
				uud.value as template_uuid,
				nad.value as template_name,
				ded.value as template_description;
		`
	},
	get_properties: {
		/*
		* [UI-4] template中のproperty情報取得

		Args:
				template_nid    : node-ID of template
		Returns:
				nid             : node-ID of property
				parent_nid      : 親ノードの node-ID, rootはtemplateのnode-ID
				description     :
				value           :
				attrib          : 属性データ, 辞書形式
		*/
		params: [
			'template_nid'
		],
		cypher_str: `
		match
		(te)-[:XML_Child*0..]->(parent)-[:XML_Child]->(prop {__tag: 'property'})
where
		id(te)=$template_nid
optional match
		(prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
optional match
		(prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
return
		id(prop) as nid,
		id(parent) as parent_nid,
		dd.value as description,
		vd.value as value,
		properties(prop) as attrib;
`
	},
	/* 20240523 add */
	get_generals: {
		/*
		* [UI-4] template中のproperty,content,uncertainty情報取得

		Args:
				template_nid    : node-ID of template
		Returns:
				nid             : node-ID of property or content or uncertainty
				parent_nid      : 親ノードの node-ID, rootはtemplateのnode-ID
				description     :
				value           :
				attrib          : 属性データ, 辞書形式
		*/
		params: [
			'template_nid'
		],
		cypher_str: `
		match
				(te)-[:XML_Child*0..]->(parent)-[:XML_Child]->(prop {__tag: 'property'})
		where
				id(te)=$template_nid
		optional match
				(prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
		optional match
				(prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
		return
				id(prop) as nid,
				id(parent) as parent_nid,
				dd.value as description,
				vd.value as value,
				properties(prop) as attrib
		union
		match
				(te)-[:XML_Child*0..]->(parent)-[:XML_Child]->(prop {__tag: 'content'})
		where
				id(te)=$template_nid
		optional match
				(prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
		optional match
				(prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
		return
				id(prop) as nid,
				id(parent) as parent_nid,
				dd.value as description,
				vd.value as value,
				properties(prop) as attrib
		union
		match
				(te)-[:XML_Child*0..]->(parent)-[:XML_Child]->(prop {__tag: 'uncertainty'})
		where
				id(te)=$template_nid
		optional match
				(prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
		optional match
				(prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
		return
				id(prop) as nid,
				id(parent) as parent_nid,
				dd.value as description,
				vd.value as value,
				properties(prop) as attrib;
		`
	},
	/* 20240906 add */
	get_insertions: {
		/*
		* [UI-4] template,instance内のinsertion情報取得

		Args:
				template_nid    : node-ID of template and instance
		Returns:
				uri             : insertion要素のuri値
				hash            : insertion要素のhash値
				format          : insertion要素のformat値
				uuid            : insertion要素のuuid値
		*/
		params: [
			'template_nid'
		],
		cypher_str: `
		match
			(te)- [: XML_Child * 0..] -> (ins { __tag: 'insertion' })
		where
		id(te) = $template_nid
		optional match
			(ins) - [: XML_Child] -> (u { __tag: 'uri' }) -[: XML_Data] -> (ud)
		optional match
			(ins) - [: XML_Child] -> (h { __tag: 'hash' }) -[: XML_Data] -> (hd)
		optional match
			(ins) - [: XML_Child] -> (uu { __tag: 'uuid' }) -[: XML_Data] -> (uud)
		optional match
			(ins) - [: XML_Child] -> (f { __tag: 'format' }) -[: XML_Data] -> (fd)
		return
		ud.value as uri,
			hd.value as hash,
			fd.value as format,
			uud.value as uuid
		`
	},
	create_PNarc: {
		/*
		* PN図のノード間にarcを作成

		!!! 作成条件の確認も含まれているので 'test_PNarc' での事前確認は必須ではありません。

		Args:
				src_nid         : arc接続ノードstart側 node-ID
				dst_nid         : arc接続ノードend側 node-ID
		Returns:
		*/
		params: [
			'src_nid',
			'dst_nid'
		],
		cypher_str: `
		match (a:XMAIL)
		-[:XML_Root]->()
		-[:XML_Child*]->(pn {__tag: 'pnml'})
		-[:XML_Child]->(s),
		(pn)
		-[:XML_Child]->(d)
where
	id(s)=$src_nid
		and id(d)=$dst_nid
		and s.__tag<>'arc'
		and d.__tag<>'arc'
		and s.__tag<>d.__tag
and not (s)-[:PN]-(d)
and not ()-[:PN]->(d {__tag: 'place'})
create
	(s)-[:PN {__xmail_nid: id(a), __edge_kind: 'arc'}]->(d);
	`
	},
	delete_PNarc: {
		/*
		* PN図のノード間のarcを削除

		Args:
				nid1, nid2      : arc接続ノードの node-ID
		Returns:
		*/
		params: [
			'nid1',
			'nid2'
		],
		cypher_str: `
		match
		(pn {__tag: 'pnml'})
		-[:XML_Child]->(n1)
		-[r:PN]-(n2)
where
	id(n1)=$nid1
		and id(n2)=$nid2
delete r;
`
	},
	test_PNarc: {
		/*
		* PN図のノード間にarc作成可否チェック
			- 条件1 : 同一XMAILに属するPNノード間の接続であること
			- 条件2 : 両端ノードのタイプは place/transition のいずれかであり両端でタイプが異なること
			- 条件3 : 同一のノードペア間のarcは1本を超えてはならない ==> 'no_arc'
			- 条件4 : placeへの入力となるarcは1本を超えてはならない

		Args:
				src_nid         : arc接続ノードstart側 node-ID
				dst_nid         : arc接続ノードend側 node-ID
		Returns:
				matched         : 条件をクリアした場合は真
		*/
		params: [
			'src_nid',
			'dst_nid'
		],
		cypher_str: `
		match
		(pn {__tag: 'pnml'})
		-[:XML_Child]->(s),
		(pn)
		-[:XML_Child]->(d)
where
	id(s)=$src_nid
		and id(d)=$dst_nid
		and s.__tag<>'arc'
		and d.__tag<>'arc'
		and s.__tag<>d.__tag
and not (s)-[:PN]-(d)
and not ()-[:PN]->(d {__tag: 'place'})
return
	count(s)>0 as matched
`
	},
	create_PNedge: {
		/*
		* PN図のノード間にedgeを作成

		Args:
				src_nid         : edge接続ノードstart側 node-ID
				dst_nid         : edge接続ノードend側 node-ID
		Returns:
		*/
		params: [
			'src_nid',
			'dst_nid'
		],
		cypher_str: `
			with
				[['arc', null, null], ['placeRef', 'templateRef', null], [null, 'ref', 'instanceRef']] as edge_table
			match
				(n)-[:XML_Child*1..]->(s),
				(n)-[:XML_Child*1..]->(d)
			where
				id(s)=$src_nid
				and id(d)=$dst_nid
				and not (s)-[:PN]->(d)
			with
				s, d, edge_table[s.__layer][d.__layer] as edge_kind
			where
				edge_kind is not null
			with
				s, d, edge_kind
			where
				case edge_kind
					when 'arc' then
						s.__tag <> d.__tag
						and not (s)<-[:PN]-(d)
						and not ({__tag: 'transition'})-[:PN]->(d)
					when 'placeRef' then
						d.__tag = 'place'
					when 'ref' then
						not (s)-[:PN {__edge_kind: 'ref'}]->()
						and d.__tag starts with s.__tag
					else true
				end
			create
				(s)-[r:PN {__xmail_nid: s.__xmail_nid, __edge_kind: edge_kind}]->(d)
			return edge_kind;
		`
	},
	delete_PNedge: {
		/*
		* PN図のノード間のedgeを削除

		Args:
				src_nid         : edge接続ノードstart側 node-ID
				dst_nid         : edge接続ノードend側 node-ID
		Returns:
		*/
		params: [
			'src_nid',
			'dst_nid'
		],
		cypher_str: `
			match
				(s)-[r:PN]->(d)
			where
				id(s)=$src_nid
				and id(d)=$dst_nid
			delete r
			return count(r) as deleted;
		`
	},
	create_PNnode: {
		/*
		* PN図にplace/transitionを作成

		Args:
				xmail_nid   : node-ID of XMAIL
				id          : ノードに付与するid, XMAILデータ中で唯一性
				kind        : 'place' or 'transition'
		Returns:
		*/
		params: [
			'xmail_nid',
			'id',
			'kind'
		],
		cypher_str: `
		match (a:XMAIL)
		-[:XML_Root]->(d)
		-[:XML_Child*]->(pn {__tag: 'pnml'})
where
	id(a)=$xmail_nid
		and not (d)-[:XML_Child*0..]->({id: $id})
create
	(pn)-[:XML_Child]->(new:XMLtag:PN:Layer1:UNREGISTERED {__tag: $kind, id: $id, __xmail_nid: $xmail_nid, __layer: 0})
return id(new) as nid;
`
	},
	append_template: {
		/*
		* PN図に追加したplaceへtemplateを付与

		Args:
				pn_nid      : node-ID of place
				tag         : template tag ('materialTemplate', 'conditionTemplate', 'resultTemplate')
				id          : template id, XMAILデータ中で唯一性
				ref_id      : ref id, XMAILデータ中で唯一性
				uuid        : UUID
				name        : 名前
				description : 説明
		Returns:
		*/
		params: [
			'place_nid',
			'tag',
			'id',
			'ref_id',
			'uuid',
			'name',
			'description'
		],
		cypher_str: `
		match
		(a:XMAIL)
		-[:XML_Root]->(d)
		-[:XML_Child]->(pr {__tag: 'protocol'})
		-[:XML_Child]->(me {__tag: 'method'})
		-[:XML_Child*..2]->(pn {__tag: 'pnml'})
		-[:XML_Child]->(pl:UNREGISTERED)
where
		id(pl)=$place_nid
		and not (d)-[:XML_Child*0..]->({id: $id})
		and not (d)-[:XML_Child*0..]->({id: $ref_id})
create
		(pr)
		-[:XML_Child]->
		(te:XMLtag:UNREGISTERED {__tag: $tag, id: $id})
		-[:XML_Child]->
		(ref:XMLtag:UNREGISTERED {__tag: 'placeRef', id: $ref_id, ref: pl.id}),
		(te)-[:XML_Child]->(uu:XMLtag:UNREGISTERED {__tag: 'uuid'})
				-[:XML_Data]->(uud:XMLdata:UNREGISTERED {value: $uuid}),
		(te)-[:XML_Child]->(na:XMLtag:UNREGISTERED {__tag: 'name'})
				-[:XML_Data]->(nad:XMLdata:UNREGISTERED {value: $name}),
		(te)-[:XML_Child]->(de:XMLtag:UNREGISTERED {__tag: 'description'})
				-[:XML_Data]->(ded:XMLdata:UNREGISTERED {value: $description});
`
	},
	delete_PNnode: {
		/*
		* PN図のplace/transitionを, 付与されたtemplateも含めて削除

		Args:
				nid         : place/transition の node-ID
		Returns:
		*/
		params: [
			'nid'
		],
		cypher_str: `
		match
		(pr {__tag: 'protocol'})
		-[:XML_Child]->(me {__tag: 'method'})
		-[:XML_Child*..2]->(pn {__tag: 'pnml'})
		-[:XML_Child]->(n:UNREGISTERED)
where
	id(n)=$nid
optional match
		(pr)-[:XML_Child]->(te:UNREGISTERED)-[:XML_Child]->(plR {__tag: 'placeRef'})
where
		plR.ref = n.id
optional match
		(te)-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uud),
		(te)-[:XML_Child]->(na {__tag: 'name'})-[:XML_Data]->(nad),
		(te)-[:XML_Child]->(de {__tag: 'description'})-[:XML_Data]->(ded)
detach delete n, te, plR, uu, uud, na, nad, de, ded;
`
	},
	import_arc: {
		/*
		* XMAIL import 実行時のarc接続作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child]->(me {__tag: 'method'})
				-[:XML_Child*..2]->(pn {__tag: 'pnml'}),
				(pn)-[:XML_Child]->(ar {__tag: 'arc'}),
				(pn)-[:XML_Child]->(s),
				(pn)-[:XML_Child]->(t)
			where
				id(a)=$xmail_nid
				and ar.source=s.id
				and ar.target=t.id
			merge (s)-[:PN {__xmail_nid: $xmail_nid, __edge_kind: 'arc'}]->(t);
		`
	},
	import_placeRef: {
		/*
		* XMAIL import 実行時のplaceRef接続作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child]->(me {__tag: 'method'})
				-[:XML_Child*..2]->(pn {__tag: 'pnml'})
				-[:XML_Child]->(pl {__tag: 'place'})
			where
				id(a)=$xmail_nid
			match
				(pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
			where
				plR.ref = pl.id
			merge
				(te)-[:PN {__xmail_nid: $xmail_nid, __edge_kind: 'placeRef'}]->(pl)
			with
				pl, te,
				case te.__tag
					when 'materialTemplate'		then 'M'
					when 'conditionTemplate'	then 'C'
					when 'resultTemplate'		then 'R'
					else null
				end as mtype
			set
				te:PN:Layer2:Layer12,
				te.__layer = 1,
				te.__xmail_nid = $xmail_nid,
				te.__maiml_type = mtype,
				pl.__maiml_type = mtype;
		`
	},
	import_ref: {
		/*
		* XMAIL import 実行時のtemplate-instance間のref接続作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'}),
				(d)-[:XML_Child]->(data {__tag: 'data'})-[:XML_Child*]->(in)
			where
				id(a)=$xmail_nid
				and in.ref = te.id
			merge
				(in)-[:PN {__xmail_nid: $xmail_nid, __edge_kind: 'ref'}]->(te)
			with
				te, in,
				case te.__tag
					when 'materialTemplate'		then 'M'
					when 'conditionTemplate'	then 'C'
					when 'resultTemplate'		then 'R'
					else null
				end as mtype
			set
				in:PN:Layer3,
				in.__layer = 2,
				in.__xmail_nid = $xmail_nid,
				in.__maiml_type = mtype;
		`
	},
	import_templateRef: {
		/*
		* XMAIL import 実行時の templateRef 接続作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child*]->(te1)-[:XML_Child]->(te1R {__tag: 'templateRef'})
			where
				id(a)=$xmail_nid
			match
				(pr)-[:XML_Child*]->(te2)
			where
				te1R.ref = te2.id
			merge
				(te1)-[:PN {__xmail_nid: $xmail_nid, __edge_kind: 'templateRef'}]->(te2);
		`
	},
	import_instanceRef: {
		/*
		* XMAIL import 実行時の instanceRef 接続作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
				-[:XML_Root]->(d)
				-[:XML_Child]->(data {__tag: 'data'})
				-[:XML_Child*]->(in1)-[:XML_Child]->(in1R {__tag: 'instanceRef'})
			where
				id(a)=$xmail_nid
			match
				(data)-[:XML_Child*]->(in2)
			where
				in1R.ref = in2.id
			merge
				(in1)-[:PN {__xmail_nid: $xmail_nid, __edge_kind: 'instanceRef'}]->(in2);
		`
	},
	update_same_uuid: {
		/*
		* XMAIL import 実行時の同一UUIDを示す接続情報更新

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			//same_uuid
			match
				(a:XMAIL)
			where
				id(a)=$xmail_nid
			match
				(a)-[:XML_Root]->(d)
				-[:XML_Child*]->(te1)
				-[:XML_Child]->(plR1 {__tag: 'placeRef'}),
				(te1)-[:XML_Child]->(uu1 {__tag: 'uuid'})-[:XML_Data]->(uud1),
				(uu2 {__tag: 'uuid'})-[:XML_Data]->(uud2)
			where
				uud1.value = uud2.value
				and id(uud1) <> id(uud2)
			match
				(pr1)-[:XML_Child*]->(te1),
				(pr1)-[:XML_Child*]->(pl1 {__tag: 'place'})
			where
				plR1.ref = pl1.id
			match
				(te2)-[:XML_Child]->(plR2 {__tag: 'placeRef'}),
				(te2)-[:XML_Child]->(uu2 {__tag: 'uuid'}),
				(pr2)-[:XML_Child*]->(te2),
				(pr2)-[:XML_Child*]->(pl2 {__tag: 'place'})
			where
				plR2.ref = pl2.id
			merge (pl1)-[:SAME_UUID {__type: 'PN', __edge_kind: 'SAME'}]->(pl2);
		`
	},
	import_same_template: {
		/*
		* XMAIL import 実行時の同一UUIDを示す接続情報作成

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			//same_uuid
			match
				(a:XMAIL)
			where
				id(a)=$xmail_nid
			match
				(a)-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child*]->(te1)
				-[:XML_Child]->(plR1 {__tag: 'placeRef'}),
				(te1)-[:XML_Child]->(uu1 {__tag: 'uuid'})-[:XML_Data]->(uud1),
				(te2)-[:XML_Child]->(uu2 {__tag: 'uuid'})-[:XML_Data]->(uud2)
			where
				uud1.value = uud2.value
				and id(uud1) <> id(uud2)
			merge (te1)-[:SAME {__edge_kind: 'SAME'}]->(te2);
		`
	},
	import_nodes: {
		/*
		* XMAIL import 実行時のnode property更新

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match (a:XMAIL)
			where
				id(a)=$xmail_nid
			match
				(a)-[:XML_Root]->(d)
				-[:XML_Child]->(pr {__tag: 'protocol'})
				-[:XML_Child]->(me {__tag: 'method'})
				-[:XML_Child*..2]->(pn {__tag: 'pnml'})
				-[:XML_Child]->(n)
			where
				n.__tag <> 'arc'
			set
				n:PN:Layer1,
				n.__layer = 0,
				n.__xmail_nid = $xmail_nid;
		`
	},
	get_docuuid: {
		/*
		20240913 add
		* document要素のuuid取得

		Args:
				xmail_nid   : node-ID of XMAIL
		Returns:
				uuid	: uuid of document element
		*/
		params: [
			'xmail_nid'
		],
		cypher_str: `
			match
				(a:XMAIL)-[:XML_Root]->(d)-[:XML_Child]->(do {__tag: 'document'})-[:XML_Child]->(uu {__tag: 'uuid'})-[:XML_Data]->(uuid)
			where
				id(a)=$xmail_nid
			return
				uuid.value as uuid
		`
	},
	/*
	sample: {
		// クエリ定義サンプル
		params: [
			'nid',
			'label'
		],
		cypher_str: 'match (a:$label) where id(a)=$nid return a;'
	},
	*/
}

function replace_strings(str, patterns) {
	repl_str = str
	for (key in patterns) {
		vstr = '\\$' + key
		pat_str = patterns[key]
		if ((typeof pat_str) !== 'string' || isNaN(pat_str)) {
			//pat_str = "'" + pat_str + "'"
			pat_str = JSON.stringify(pat_str)
		}
		repl_str = repl_str.replace(new RegExp(vstr, 'g'), pat_str)
	}
	return repl_str
}

function get_cypher(name, ...args) {
	const query = query_list[name]
	var params = {};
	query['params'].forEach((key, i) => {
		params[key] = args[i]
	})

	//console.log('query: ', name, params)
	return replace_strings(query['cypher_str'], params)
}

module.exports = {
	query_list: query_list,
	get_cypher: get_cypher
}


//
// codes executed from Node.js
//
if (!module.parent) {
	console.log(JSON.stringify(query_list, null, 2));
}