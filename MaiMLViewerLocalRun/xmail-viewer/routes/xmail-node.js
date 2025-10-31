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
 * ルートサービス  XMAILノードデータ一括取得
 * @name post/
 * @function
 * @memberof module:routes/xmail-node
 * @inner
 * @param {string} node - XMAIL自身のnode id
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.post('/', async (req, res, next) => {
	xmail
		.node_all(req.body.node_id)
		.then(result => {
			logger.app.debug('[router-node-root]' + util.inspect(result));

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
			logger.app.error('[router-node-root]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  XMAILノードデータリスト取得
 * @name post/node-list
 * @function
 * @memberof module:routes/xmail-node
 * @inner
 * @param {string} node_list - XMAIL内ノードのnode idのリスト
 * @param {callback} middleware - Express middleware.
 */
router.post('/node-list', async (req, res, next) => {
	xmail
		.node_list(JSON.parse(req.body.node_list))
		.then(result => {
			logger.app.debug('[router-node-list]' + util.inspect(result));

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
			logger.app.error('[router-node-list]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  ペトリネットノードデータ取得
 * @name post/node
 * @function
 * @memberof module:routes/xmail-node-material
 * @inner
 * @param {string} node - XMAIL内ノードのnode id
 * @param {string} path - Express path
 * @param {callback} middleware - Express middleware.
 */
router.post('/node-material', async (req, res, next) => {
	xmail
		.node_material(req.body.node_id)
		.then(result => {
			logger.app.debug('[router-node-material]' + util.inspect(result));

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
			logger.app.error('[router-node-material]' + error.message);
			res.send(error.message);
		});

	return next;
});

module.exports = router;
