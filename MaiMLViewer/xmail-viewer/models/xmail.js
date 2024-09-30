'use strict';

var request = require('request');
/*const neo4j = require('neo4j-driver').v1;*/
const neo4j = require('neo4j-driver');
var logger = require('../common/log-utils.js');
const cypher_api = require('../../graph-db/app/Cypher/cypher_api.js');

var graphDb = process.env.GRAPH_DB_IP || '127.0.0.1';
/*const uri = 'bolt://' + graphDb + ':7687';*/
const uri = 'neo4j://' + graphDb + ':7687';
const user = process.env.GRAPH_USER || '';
const password = process.env.GRAPH_PWD || '';
const url = 'http://' + graphDb + ':7474/db/data/transaction/commit';
const C_MODEL = '[xmail]';

/*
 * [UI-1] XMAILデータ一覧
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットからGraphJsonを生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns graphJson - XMAILデータ一覧JSON
 * @throws {cypher error}
 */
 exports.list = async function() {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	let cypher = cypher_api.get_cypher('get_xmail');
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	var graphJson = '[';
	var idx = 0;

	await session
		.run(cypher)
		.then(function(result) {
			result.records.forEach(function(record) {
				session.close();

				if (idx >= 1) {
					graphJson = graphJson + ',';
				}

				// テーブル形式データをセル内における表現に変換する関数
				function tableToString(table, titles) {
					return table.map(function(elm) {
						return elm.map(function(s) { return s === null ? '' : s; })
									.map( (v, i) => '<b>[' + titles[i] + ']</b> ' + v)
									.join('<br>');
					}).join('<br><br>');
				}

				/* Generate creators column */
				var creators = record.get('creators');
				var creatorCol = tableToString(creators, ['uuid', 'name', 'description']);
				logger.app.debug('[Creators column] ' + creatorCol);

				/* Generate vendors column */
				var vendors = record.get('vendors');
				var vendorCol = tableToString(vendors, ['uuid', 'name', 'description']);
				logger.app.debug('[Vendors column] ' + vendorCol);

				/* Generate owners column */
				var owners = record.get('owners');
				var ownerCol = tableToString(owners, ['uuid', 'name', 'description']);
				logger.app.debug('[Owners column] ' + ownerCol);

				/* Generate linkages column */
				var linkages = record.get('linkages');
				var lnkCol = tableToString(linkages, ['tag', 'uuid']);
				logger.app.debug('[Linkages column] ' + lnkCol);

				/* Generate insertions column */
				var insertions = record.get('insertions');
				var insCol = tableToString(insertions, ['uri', 'uuid']);
				logger.app.debug('[Insertions column] ' + insCol);

				graphJson =
					graphJson +
					'{"del_link": "' +
					record.get('nid') +
					'", ' +
					'"nid": "' +
					record.get('nid') +
					'", ' +
					'"file": ' +
					JSON.stringify(record.get('file')) +
					', ' +
					'"xmail_uuid": "' +
					record.get('xmail_info')[0] +
					'", ' +
					'"xmail_name": "' +
					record.get('xmail_info')[1] +
					'", ' +
					'"xmail_description": "' +
					record.get('xmail_info')[2] +
					'", ' +
					'"creators": "' +
					creatorCol +
					'", ' +
					'"vendors": "' +
					vendorCol +
					'", ' +
					'"owners": "' +
					ownerCol +
					'", ' +
					'"linkages": "' +
					lnkCol +
					'", ' +
					'"insertions": "' +
					insCol +
					'"}';

				logger.app.debug('xmail_info=' + record.get('xmail_info').length);
				logger.app.debug('creators=' + record.get('creators').length);
				logger.app.debug('vendors=' + record.get('vendors').length);
				idx = idx + 1;
			});

			graphJson = graphJson + ']';
		})
		.catch(function(error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});

	driver.close();

	return graphJson;
};


/*
 * [UI-2] PN図出力 - nodes & edges
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットからGraphJsonを生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns graphJson - ペトリネットJSON
 * @throws {cypher error}
 */
exports.pn_nodes = async function(id) {
	let cypher = cypher_api.get_cypher('get_PNall', id);
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	var graphJson = '';
	var idx = 0;

	return new Promise(function(resolve, reject) {
		request.post(
			{
				uri: url,
				json: {
					statements: [
						{
							statement: cypher,
							parameters: {},
							resultDataContents: ['row', 'graph']
						}
					]
				}
			},
			async function(error, response, body) {
				if (error) {
					logger.app.error(C_MODEL + error.message);
					reject(error);
				}

				/*
				 * nodes json
				 */
				logger.app.debug(C_MODEL + 'results: ' + JSON.stringify(body.results));
				let nodes = [];
				let edges = [];
				let parents = [];

				if (body.results[0].data.length > 0) {
					nodes = body.results[0].data[0].graph.nodes;
					edges = body.results[0].data[0].graph.relationships;
				}

				// add 240912
				// ステップ１　nodesから１つずつデータを取得、properties.__xmail_nidを取得ーー＞重複なしのリスト
				var maimlnidlist = [];
				var uuidlist = []; 
				var maimlnid;
				for (const record of nodes) {
					maimlnid = record.properties.__xmail_nid;

					if (!maimlnidlist.includes(maimlnid)) {
						maimlnidlist.push(maimlnid);

						const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
						const session = driver.session();
						logger.app.debug(C_MODEL + 'Graph DB connected.');
						let cypher2 = cypher_api.get_cypher('get_docuuid', maimlnid);
						logger.app.debug(C_MODEL + 'Cypher : ' + cypher2.toString());

						// ステップ２　uuidを取得ーー＞uuidとnidのリストを作る
						var uuid;
						await session
							.run(cypher2)
							.then(function (result) {
								result.records.forEach(function (record) {
									//logger.app.debug("getuuid record:"+JSON.stringify(record));
									uuid = record.get('uuid');
									session.close();
								});
							})
							.catch(function (error) {
								session.close();
								logger.app.error(C_MODEL + error.message);
								throw error;
							});
						uuidlist.push({ uuid: uuid, maimlnid: maimlnid });
					}
				}

				// get position's file
				var fdataList = {};
				uuidlist.forEach(function (idobj) {
					var uuid = idobj.uuid;
					var maimlnid = idobj.maimlnid;
					var filename = uuid + '.position';
					var filepath = path.join(__dirname, '../exports/pnmlpositions', filename);
					logger.app.debug('uuid , maimlNID =' + JSON.stringify(uuid) + ',' + JSON.stringify(maimlnid));
					logger.app.debug('positions filepath=' + JSON.stringify(filepath));
					const fs = require('fs');
					var fdata;
					if (fs.existsSync(filepath)) {
						try {
							fdata = fs.readFileSync(filepath, 'utf8');
							if (fdata) {
								fdata = JSON.parse(fdata)
								.map(item => item ? JSON.parse(item) : null)
								.filter(item => item !== null);
								fdataList[maimlnid] = {uuid: uuid, fdata: fdata};
							};
						} catch (error) {
							logger.app.error(C_MODEL + error.message);
						}
					}
				});

				graphJson = graphJson + '[';
				nodes.forEach(function (record) {
					logger.app.debug("record:" + JSON.stringify(record));
					if (idx >= 1) {
						graphJson = graphJson + ',';
					}

					let own_node = (record.properties.__xmail_nid == id);

					graphJson = graphJson + '{"group":"nodes",';

					graphJson = graphJson + '"data":{';	
					graphJson = graphJson +
						'"id": "' +
						record.id +
						'", ' +
						'"pid": "' +
						record.properties.id +
						'", ' +
						'"elementID": "' +
						record.properties.id +
						'", ' +
						' "nodeType": "' +
						record.properties.__tag +
						'", ' +
						' "maiml_type": "' +
						record.properties.__maiml_type +
						'", ' +
						' "layer": "' +
						record.properties.__layer +
						'", ' +
						'"parent": "' +
						record.properties.__xmail_nid +
						'", ' +
						'"ownNode": "' +
						JSON.stringify(own_node) +
						'"';
					if (!own_node) {
						graphJson = graphJson + ',"type": "otherNode"';
						graphJson = graphJson + ',"readonly": "true"';
					} else {
						graphJson = graphJson + ',"type": "ownNode"';
						graphJson = graphJson + ',"readonly": "false"';
					}
					if (idx == 1) {
						graphJson = graphJson + ',"root": true';
					}
					if (!parents.includes(record.properties.__xmail_nid)) {
						parents.push(record.properties.__xmail_nid);
					}

					graphJson = graphJson + '},';


					// add 240910 positionを追加する
					//record.properties.__xmail_nid を用いてfdataを取得する
					if (fdataList[maimlnid] && fdataList[maimlnid].fdata) {
						var fdata = fdataList[maimlnid].fdata;
						var pt = false;
						var positions;
						fdata.forEach(item => {
							//logger.app.debug("jsonString:" + item);
							try {
								if (record.properties.id === item.data.pid) {	//pidの一致
									pt = true;
									positions = item.position;
								};
							} catch (error) {
								logger.app.error(C_MODEL + error.message);
							}
						});

						if (pt) {
							graphJson = graphJson + '"position":';
							graphJson = graphJson + JSON.stringify(positions);
							graphJson = graphJson + ',';
						}
					} else {
						logger.app.debug(C_MODEL + "fdata is null.");
					}

					graphJson = graphJson + 
						'"classes": "' +
						record.properties.__tag +
						'"';

					graphJson = graphJson + '}';

					idx = idx + 1;
				});

				/*
				 * groups json
				 */
				//idx = 0;
				parents.forEach(function(elem) {
					graphJson = graphJson + ',';
					graphJson = graphJson + '{"group":"nodes", "data":{' +
						'"id": "' + elem +
						'", ' +
						'"name": "' +
						'", ' +
						' "nodeType": "parent"';
					if (elem == id) {
						graphJson = graphJson + ',"readonly": "true"';
						graphJson = graphJson + ',"type": "ownParent"';
						//graphJson = graphJson + ',"readonly": "true"';
					} else {
						graphJson = graphJson + ',"readonly": "false"';
						graphJson = graphJson + ',"type": "otherParent"';
					}
					graphJson = graphJson + '} }';
					idx = idx + 1;
				});

				/*
				 * edges json
				 */
				//idx = 0;
				edges.forEach(function(
					record
				) {
					let own_node = (record.properties.__xmail_nid == id);
					logger.app.debug("record.__xmail_nid:" + record.properties.__xmail_nid);
					logger.app.debug("id:"+id);
					logger.app.debug("own_node:"+own_node);

					if (idx >= 1) {
						graphJson = graphJson + ',';
					}

					graphJson = graphJson + '{"group":"edges", "data":{';

					graphJson =
						graphJson +
						' "source": "' +
						record.startNode +
						'", ' +
						' "target": "' +
						record.endNode +
						'", ' +
						' "edgetype": "' +
						record.properties.__edge_kind +
						'", ' +
						'"ownNode": "' +
						JSON.stringify(own_node) +
						'"';
						//Do not to display "PNarc" on the conneciton
						if (record.type=='SAME'){
							graphJson = 
								graphJson +
								', "arrow":  "none"';
						}
						graphJson =
							graphJson +
							'} }';
					idx = idx + 1;
				});
				graphJson = graphJson + '] ';
				logger.app.debug(C_MODEL +'GraphJson : ' + graphJson);

				resolve(graphJson);
			}
		);
	});
};


// 20240912 add
/*
 * PN図の座標記録
 *・GraphDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果を元に座標ファイルを保存
 *
 * @returns true
 * @throws {cypher error}
*/
const path = require('path');
const fs = require('fs');
const { json } = require('body-parser');
exports.pn_position = async function(id,position){
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	let cypher = cypher_api.get_cypher('get_docuuid',id);
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	// document要素のuuidを取得
	var uuid;
	await session
		.run(cypher)
		.then(function (result) {
			logger.app.debug(JSON.stringify(result.records));
			result.records.forEach(function (record) {
				logger.app.debug(JSON.stringify(record));
				session.close();
				uuid = record.get('uuid');
			});
		})
		.catch(function (error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});

	const m_position = position.split('\n')
		.filter(line => line.trim() !== '') // 空行を除去
		.map(jsonString => {
			try {
				const obj = JSON.parse(jsonString);
				const po = obj.position;
				const parentid = obj.data.parent;
				if (id === parentid) {
					var pojson;
					pojson = '{"data":{"id":"'+obj.data.id+'","pid":"'+obj.data.pid+'"},"position":'+JSON.stringify(po)+'}';
					return pojson;
				} else {
					return null;
				}
			} catch (error) {
				logger.app.error(C_MODEL + error.message);
				return null; // パースエラーの場合はnull
			}
		})
		.filter(item => item !== null);

	//var filename = id + '_' + uuid + '.position'
	var filename = uuid + '.position'
	var filepath = path.join(__dirname, '../exports/pnmlpositions', filename)
	// save file
	fs.writeFile(filepath, JSON.stringify(m_position), 'utf8', (error) => {
		if (error) {
			logger.app.error(C_MODEL + error.message);
			throw error;
		}
	});

	driver.close();
	var t = true;
	return t;
};



/*
 * [UI-3] node詳細情報取得（個別）
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットからGraphJsonを生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns graphJson - node詳細情報JSON
 * @throws {cypher error}
 */
exports.node_list = async function(node_list) {


	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	logger.app.debug(C_MODEL + 'node_list: ' + JSON.stringify(node_list));
	let cypher = cypher_api.get_cypher('get_details_bylist', node_list);
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	var graphJson = '[';
	var idx = 0;

	await session
		.run(cypher)
		.then(function(result) {
			result.records.forEach(function(record) {
				session.close();

				if (idx >= 1) {
					graphJson = graphJson + ',';
				}

				graphJson =
					graphJson +
					'{"place_nid": "' +
					record.get('place_nid') +
					'", ' +
					'"place_id": "' +
					record.get('place_id') +
					'", ' +
					'"placeRef_nid": "' +
					record.get('placeRef_nid') +
					'", ' +
					'"placeRef_id": "' +
					record.get('placeRef_id') +
					'", ' +
					'"template_nid": "' +
					record.get('template_nid') +
					'", ' +
					'"template_tag": "' +
					record.get('template_tag') +
					'", ' +
					'"template_id": "' +
					record.get('template_id') +
					'", ' +
					'"template_uuid": "' +
					record.get('template_uuid') +
					'", ' +
					'"template_name": "' +
					record.get('template_name') +
					'", ' +
					'"template_description": "' +
					record.get('template_description') +
					'"} ';
				idx = idx + 1;
			});

			graphJson = graphJson + ']';
		})
		.catch(function(error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});

	logger.app.debug(C_MODEL + 'GraphJson : ' + graphJson);
	driver.close();
	return graphJson;
};

/*
 * [UI-3] node詳細情報取得（一括取得）
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットからGraphJsonを生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns graphJson - node詳細情報JSON
 * @throws {cypher error}
 */
exports.node_all = async function(node_id) {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	var cypher =
		`match (a:XMAIL)
                    -[:XML_Root]->(d)
                    -[:XML_Child]->(pr {__tag: 'protocol'})
                    -[:XML_Child]->(me {__tag: 'method'})
                    -[:XML_Child]->(pg {__tag: 'program'})
                    -[:XML_Child]->(pn {__tag: 'pnml'})
                    -[:XML_Child]->(pl {__tag: 'place'})
                where id(a)=` +
		node_id +
		`
                optional match
					(pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
				where plR.ref = pl.id
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
                    ded.value as template_description;`;
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	var graphJson = '[';
	var idx = 0;

	await session
		.run(cypher)
		.then(function(result) {
			result.records.forEach(function(record) {
				session.close();

				if (idx >= 1) {
					graphJson = graphJson + ',';
				}

				graphJson =
					graphJson +
					'{"place_nid": "' +
					record.get('place_nid') +
					'", ' +
					'"place_id": "' +
					record.get('place_id') +
					'", ' +
					'"placeRef_nid": "' +
					record.get('placeRef_nid') +
					'", ' +
					'"placeRef_id": "' +
					record.get('placeRef_id') +
					'", ' +
					'"template_nid": "' +
					record.get('template_nid') +
					'", ' +
					'"template_tag": "' +
					record.get('template_tag') +
					'", ' +
					'"template_id": "' +
					record.get('template_id') +
					'", ' +
					'"template_uuid": "' +
					record.get('template_uuid') +
					'", ' +
					'"template_name": "' +
					record.get('template_name') +
					'", ' +
					'"template_description": "' +
					record.get('template_description') +
					'"} ';
				idx = idx + 1;
			});

			graphJson = graphJson + ']';
		})
		.catch(function(error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});

	logger.app.debug(C_MODEL + 'GraphJson : ' + graphJson);
	driver.close();
	return graphJson;
};

/*
 * [UI-4] ペトリネットnode詳細情報取得
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットからGraphJsonを生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns graphJson - node詳細情報JSON
 * @throws {cypher error}
 */
exports.node_material = async function(node_id) {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	/* */
	let cypher = cypher_api.get_cypher('get_generals', node_id);
	//let cypher = cypher_api.get_cypher('get_properties', node_id);
	/*
	var cypher =
		`match
			(pr {__tag: 'protocol'})
			-[:XML_Child]->(me {__tag: 'method'})
			-[:XML_Child]->(pg {__tag: 'program'})
			-[:XML_Child]->(pn {__tag: 'pnml'})
			-[:XML_Child]->(pl {__tag: 'place'}),
			(pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
		where
			id(pl)=` +
		node_id +
		`
			and plR.ref = pl.id
		with te
		match
			(te)-[:XML_Child*]->(prop {__tag: 'property'})
		optional match
			(prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
		optional match
			(prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
		optional match
			(prop)<-[:XML_Child]-(parent {__tag: 'property'})
		return
			te.__tag as tag_name,
			te.id as template,
			id(prop) as nid,
			id(parent) as parent_nid,
			dd.value as description,
			vd.value as value,
			properties(prop) as attrib;
		`;
	*/
	logger.app.debug(C_MODEL + 'Cypher : ' + cypher.toString());

	//var graphJson = '[';
	
	// property,content
	//var graphJson1 = '[';
	var graphJson1;
	var idx = 0;
	await session
		.run(cypher)
		.then(function(result) {
			result.records.forEach(function(record) {
				session.close();


				var attrib = record.get('attrib');
				delete attrib.__tag;
				
				var arrayTmp = {
					'nid': String(record.get('nid')),
					'parent_nid': String(record.get('parent_nid')),
					'description': record.get('description'),
					'value': record.get('value') ? record.get('value').substring(0, 96): "",  /* 20240523 edit */
					'attrib': jsonPrettier(attrib)
				};

				if (idx >= 1) {
					graphJson1 = graphJson1 + ',' + JSON.stringify(arrayTmp);
					//graphJson1 = graphJson1 + ',';
				}else {
					//graphJson1 = graphJson1 + JSON.stringify(arrayTmp);
					graphJson1 = JSON.stringify(arrayTmp);
				};
				//graphJson1 = graphJson1 + JSON.stringify(arrayTmp);
				idx = idx + 1;
			});
		})
		.catch(function(error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});
	//graphJson.graphJson1 = graphJson1;
	//graphJson = graphJson + graphJson;
	logger.app.debug('graphJson1のデータ');
	logger.app.debug(C_MODEL + 'GraphJson1 : ' + graphJson1);

	
	// 20240906 add
	// get insertion contents
	const session2 = driver.session();
	let cypher2 = cypher_api.get_cypher('get_insertions', node_id);
	
	//var graphJson2 = '[';
	var graphJson2;
	var idx = 0;
	await session2
		.run(cypher2)
		.then(function (result2) {
			result2.records.forEach(function (record) {
				session2.close();

				var arrayTmp2 = {
					'uri': record.get('uri'),
					'hash': record.get('hash'),
					'format': record.get('format'),
					'uuid': record.get('uuid')
				};

				if (idx >= 1) {
					graphJson2 = graphJson2 + ',' + JSON.stringify(arrayTmp2);
				}else {
					//graphJson2 = graphJson2 + JSON.stringify(arrayTmp2);
					graphJson2 = JSON.stringify(arrayTmp2);
				};
				idx = idx + 1;
			});
		})
		.catch(function (error) {
			session2.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});
	
	logger.app.debug('graphJson２のデータ');
	logger.app.debug(C_MODEL + 'GraphJson2 : ' + graphJson2);

	var graphJson = [{
		graphJson1 : graphJson1,
		graphJson2 : graphJson2
	}];
	//graphJson = graphJson + ']';
	logger.app.debug(C_MODEL + 'GraphJson : ' + graphJson);

	driver.close();
	return graphJson;
};

function jsonPrettier(json) {
	var result = '';
	result = JSON.stringify(json, null, 2);
	result = result.replace(/[\"]/g, '');
	result = result.replace('{', '');
	result = result.replace('}', '');
	result = result.replace(/,/g, '<br>');

	return result;
}
