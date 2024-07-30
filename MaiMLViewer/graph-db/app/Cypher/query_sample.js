const neo4j = require('neo4j-driver');

const uri = 'bolt://localhost:7687';
const user = '';
const password = '';

const cypher_api = require('./cypher_api.js');


////////////////


async function run_query(cypher, params = {}) {
	const driver = neo4j.driver(uri, neo4j.auth.basic(user, password))
	const session = driver.session()

	try {
		const result = await session.run({text: cypher, parameters: params})
		result.records.forEach(r => {
			console.log('== record')
			r.forEach(v => console.log(v))
			console.log('')
		})
		console.log('== summary')
		console.log(result.summary.counters._stats)
	} finally {
		await session.close()
	}

	await driver.close()
}

////////////////


console.log(JSON.stringify(cypher_api.query_list, null, 2));

//run_query(cypher_api.get_cypher('sample', 0, 'XMAIL'));
//run_query(cypher_api.get_cypher('get_xmail'));
//run_query(cypher_api.get_cypher('get_PN', 1765));
//run_query(cypher_api.get_cypher('get_template', 1893));
//run_query('match (a:XMAIL) where id(a)=0 return a;')
