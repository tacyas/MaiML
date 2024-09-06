'use strict';

var gdata = ''; // eslint-disable-line
var cy;
// layout settings
const layoutConfig_grid = {
	name: 'grid',
	animate: true,
	fit: true,
	avoidOverlap: true,
	ready: e => {
		e.cy.fit()
		e.cy.center()
	}
};
const layoutConfig_cose = {
	name: 'cose',
	//animate: 'end',
	//animationDuration: 1000,
	//fit: true,
	avoidOverlap: true,
	infinite: true,
	ready: e => {
		e.cy.fit()
		e.cy.center()
	}
};
const layoutConfig_cola = {
    name: 'cola',
    animate: false,
    flow: { axis: 'x' },
	// name: 'cose-bilkent',
	// animate: 'end',
	// animationEasing: 'ease-out',
	// animationDuration: 1000,
	// randomize: true
};
const layoutConfig = layoutConfig_cola;


/* global $ alchemy getParam formatErrorMessage */
/**
 * XMAILペトリネット図照会画面の初期処理
 * ・ペトリネット図の描画処理呼び出し
 */
$(document).ready(function() {
	gdata = '';
	document.getElementById('navbarNavImport').style.visibility = 'hidden';

	/* eslint-disable no-unused-vars */
	var table = $('#datagrid').DataTable({
		paging: false,
		searching: false,
		select: true,
		columns: [
			{ data: 'nid' },
			{ data: 'parent_nid' },
			{ data: 'description' },
			{ data: 'value' },
			{ data: 'attrib' }
		],
		columnDefs: [
			{
				targets: [2, 4],
				className: 'left-aligned-cell'
			}
		],
		order: [[0, 'asc']]
	});

	loadPetrinet();
});

/**
 * ペトリネット図の描画
 * ・ペトリネット図構成データの取得
 * ・取得したデータからペトリネット図を描画
 * @function
 * @see https://js.cytoscape.org/#tyle/edse
 * @returns
 * @throws {xhr error}
 */
 function loadPetrinet() {
	$('#cy').empty();

	$.ajax({
		url: '/petrinet/xmail-petrinet',
		type: 'post',
		dataType: 'json',
		data: {
			id: getParam('id')
		},
		success: function(data) {

			cy = cytoscape({
				container: $('#cy'),
				style: [
					{
						selector: 'node',
						style: {
							// 20240906 update
							'label': function (ele) { return ele.data('name') },
							//'label': function(ele) { return '[' + ele.data('id') + '] ' + ele.data('name') },
							'color': 'black',
							'text-outline-color': 'white',
							'text-outline-width': 1,
							'background-color': 'lightblue',
							'background-opacity': 0.5,
							'border-color': 'black',
							'border-width': 1
						}
					},
					{
						// place node
						selector: 'node',
						style: {
							'shape': 'ellipse',
							'width': 24,
							'height': 24,
						}
					},
					//nodeStyle
					//layer
					{
						selector: 'node[layer = "0"]',
						style: {
							'width': 24,
							'height': 24,
						}
					},
					{
						selector: 'node[layer = "1"]',
						style: {
							'width': 12,
							'height': 12,
							//'border-style' : 'dashed',
							'background-opacity': 0,
						}
					},
					{
						selector: 'node[layer = "2"]',
						style: {
							'width': 12,
							'height': 12,
							'background-color': 'black',
						}
					},
					//_maiml_type
					{
						selector: 'node[maiml_type = "M"]',
						style: {
							'shape': 'ellipse',
						}
					},
					{
						selector: 'node[maiml_type = "C"]',
						style: {
							'shape': 'pentagon',
						}
					},
					{
						selector: 'node[maiml_type = "R"]',
						style: {
							'shape': 'rectangle',
						}
					},
					{
						selector: 'node[maiml_type = "undefined"]',
						style: {
							'shape': 'ellipse',
							'border-style' : 'dashed',
						}
					},
					// transition node
					{
						selector: 'node[nodeType = "transition"]',
						style: {
							'shape': 'rectangle',
							'width': 6,
							'height': 48,
							'border-style' : 'solid',
						}
					},
					{
						//otherNode 
						selector : 'node[type = "otherNode"]',
						style: {
							'background-color': 'gray',
						}
					},
					{
						//ownnode Group
						selector : 'node[type = "ownParent"]',
						style: {
							'background-color': 'aliceblue',
						}
					},
					{
						//othernode Group
						selector : 'node[type = "otherParent"]',
						style: {
							'background-color': 'lightgray',
						}
					},
					{
						//otherNode 
						selector : '.class',
						style: {
							'background-color': 'red',
						}
					},
					{
						//otherNode 
						selector : '.instance',
						style: {
							'background-color': 'yellow',
						}
					},
					//edgeStyle
					{
						selector: 'edge',
						style: {
							'width': 1,
							'curve-style': 'bezier',
							'line-color': 'steelblue',
							'target-arrow-color': 'steelblue',
							'target-arrow-shape': 'triangle',
							'target-arrow-fill': 'filled',
							'arrow-scale': 1,
							'label': '',
						}
					},
					//edge-arrow
					{
						selector : 'edge[arrow = "none"]',
						style: {
							'width': 1,
							'target-arrow-shape' : 'data(arrow)',
						}
					},
					//edge-edgetype
					{
						selector : 'edge[edgetype = "SAME"]',
						style: {
							//'line-style': 'dashed',
							'line-style': 'dotted',
							'line-color': 'lightgreen',
						}
					},
					{
						selector : 'edge[edgetype = "arc"]',
						style: {
							'width':4,
						}
					},
					{
						selector : 'edge[edgetype = "placeRef"]',
						style: {
						}
					},
					{
						selector : 'edge[edgetype = "templateRef"]',
						style: {
							'line-style': 'dashed',
						}
					},
					{
						selector : 'edge[edgetype = "ref"]',
						style: {
						}
					},
					{
						selector : 'edge[edgetype = "instanceRef"]',
						style: {
							'line-style': 'dashed',
						}
					},
					//edge-ownNode
					{
						selector : 'edge[ownNode = "true"]',
						style: {
							'line-color': 'steelblue',
							'target-arrow-color': 'steelblue',
						}
					},
					{
						selector : 'edge[ownNode =  "false"]',
						style: {
							'line-color': 'gray',
							'target-arrow-color': 'gray',
						}
					},
					{
						selector: ':selected',
						style: {
							'background-color': 'magenta',
							'background-opacity': 1.0,
							'border-width': 2,
							'line-color': 'magenta',
							'target-arrow-color': 'magenta',
							'z-index': 1,
						}
					},
					{
						selector: 'edge:selected',
						style: {
							'label': function(ele) { return ele.data('edgetype') },
							'color': 'blue',
							'text-outline-opacity': 0,
							'text-background-color': 'white',
							'text-background-opacity': 1,
							'text-border-opacity': 1,
							'text-border-color': 'blue',
							'text-border-width': 1,
							'text-background-padding': 2,
						}
					},
				],
				//wheelSensitivity: 1,
				layout: layoutConfig,
				//layout: {
				//	name: 'preset'
				//},
				elements: data,
			})
	
			var tappedBefore;
			var tappedTimeout;

			//Node click event
			cy.on('tap', 'node', function(evt) {
				var target = evt.target;
				var data = target.json().data;
				var id = data["id"];
				var nodeType = data["nodeType"];
				var pid = data["pid"];
				var parentGroup = data["parent"];
				var ownNode = data["ownNode"];
				var maiml_type = data["maiml_type"];
				var layer = '';
				
				if (data["layer"] == '0') {
					layer = 'Petri net';
				} else if (data["layer"] == '1') {
					layer = 'Class';
				} else if (data["layer"] == '2') {
					layer = 'Instance';
				}

				if (nodeType=="parent"){
					evt.target.nodes().unselectify();
				}

				if (nodeType!="parent"){
					if (ownNode=="true"){
						if ($('#txtNewDestinationNode').val() != '') {
							$('#txtNewSourceNode').val(id);
							$('#txtNewDestinationNode').val('');
						} else if($('#txtNewSourceNode').val() =='') {
							$('#txtNewSourceNode').val(id);
						} else {
							if ($('#txtNewSourceNode').val() == id) {
								$('#txtNewSourceNode').val(id);
								$('#txtNewDestinationNode').val('');
							}　else {
								$('#txtNewDestinationNode').val(id);
							}
						}
					} else {
						$('#txtNewSourceNode').val('');
						$('#txtNewDestinationNode').val('');
					}

					//Node Detailsセット
					$('#txtNode').val(''); 
					$('#txtId').val('');
					$('#txtPlaceId').val('');
					$('#txtNode').val(id); 
					$('#txtId').val(maiml_type);
					$('#txtPlaceId').val(pid);
					$('#txtXmailNid').val(parentGroup);
					$('#txtLayer').val(layer);

					//Templatesセット
					for (var ii = 1; ii < 4; ii++) {
						$('#txtPlaceRefId' + ii).val('');
						$('#txtTemplateTag' + ii).val('');
						$('#txtTemplateId' + ii).val('');
						$('#txtTemplateUuId' + ii).val('');
						$('#txtTemplateName' + ii).val('');
						$('#txtTemplateDescription' + ii).val(''); 
					}
					var icnt = 1;
					for (var ii = 0; ii < gdata.length; ii++) {
						if (gdata[ii].place_nid == id) {
							$('#txtPlaceId').val(gdata[ii].place_id);
							$('#txtPlaceRefId' + icnt).val(gdata[ii].placeRef_id);
							$('#txtTemplateTag' + icnt).val(gdata[ii].template_tag);
							$('#txtTemplateId' + icnt).val(gdata[ii].template_id);
							$('#txtTemplateUuId' + icnt).val(gdata[ii].template_uuid);
							$('#txtTemplateName' + icnt).val(gdata[ii].template_name);
							$('#txtTemplateDescription' + icnt).val(gdata[ii].template_description); 
							icnt = icnt + 1;
						}
					}
					getNodeMaterial(id);	
				}

			})

			//Edge click event
			cy.on('select', 'edge', function(evt) {
				var tgt = evt.target;
				var data = tgt.json().data;
				var source = data["source"];
				var target = data["target"];
				var arrow = data["arrow"];
				var ownNode = data["ownNode"];
				
				if (ownNode=="true"){
					if(arrow!="none"){
						$('#txtSourceNode').val(source);
						$('#txtDestinationNode').val(target);
					}
				}
			})

			//Edge unselect event
			cy.on('unselect', 'edge', function(evt) {
				$('#txtSourceNode').val('');
				$('#txtDestinationNode').val('');
			});

			//Double tap implementation event
			cy.on('tap', function(event) {
				var tappedNow = event.target;
				if (tappedTimeout && tappedBefore) {
					clearTimeout(tappedTimeout);
				}
				if(tappedBefore === tappedNow) {
					tappedNow.trigger('doubleTap');
					tappedBefore = null;
				} else {
					tappedTimeout = setTimeout(function(){ tappedBefore = null; }, 300);
					tappedBefore = tappedNow;
				}
				});

			//Double tap event
			cy.on('doubleTap', 'node', function(event) { 
				var url = new URL(window.location.href);
				var params = url.searchParams;

				if (event.target.json().data["readonly"] == "false"){
					if (event.target.json().data["nodeType"] == "parent"){
						params.set('id',event.target.json().data["id"]);
						window.location.href = url;
						//window.location.replace(url);
						loadPetrinet();
					}
				}
			});

			//getNodeDetails(getParam('id'));
			getTemplatesByList(
				data.filter(x => (x.group === 'nodes') && (x.data.nodeType !== 'parent'))
				.map(x => Number(x.data.id))
			);
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'ペトリネット図の取得に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
 * ノード詳細情報取得（対象ノードリスト指定）
 * ・ノードリストで列挙したノードの詳細情報を取得する。
 * ・ここで取得した内容はメモリ上に保持され、ペトリネット図のノード選択時に参照される。
 * @param {array} node_list - UI1で取得したペトリネットに含まれるノードのNIDの配列を指定する。
 * @returns
 * @throws {xhr error}
 */
function getTemplatesByList(node_list) {
	$('#txtPlaceId').val('');
	$('#txtPlaceRefId').val('');
	$('#txtTemplateTag').val('');
	$('#txtTemplateId').val('');
	$('#txtTemplateUuId').val('');
	$('#txtTemplateName').val('');
	$('#txtTemplateDescription').val('');
	$('#txtLayer').val('');

	$.ajax({
		url: '/node/node-list',
		type: 'post',
		dataType: 'json',
		data: {
			node_list: JSON.stringify(node_list)
		},
		success: function(data) {
			//store retrived data into memory
			gdata = data;
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'ノード詳細情報の取得に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
 * ノード詳細情報取得
 * ・XMAILに紐づくノードの詳細情報を取得する。
 * ・ここで取得した内容はメモリ上に保持され、ペトリネット図のノード選択時に参照される。
 * @param {number} node_id - UI1で取得したNIDを指定する。
 * @returns
 * @throws {xhr error}
 */
function getNodeDetails(node_id) {
	$('#txtPlaceId').val('');
	$('#txtPlaceRefId').val('');
	$('#txtTemplateTag').val('');
	$('#txtTemplateId').val('');
	$('#txtTemplateUuId').val('');
	$('#txtTemplateName').val('');
	$('#txtTemplateDescription').val('');
	$('#txtLayer').val('');

	$.ajax({
		url: '/node',
		type: 'post',
		dataType: 'json',
		data: {
			node_id: node_id
		},
		success: function(data) {
			//store retrived data into memory
			gdata = data;
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'ノード詳細情報の取得に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
 * ノード詳細情報取得
 * ・XMAILに紐づくノードの詳細情報を取得する。
 * ・ここで取得した内容はメモリ上に保持され、ペトリネット図のノード選択時に参照される。
 * @param {number} node_id - UI1で取得したNIDを指定する。
 * @returns
 * @throws {xhr error}
 */
function getNodeMaterial(node_id) {
	// eslint-disable-line

	$.ajax({
		url: '/node/node-material',
		type: 'post',
		dataType: 'json',
		data: {
			node_id: node_id
		},
		success: function(data) {
			$('#datagrid')
				.dataTable()
				.fnClearTable();
			if (data.length > 0) {
				$('#datagrid')
					.dataTable()
					.fnAddData(data);
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'ノードマテリアル情報の取得に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
* ノード選択エリアのクリアボタンイベントハンドラ
*/
$('#btnClearDelSelect').click(function() {
	// var cy = window.cy;
	//formatTestMessage(data);
	$('#txtSourceNode').val('');
	$('#txtDestinationNode').val('');
});
$('#btnClearNewSelect').click(function() {
	$('#txtNewSourceNode').val('');
	$('#txtNewDestinationNode').val('');
});

/**
* Node追加モーダル初期表示処理
*/
$('#modalNodeCreation').on('shown.bs.modal', function () {
	$('#txtNodeId').val(getParam('id'));
	$('#txtNewId').trigger('focus');
});

/**
* Node間のコネクションを削除するボタンのイベントハンドラ
*/
$('#btnDeleteConn').click(function() {
	let src_nid = $('#txtSourceNode').val();
	let dst_nid = $('#txtDestinationNode').val();
	
	if (src_nid == '' || dst_nid == '') {
		alert('接続を削除するために、Source及びDestinationを必ず指定してください。');
	} else {
		var res = confirm('指定された接続を削除します。よろしいですか？');
		if( res == true ) {
			deletePNarc(src_nid, dst_nid);
		}
	}
});

/**
* 新たなNode勘のコネクション作成するボタンのイベントハンドラ
*/
$('#btnCreateConn').click(function() {
	let src_nid = $('#txtNewSourceNode').val();
	let dst_nid = $('#txtNewDestinationNode').val();
	
	if (src_nid == '' || dst_nid == '') {
		alert('接続を作成するために、Source及びDestinationを必ず指定してください。');
	} else {
		var res = confirm('指定された接続を作成します。よろしいですか？');
		if( res == true ) {
			createPNarc(src_nid, dst_nid);
		}
	}
});

/**
* 新しいノード（Place or Transition）の実行ボタンのイベントハンドラ
*/
$('#execAddNode').click(function() {
	let nid = $('#txtNodeId').val();
	let id = $('#txtNewId').val();
	let kind = $('#lstNodeType').val();

	if (nid == '' || id == '' || kind == '') {
		alert('新たなノードを作成するために、IDを必ず指定してください。');
	} else {
		createNode(nid, id, kind);
	}
});

/**
* XMAILファイルのエクスポート
*/
$('#execExportXmail').click(function() {
	let outfilename = $('#txtFileName').val();

	if (outfilename == '') {
		alert('出力ファイル名は必ず指定してください。');
	} else {
		var res = confirm('MaiMLデータをエクスポートします。よろしいですか？');
		if( res == true ) {
			exportXMAIL(getParam('id'), getParam('infile'), outfilename);
		}
	}
});

/**
 * PNarc作成チェック
 * ・指定されたSourceとDestinationを使いtest_PNarcを呼び出す。
 * ・作成可否チェック結果を元に画面を制御する。
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @returns {Boolean} True (作成可能) / False (作成不可能)
 * @throws {xhr error}
 */
const checkPNarcCreation = async function(src_nid, dst_nid) {

	$.ajax({
		url: '/node-edit/pnarc-check',
		type: 'post',
		dataType: 'json',
		data: {
			src_nid: src_nid,
			dst_nid: dst_nid
		},
		success: function(data) {
			return data;
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = '接続の作成チェックに失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
			return false;
		}
	});
};

/**
 * PNarc作成
 * ・指定されたSourceとDestinationを使いPNarcを作成する。
 * ・作成結果を元に画面を制御する。
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @returns {Boolean} True (成功) / False (失敗)
 * @throws {xhr error}
 */
function createPNarc(src_nid, dst_nid) {

	$.ajax({
		url: '/node-edit/pnarc-create',
		type: 'post',
		dataType: 'json',
		data: {
			src_nid: src_nid,
			dst_nid: dst_nid
		},
		
		success: function(result) {
			if (result.success == true) {
				cy.nodes().forEach(node => {
					node.lock();
				});
				cy.edges().forEach(edge => {
					edge.lock();
				});

				cy.add([
					{
						group: 'edges',
						data: {
							source: src_nid,
							target: dst_nid,
							edgetype: result.data.edge_kind,
							ownNode: "true",
						},
					}
				]);

				const layout = cy.makeLayout(layoutConfig);
				layout.run();

				cy.edges().forEach(edge => {
					edge.unlock();
				});
				cy.nodes().forEach(node => {
					node.unlock();
				});
				alert('指定された接続を作成しました。');
			} else {
				alert('指定された接続は作成できませんでした。');
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = '指定された接続の作成に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});
}

/**
 * PNarc削除
 * ・指定されたSourceとDestinationを使いPNarcを削除する。
 * ・作成結果を元に画面を制御する。
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @returns {Boolean} True (成功) / False (失敗)
 * @throws {xhr error}
 */
function deletePNarc(src_nid, dst_nid) {

	$.ajax({
		url: '/node-edit/pnarc-delete',
		type: 'post',
		dataType: 'json',
		data: {
			src_nid: src_nid,
			dst_nid: dst_nid
		},
		success: function(result) {
			if (result.success == true) {
				cy.nodes().forEach(node => {
					node.lock();
				});
				cy.edges().forEach(edge => {
					edge.lock();
				});

				cy.edges(`[source = "${src_nid}"][target = "${dst_nid}"]`).remove();

				cy.edges().forEach(edge => {
					edge.unlock();
				});
				cy.nodes().forEach(node => {
					node.unlock();
				});
				alert('指定された接続を削除しました。');
			} else {
				alert('指定された接続は削除できませんでした。');
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = '指定された接続の削除に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});
}

/**
 * ノード追加
 * ・指定されたNodeID、Id、Typeで新たなノードを作成する。
 * ・作成結果を元に画面を制御する。
 * @param {number} nid - Node id
 * @param {number} id - Place or transition  id
 * @param {string} type - Node type
 * @returns {Boolean} True (成功) / False (失敗)
 * @throws {xhr error}
 */
function createNode(nid, id, kind) {

	$.ajax({
		url: '/node-edit/node-creation',
		type: 'post',
		dataType: 'json',
		data: {
			nid: nid,
			id: id,
			kind: kind
		},
		success: function(result) {
			if (result.success == true) {
				loadPetrinet();
				alert('新たなノードを追加しました。' + '[' + result.data.nid + ']');
			} else {
				alert('指定されたノードは追加できませんでした。');
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = '新たなノードの作成に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});
}

/**
 * XMAIL エクスポート
 * ・指定されたNodeID、出力ファイル名から新たなノードを作成する。
 * ・作成結果を元に画面を制御する。
 * @param {string} nid - Node id
 * @param {string} infile - existing original XMAIL
 * @param {string} outfile - exported XMAIL.
 * @returns {Boolean} True (成功)
 * @throws {xhr error}
 */
function exportXMAIL(nid, infile, outfile) {

	$.ajax({
		url: '/node-edit/export',
		type: 'post',
		dataType: 'json',
		data: {
			nid: nid,
			infile: infile,
			outfile: outfile
		},
		success: function(data) {
			if (data != false) {
				alert('MaiMLファイルにエクスポートしました。');
				window.open(data, '_blank');
			} else {
				alert('MaiMLのエクスポートに失敗しました。');
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'MaiMLのエクスポートに失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});
}