'use strict';

const C_ERR_HEAD = '入力エラー：\n\n';

/*global $ formatErrorMessage */
/**
 * XMAIL一覧データ照会画面の初期処理
 * ・Datatablesの初期化
 * ・Datatablesのクリックイベントの定義
 * ・Datatablesデータ表示処理の呼び出し
 * @function
 */
$(document).ready(function() {
	// Setup the dnd listeners.
	var dropZone = document.getElementById('drop_zone');
	dropZone.addEventListener('dragover', handleDragOver, false);
	dropZone.addEventListener('drop', handleFileSelect, false);

	/* eslint-disable no-unused-vars */
	var table = $('#datagrid').DataTable({
		paging: false,
		searching: false,
		select: true,
		columns: [
			{
				className: 'dt-control',
				data: null,
				defaultContent: '',
			},
			{
				data: 'del_link',
				render: function(data) {
					return (
						'<button type="button" class="btn-xs btn-default" style="width:2.3rem;" onclick="actionDelete(' +
						data +
						');" >DEL</button>'
					);
				}
			},
			{
				data: 'nid',
				render: function(data) {
					return (
						'<button type="button" class="btn-xs btn-primary" style="width:3.2rem;" onclick="actionNid(' +
						data + 
						');" >' +
						data +
						'</button>'
					);
				}
			},
			{ data: 'xmail_uuid' },
			{ data: 'xmail_name' },
			{ data: 'xmail_description' },
			{ data: 'creators' },
			{ data: 'vendors' },
			{ data: 'owners' },
			{ data: 'linkages' },
			{ data: 'insertions' },
			{ data: 'file' },
		],
		columnDefs: [
			{
				targets: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
				//className: 'left-aligned-cell'
				className: 'dt-head-center',
			},
			{
				targets: [6, 7, 8, 9, 10, 11],
				visible: false
			},
			{ targets: [0, 1], orderable: false },
			{ targets: [0, 1, 2], width: 10 },
			{ targets: 3, width: 280 },
		],
		order: [[2, 'asc']]
	});

	loadGrid();

	/* Formatting function for row details - modify as you need */
	function format(d) {
		// `d` is the original data object for the row
		return (
			'<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
			'<tr>' +
				'<td>Creators</td>' +
				'<td>' + d.creators + '</td>' +
			'</tr>' +
			'<tr>' +
				'<td>Vendors</td>' +
				'<td>' + d.vendors + '</td>' +
			'</tr>' +
			'<tr>' +
				'<td>Owners</td>' +
				'<td>' + d.owners + '</td>' +
			'</tr>' +
			'<tr>' +
				'<td>Linkages</td>' +
				'<td>' + d.linkages + '</td>' +
			'</tr>' +
			'<tr>' +
				'<td>Insertions</td>' +
				'<td>' + d.insertions + '</td>' +
			'</tr>' +
			/*'<tr>' +
				'<td>Data source</td>' +
				'<td>' + d.file + '</td>' +
			'</tr>' +*/
			'</table>'
		);
	}

	// Add event listener for opening and closing details
    $('#datagrid tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

});

$('#uploadXmail').click(function() {
	$('#modalHead').html('MaiMLファイル登録');
	$('#modalData').html(
		'下記エリアにMaiMLファイルをドロップしてください。（1&nbsp;MaiMLファイル／1&nbsp;回）'
	);
	$('#filename').val('');
	document.getElementById('text_content').textContent = '';

	$('#myModal').modal('show');
});

/* eslint-disable no-unused-vars */
function actionDelete(nid) {
	var ret = confirm(
		'[NID] ' + nid + ' のMaiMLデータを削除します。\nよろしいですか？'
	);
	if (!ret) {
		return false;
	}
	deleteData(nid);
}

/* eslint-disable no-unused-vars */
function actionNid(nid) {
	//location.href = '/petrinet/view?id=' + nid + '&infile=' + $('#datagrid').DataTable().rows({selected: true}).data()[0]['file'];
	location.href = '/petrinet/view?id=' + nid;
}

$('#execImport').click(function() {
	// 何もデータがロードできていない場合はNG
	if (
		document.getElementById('filename').innerHTML == '' ||
		$('#text_content').val() == ''
	) {
		alert(C_ERR_HEAD + 'ファイルをアップロードしてから実行してください。');
		return false;
	}

	var ret = confirm('MaiMLデータを登録します。\nよろしいですか？');
	if (!ret) {
		return false;
	}

	uploadData($('#filename').val(), $('#text_content').val());
});

/**
 * ドロップされたファイルの処理
 * ・
 * @function
 * @param {evt} evt - イベント
 * @returns void
 */
function handleFileSelect(evt) {
	evt.stopPropagation();
	evt.preventDefault();

	var files = evt.dataTransfer.files;
	var file = '';

	if (files.length > 0) {
		//複数あった場合でも1件目のみを対象に処理
		file = files[0];

		//拡張子がxmail以外のファイルはNG
		var fileName = file.name;
		var xmailExt = fileName.substr(fileName.length - 5);
		var xmlExt = fileName.substr(fileName.length - 3);

		if (xmlExt !== 'xml' && xmailExt !== 'xmail'
			&& xmlExt !== 'mai' && xmailExt !== 'maiml') {
				alert(
				C_ERR_HEAD +
					'ファイル拡張子が"xml"又は、"mai"、"maiml"のデータを選択してください。'
			);
			return false;
		}

		// escape(f.name), file.type, file.size, file.lastModifiedDate.toLocaleDateString()
		var reader = new FileReader();
		// ファイルロード
		reader.onload = (function(file) {
			document.getElementById('filename').innerHTML = file.name;
			reader.readAsText(file);
		})(file);

		// ファイルコンテンツの読み込み
		reader.onloadend = function(evt) {
			if (evt.target.readyState == FileReader.DONE) {
				// DONE == 2
				document.getElementById('text_content').textContent =
					evt.target.result;
			}
		};
	} else {
		alert('エラー:ファイルの数が０');
	}
}

function handleDragOver(evt) {
	evt.stopPropagation();
	evt.preventDefault();
	evt.dataTransfer.dropEffect = 'copy';
}

/**
 * XMAIL一覧データ照会画面データのロード処理
 *
 * @function
 * @returns void
 * @throws {xhr error}
 */
function loadGrid() {
	$.ajax({
		url: '/xmail-list',
		type: 'GET',
		dataType: 'json',
		success: function(data) {
			$('#datagrid')
				.dataTable()
				.fnClearTable();
			if (data.length > 0) {
				$('#datagrid')
					.dataTable()
					.fnAddData(data);
			} else {
				alert('MaiMLデータは存在しません。');
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = '一覧取得に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
 * XMAILファイルアップロード処理
 *
 * @function
 * @param {filename} filename - XMAILファイル名
 * @param {xmail} xmail - XMAILデータ内容
 * @returns void
 * @throws {xhr error}
 */
function uploadData(filename, xmail) {
	$.ajax({
		url: '/xmail-upload',
		type: 'POST',
		dataType: 'json',
		data: {
			filename: filename,
			xmail: xmail
		},
		success: function() {
			loadGrid();
			alert('MaiMLデータのロードが完了しました。');
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'MaiMLデータのロードに失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}

/**
 * XMAILデータ削除
 *
 * @function
 * @param {nid} nid - XMAIL一意キー
 * @returns void
 * @throws {xhr error}
 */
function deleteData(nid) {
	$.ajax({
		url: '/xmail-delete',
		type: 'POST',
		dataType: 'json',
		data: {
			nid: nid
		},
		success: function() {
			loadGrid();
			alert('MaiMLデータの削除が完了しました。');
		},
		error: function(jqXHR, textStatus, errorThrown) {
			var msg = 'MaiMLデータの削除に失敗しました。';
			formatErrorMessage(jqXHR, textStatus, errorThrown, msg);
		}
	});

	return;
}
