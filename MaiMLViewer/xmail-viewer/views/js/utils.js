'use strict';

/**
 * URLパラメータ取得
 * ・URLパラメータから指定されたキーに該当するデータを解析して取得する。
 * @param {string} name -パラメータのキー文字列
 * @param {url} url - 対象のURL文字列（任意）
 * @returns {string} - URLパラメータに対応する値
 */
function getParam(name, url) { // eslint-disable-line
	if (!url) {
		url = window.location.href;
	}

	name = name.replace(/[[]]/g, '\\$&');
	var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
	var results = regex.exec(url);
    
	if (!results) {
		return null;
	}

	if (!results[2]) {
		return '';
	}

	return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

/**
 * HttpXMLRequest（XHR) エラーハンドラー
 * XHRでエラーが発生した場合にその情報をもとに、エラーメッセージを生成して返却する。
 * @param {*} jqXHR
 * @param {*} textStatus
 * @param {*} errorThrown
 * @param {*} msg - XHRエラーメッセージ
 * @returns
 */
function formatErrorMessage(jqXHR, textStatus, errorThrown, msg) { // eslint-disable-line
	var stsMsg = jqXHR.responseText;
	var errMsg = '';

	errMsg = msg + '\n' +
            'Status ：' + jqXHR.status + '\n' +
			'Error  :' + errorThrown + '\n' +
			'Detail :' + stsMsg + '\n';
    
	alert(errMsg);
	return;
}
