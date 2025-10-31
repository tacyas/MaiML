'use strict';

/*const neo4j = require('neo4j-driver').v1;*/
const neo4j = require('neo4j-driver');
const logger = require('../common/log-utils.js');
const cypher_api = require('../../graph-db/app/Cypher/cypher_api.js');
const fs = require('fs');
const exec = require('child_process').execSync;
const path = require('path');

const graphDb = process.env.GRAPH_DB_IP || '127.0.0.1';
/* const uri = 'bolt://' + graphDb + ':7687'; */
const uri = 'neo4j://' + graphDb + ':7687';
const user = process.env.GRAPH_USER || '';
const password = process.env.GRAPH_PWD || '';
const C_MODEL = '[xmail-edit]';
const path_to_scripts = '../../../graph-db/app/Script/';

/*
 * XMAILデータ登録処理
 *
 * ・引数に指定されたファイルを一度添付ファイルとして保存する
 * ・xml2cypher.pyを実行する
 * ・GrpahDBに接続する
 * ・cypher実行：(1) XMAILファイル内のXML構造作成
 * ・(1)で登録できたcypherのreturn = IDを取得する
 * ・(2) XMAIL内のペトリネット構造作成用のCypher生成
 * ・cypher実行：(2) XMAIL内のペトリネット構造作成
 * ・(1), (2)共に正常終了した場合のみcommit、以外の場合はrollbackしてエラーを表示
 * ・一時ファイルを削除する
 *
 * @param {filename} filename - XMAILファイル名
 * @param {xmail} xmail - XMAILデータ内容
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns [0]: JSON for XHR
 * @throws {error}
 */
exports.upload = async function(filename, xmail) {
	var idx = 0;
	var cypher1 = '';
	var idNx = '';
	var graphJson = '[0]';
	var uploadResult = false;
	//const pythonapp = path.join(path_to_scripts, 'xmail_import.py');
	
	// 引数に指定されたファイルを一時ファイルとして保存する
	let tmpfile = path.join(__dirname, 'tmp', filename);
	logger.app.debug(C_MODEL + 'filename:' + tmpfile);

	//windows環境の場合コメント外す
	var targetStr = String.raw`\\`
	var regExp = new RegExp(targetStr, 'g') 
	tmpfile = tmpfile.replace(regExp, '/')
	logger.app.debug(C_MODEL + 'filename:' + tmpfile);

	try {
		fs.writeFileSync(tmpfile, xmail);
		logger.app.debug(C_MODEL + 'Temporary file created.');
	} catch (err) {
		logger.app.error(
			C_MODEL + 'Temporary file creation failed：' + err.message
		);
		throw err;
	}

	// 2025/7/8 edit パスに空白文字を含む場合、windows環境でエラーになるバグの修正
	// ファイルパスやオプションはすべてクォート（"）で囲む
	const pythonScript = path.join(path_to_scripts, 'xmail_import.py');
	const pythonScriptPath = path.join(__dirname, 'python', pythonScript);
	const quotedPython = `"${pythonScriptPath}"`;
	const quotedTmpfile = `"${tmpfile}"`;
	const quotedHost = `"${graphDb}"`;

	// xmail_importを実行する
	try {
		let cmd = `${quotedPython} --host ${quotedHost} ${quotedTmpfile}`;

		cypher1 = cmdExecute(cmd);
	} catch (err) {
		logger.app.error(C_MODEL + err.name + ':' + err.message);
		throw err;
	}

	/*
	// xmail_importを実行する
	try {
		var cmd = '';
		cmd =
			//'PYTHONIOENCODING=utf-8 ' +
			//'python ' +
			path.join(__dirname, 'python', pythonapp) +
			' ' +
			'--host "' +
			graphDb +
			'" ' +
			'"' +
			tmpfile +
			'"';
		cypher1 = cmdExecute(cmd);
	} catch (err) {
		logger.app.error(C_MODEL + err.name + ':' + err.message);
		throw err;
	}
	*/

	
	return graphJson;
};

/*
 * XMAILエクスポート処理
 *
 * ・現在編集中のペトリネット図をXMAILファイルに出力する
 * ・入力パラメータ（元ファイル）の存在チェックを行う
 * ・指定されたパラメータと使いxmail_export.pyを実行する
 *
 * @param {nodeid}} nodeid - ノードID
 * @param {infile} infile - 元XMAILファイル名
 * @param {outfile} outfile - エクスポートXMAILファイル名
 * @returns [0]: True
 * @throws {error}
 */
exports.export = async function(nodeid, infile, outfile) {
	//const original = path.join(__dirname, 'tmp', infile);
	const original = infile;
	const savepath = path.join(__dirname, '../exports', outfile);
	const pythonapp = path.join(path_to_scripts, 'xmail_export.py');

	logger.app.debug(C_MODEL + ' original:' + original);
	logger.app.debug(C_MODEL + ' savepath:' + savepath);
	logger.app.debug(C_MODEL + ' script:' + pythonapp);

	if( fs.existsSync(!original)) {
		logger.app.error(C_MODEL + ':' + original + ' file not found.');
		return false;
	}

	try {
		var cmd = '';
		var ret = '';

		cmd =
			//'PYTHONIOENCODING=utf-8 ' +
			//'python ' +
			path.join(__dirname, 'python', pythonapp) +
			' ' +
			'--host "' +
			graphDb +
			'" ' +
			'--node-id "' +
			nodeid +
			'" ' +
			'--output "' +
			savepath +
			//'" "' +
			//original +
			'"';
		ret = cmdExecute(cmd);
		logger.app.debug(C_MODEL + ':' + ret);
	} catch (err) {
		logger.app.error(C_MODEL + err.name + ':' + err.message);
		throw err;
	}

	//return true;
	return '"/download/' + outfile + '"';
};

/*
 * コマンド実行
 *
 * ・引数に指定されたコマンドを実行する。
 * ・実行環境においてコマンドライン上で"python"コマンドが実行できることが前提
 *
 * @param {cmd} cmd - コマンド（pythonスクリプト実行を想定)
 * @returns {stdout} コマンド実行後の標準出力結果
 * @throws {error}
 */
function cmdExecute(cmd) {
	const isWindows = process.platform === 'win32';
	if (isWindows) {
		cmd = 'set PYTHONIOENCODING=utf-8 && python ' + cmd;
	} else {
		cmd = 'PYTHONIOENCODING=utf-8 ' + cmd;
	}

	try {
		logger.app.debug('[cmdExecute]' + cmd);
		//var result = exec('python -c "import sys; print("hoge"); sys.exit(-1)"');
		//var result = exec(cmd, { timeout: 30000 });
		var result = exec(cmd, { timeout: 400000 });  //20240516 edit
		return result.toString();

	} catch (err) {
		logger.app.error('[cmdExecute]' + err.status);
		logger.app.error('[cmdExecute]' + err.stdout);
		logger.app.error('[cmdExecute]' + err.stderr);
		throw err;
	}
}

/*
 * XMAILデータ削除処理
 *
 * ・引数に指定されたNIDをキーに、GraphDBのXMAILデータ一式を削除する
 * ・GrpahDBに接続する
 * ・cypher実行：XMAILデータ削除
 *
 * @param {nid} nid - XMAIL一意キー
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns [0]: JSON for XHR
 * @throws {error}
 */
exports.delete = async function(nid) {
	var graphJson = '[0]';

	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	logger.app.debug(C_MODEL + 'Graph DB connected');

	var session = driver.session();
	var tx = session.beginTransaction();
	logger.app.debug(C_MODEL + 'tx created.');

	var cypher =
		`match p=(a:XMAIL)
					-[:XML_Root]->(r)
					-[:XML_Child|XML_Data*1..]->(n)
					where id(a)=` +
		nid +
		`
					detach delete p;`;
	logger.app.debug(C_MODEL + 'Delete Cypher : ' + cypher);

	try {
		await tx
			.run(cypher)
			.then(function(result) {
				logger.app.debug(
					C_MODEL + 'Cypher Counter:' + result.summary.counters
				);
				logger.app.debug(
					C_MODEL +
						'Cypher Notification:' +
						result.summary.notifications
				);
			})
			.catch(function(err) {
				if (err.message === undefined) {
					logger.app.debug(C_MODEL + 'Cypher Not affected.');
				} else {
					logger.app.error(
						C_MODEL + 'Cypher error rollbacked : ' + err.message
					);
					tx.rollback();
					throw err;
				}
			});
	} catch (err) {
		await tx.rollback();
		logger.app.error(C_MODEL + 'Error rollbacked : ' + err.message);
		throw err;
	} finally {
		await tx.commit();
		logger.app.debug(C_MODEL + 'Commit completed.');
		await session.close();
		logger.app.debug(C_MODEL + 'Finally session closed.');
	}

	driver.close();
	
	return graphJson;
};

/*
 * Place/TransitionのPNarcを作成可否チェック
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットから戻り値を生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns boolean - PNarc作成可否
 * @throws {cypher error}
 */
exports.pnarc_check = async function(src_nid, dst_nid) {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	logger.app.debug(C_MODEL + 'Graph DB connected.');

	let cypher = cypher_api.get_cypher('test_PNarc', src_nid, dst_nid);
	logger.app.debug(C_MODEL + 'test_PNarc : ' + cypher.toString());

	var checkResult = false;

	await session
		.run(cypher)
		.then(function(result) {
			session.close();
			checkResult = result.records[0]['_fields'];
			logger.app.info('test_PNarc result=' + checkResult);
		})
		.catch(function(error) {
			session.close();
			logger.app.error(C_MODEL + error.message);
			throw error;
		});
	
	driver.close();

	return checkResult;
};

/*
 * Place/TransitionのPNarcを作成する
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットから戻り値を生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns boolean - PNarc作成結果
 * @throws {cypher error}
 */
exports.pnarc_create = async function(src_nid, dst_nid) {
	try {
		let cypher = cypher_api.get_cypher('create_PNedge', src_nid, dst_nid);
		logger.app.debug(C_MODEL + 'create_PNarc : ' + cypher.toString());

		var ret = run_cud_query(cypher);
	} catch (err) {
		logger.app.error(C_MODEL + 'pnarc_create' + err.status + ' ' + err.message);
		throw err;
	}

	return ret;
};

/*
 * Place/TransitionのPNarcを削除する
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットから戻り値を生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns boolean - PNarc削除結果
 * @throws {cypher error}
 */
exports.pnarc_delete = async function(src_nid, dst_nid) {
	try {
		let cypher = cypher_api.get_cypher('delete_PNedge', src_nid, dst_nid);
		logger.app.debug(C_MODEL + 'delete_PNarc : ' + cypher.toString());

		var ret = run_cud_query(cypher);
	} catch (err) {
		logger.app.error(C_MODEL + 'pnarc_delete' + err.status + ' ' + err.message);
		throw err;
	}

	return ret;
};

/*
 * Place/TransitionのPNarcを削除する
 *・GrpahDBへ接続
 *・Cypher生成
 *・Cypher実行
 *・結果データセットから戻り値を生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @returns boolean - PNarc削除結果
 * @throws {cypher error}
 */
exports.node_creation = async function(nid, id, kind) {
	try {
		let cypher = cypher_api.get_cypher('create_PNnode', nid, id, kind);
		logger.app.debug(C_MODEL + 'create_PNnode : ' + cypher.toString());

		var ret = run_cud_query(cypher);
	} catch (err) {
		logger.app.error(C_MODEL + 'node_creation' + err.status + ' ' + err.message);
		throw err;
	}

	return ret;
};

/*
 * 更新系のCypherを実行する関数
 *・GrpahDBへ接続
 *・Cypher実行
 *・実行結果を生成
 *
 * @see https://neo4j.com/docs/api/javascript-driver/current/
 * @param string - Cypher
 * @param string - Param (Optional)
 * @returns boolean - 更新件数 > 0 = True、以外はfalse
 * @throws {cypher error}
 */
async function run_cud_query(cypher, params = {}) {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
	const session = driver.session();
	var tx = session.beginTransaction();
	var ret = {};

	try {
		await tx
			.run({text: cypher, parameters: params})
			.then(function(result){
				/*
				logger.app.debug('== summary');
				logger.app.debug(result.summary.counters._stats);
		
				var sum = result.summary.counters._stats.nodesCreated +
					result.summary.counters._stats.nodesDeleted +
					result.summary.counters._stats.relationshipsCreated +
					result.summary.counters._stats.relationshipsDeleted +
					result.summary.counters._stats.propertiesSet +
					result.summary.counters._stats.labelsAdded +
					result.summary.counters._stats.labelsRemoved +
					result.summary.counters._stats.indexesAdded +
					result.summary.counters._stats.indexesRemoved +
					result.summary.counters._stats.constraintsAdded +
					result.summary.counters._stats.constraintsRemoved;
				*/
				var sum = result.summary.counters.containsUpdates();
				
				logger.app.info('cud cypher exec affected = ' + sum);
				if (sum) {
					var obj = {};
					[...result.records[0].entries()].forEach( (e) => {
						obj[e[0]] = e[1].toString();
					});
					logger.app.debug(C_MODEL + 'records[0]: ' + JSON.stringify(obj));
					ret.success = true;
					ret.data = obj;
				} else {
					ret.success = false;
				}
			})
			.catch(function(err) {
				if (err.message === undefined) {
					logger.app.debug(C_MODEL + 'Cypher Not affected.');
				} else {
					logger.app.error(
						C_MODEL + 'Cypher error rollbacked : ' + err.message
					);
					tx.rollback();
					throw err;
				}
			});

	}
	catch(error) {
		await tx.rollback();
		logger.app.error(C_MODEL + 'Error rollbacked : ' + error.message);
		await session.close();
		throw error;
	}
	finally {
		await tx.commit();
		logger.app.debug(C_MODEL + 'Commit completed.');
		await session.close();
	}

	await driver.close();
	return ret;
}
