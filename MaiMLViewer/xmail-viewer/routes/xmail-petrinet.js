'use strict';

/**
 * express module
 * @const
 */
const express = require('express');
const util = require('util');
const xmail = require('../models/xmail.js');
const router = express.Router();
var logger = require('../common/log-utils.js');

/**
 * ルートサービス  XMAILペトリネット図照会画面の描画
 * @name get/view
 * @function
 * @memberof module:routes/xmail-petrinet
 * @inner
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.get('/view', async (req, res, next) => {
	res.render('xmail-petrinet', {
		title: 'MaiML-Petrinet'
	});

	return next;
});

/**
 * ルートサービス  XMAILペトリネット図データ取得（node及びedge）
 * @name get/view
 * @function
 * @memberof module:routes/xmail-petrinet
 * @inner
 * @param {string} node - XMAIL自身のnode id
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.post('/xmail-petrinet', async (req, res, next) => {
	logger.app.debug('[router-petrinet] param:' + util.inspect(req.body.id));
	//nodes & edges
	await xmail
		.pn_nodes(req.body.id)
		.then(result => {
			logger.app.debug('[router-petrinet]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			if (result === '[') {
				res.status(404);
			} else {
				res.status(200);
			}
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-petrinet]' + error.message);
			res.send(error.message);
		});

	return next;
});


// 20240912 add
/**
 * ルートサービス  XMAILペトリネット図の位置情報を保存
 * @name get/view
 * @function
 * @memberof module:routes/xmail-petrinet
 * @inner
 * @param {string} node - XMAIL自身のnode id
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.post('/xmail-position', async (req, res, next) => {
	logger.app.debug('[router-petrinet] param:' + util.inspect(req.body.nid) + util.inspect(req.body.pnml_data));
	//nodes & edges
	await xmail
		.pn_position(req.body.nid, req.body.pnml_data)
		.then(result => {
			logger.app.debug('[router-petrinet]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			if (result === '[') {
				res.status(404);
			} else {
				res.status(200);
			}
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-petrinet]' + error.message);
			res.send(error.message);
		});

	return next;
});

module.exports = router;
