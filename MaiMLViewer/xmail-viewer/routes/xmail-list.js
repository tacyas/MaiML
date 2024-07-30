'use strict';

/**
 * express module
 * @const
 */
const express = require('express');
const router = express.Router();
const util = require('util');
const xmail = require('../models/xmail.js');
const xmailedit = require('../models/xmail-edit.js');
var logger = require('../common/log-utils.js');

/**
 * ルートサービス  XMAIL一覧データ照会
 * @name get/
 * @function
 * @memberof module:routes/xmail-list
 * @inner
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.get('/', async (req, res, next) => {
	res.render('xmail-list', {    //'xmail-list.hbs'をテンプレートとしてレンダリングする
		title: 'MaiML-List'      //レンダリングで渡すデータ
	});

	return next;
});

/**
 * ルートサービス  XMAIL一覧データ取得
 * @name get/xmail-list
 * @function
 * @memberof module:routes/xmail-list
 * @inner
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.get('/xmail-list', async (req, res, next) => {    // '/xmail-list'パスにgetリクエストが来た時の処理
	xmail
		.list()
		.then(result => {
			logger.app.debug('[router-xmail-list-root]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');    // resultがJSONタイプ
			if (result === '[') {
				res.status(404);
			} else {
				res.status(200);
			}
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-xmail-list-root]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  XMAILデータアップロード
 * @name get/xmail-list
 * @function
 * @memberof module:routes/xmail-upload
 * @inner
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.post('/xmail-upload', async (req, res, next) => {    // '/xmail-list'パスにpostリクエストが来た時の処理
	logger.app.debug(
		'[xmail-list-upload] filename:' + util.inspect(req.body.filename)
	);
	logger.app.debug(
		'[xmail-list-upload] contents:' + util.inspect(req.body.xmail)
	);

	await xmailedit
		.upload(req.body.filename, req.body.xmail)
		.then(result => {
			logger.app.debug(
				'[router-xmail-list-upload]' + util.inspect(result)
			);

			res.setHeader('Content-Type', 'application/json');
			if (result == '[0]') {
				res.status(200);
			} else {
				res.status(500);
			}
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-xmail-list-upload]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  XMAILデータ削除
 * @name get/xmail-list
 * @function
 * @memberof module:routes/xmail-delete
 * @inner
 * @param {string} nid - Xmail ID
 * @param {callback} middleware - Express middleware.
 */
router.post('/xmail-delete', async (req, res, next) => {
	logger.app.debug('[xmail-list-delete] nid:' + util.inspect(req.body.nid));

	await xmailedit
		.delete(req.body.nid)
		.then(result => {
			logger.app.debug(
				'[router-xmail-list-delete]' + util.inspect(result)
			);

			res.setHeader('Content-Type', 'application/json');
			if (result == '[0]') {
				res.status(200);
			} else {
				res.status(500);
			}
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-xmail-list-delete]' + error.message);
			res.send(error.message);
		});

	return next;
});

module.exports = router;
