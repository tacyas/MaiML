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
			function(error, response, body) {
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
				graphJson = graphJson + '[';
				nodes.forEach(function(record) {
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
						'"name": "' +
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
				logger.app.debug(C_MODEL + 'GraphJson : ' + graphJson);

				resolve(graphJson);
			}
		);
	});
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

	let cypher = cypher_api.get_cypher('get_properties', node_id);
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

				var attrib = record.get('attrib');
				delete attrib.__tag;

				var arrayTmp = {
					'nid': String(record.get('nid')),
					'parent_nid': String(record.get('parent_nid')),
					'description': record.get('description'),
					'value': record.get('value'),
					'attrib': jsonPrettier(attrib)
				};
				graphJson =
					graphJson + JSON.stringify(arrayTmp);
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

function jsonPrettier(json) {
	var result = '';
	result = JSON.stringify(json, null, 2);
	result = result.replace(/[\"]/g, '');
	result = result.replace('{', '');
	result = result.replace('}', '');
	result = result.replace(/,/g, '<br>');

	return result;
}
