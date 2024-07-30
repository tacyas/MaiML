
/* テスト用データ */
var testdata = [
    // node(place,transition)
    {"data": {"id": "M1", "maiml_type": "M"},},
    {"data": {"id": "C1", "maiml_type": "C"},},
    {"data": {"id": "T1", "maiml_type": "T"},},
    {"data": {"id": "R1", "maiml_type": "R"},},
    // edge(arc)
    {"data": {"id": "E1", "source": "M1", "target": "T1", "nodeType":"transition", "label": "M1 - T1"}},
    {"data": {"id": "E2", "source": "C1", "target": "T1", "nodeType":"transition", "label": "C1 - T1"}},
    {"data": {"id": "E3", "source": "T1", "target": "R1", "nodeType":"transition", "label": "C - D"}},
]
// 座標を初期指定
var testdata2 = [
    // node(place,transition)
    {"data": {"id": "M1", "maiml_type": "M"}, position: { x: 100, y: 100 }},
    {"data": {"id": "C1", "maiml_type": "C"}, position: { x: 300, y: 100 }},
    {"data": {"id": "T1", "maiml_type": "T"}, position: { x: 100, y: 300 }},
    {"data": {"id": "R1", "maiml_type": "R"}, position: { x: 300, y: 300 }},
    // edge(arc)
    {"data": {"id": "E1", "source": "M1", "target": "T1", "nodeType":"transition", "label": "M1 - T1"}},
    {"data": {"id": "E2", "source": "C1", "target": "T1", "nodeType":"transition", "label": "C1 - T1"}},
    {"data": {"id": "E3", "source": "T1", "target": "R1", "nodeType":"transition", "label": "C - D"}},
]

/////////////////////////////////////////////////////////////////////////////////////
// draw petri-net graph
////////////////////////////////////////////////////////////////////////////////////
/* cytoscape用定数  */
var petridata
var cy
var layoutConfig = {name: 'preset'};
const layoutConfig_cola = {
    name: 'cola',
    animate: false,
    flow: { axis: 'x' },
};

var style = [
    {selector: 'node',
    css: {
        'label': 'data(id)',
        'color': 'black',
        'text-outline-color': 'white',
        'text-outline-width': 1,
        //'background-color': '#A1C65E',  //serisunawatisakau
        //'background-color': '#3B3939',  //sekireinaku
        'background-color': 'white',
        //'background-opacity': 0.5,
        //'border-color': 'black',
        'border-color':  '#676D70',
        'border-width': 0.5,
        'font-size': '3px'
    }},
    // material nodeに対するスタイル
    {selector: 'node[maiml_type="M"]',
        css: {
            //'background-color': 'blue',
            'shape': 'ellipse',
            //'width': 24,
            //'height': 24,
            'text-valign': 'center',
            'text-halign': 'center',
        }},
    // condition nodeに対するスタイル
    {selector: 'node[maiml_type="C"]', 
        css: {
            'shape': 'pentagon',
            'text-valign': 'center',
            'text-halign': 'center',
        }},
    // result nodeに対するスタイル
    {selector: 'node[maiml_type="R"]', 
        css: {
            'shape': 'rectangle', 
            'text-valign': 'center',
            'text-halign': 'center',
        }},
    // transition nodeに対するスタイル
    {selector: "node[maiml_type='T']", 
        css: {
            'shape': 'rectangle',
            'width': 6,
            'height': 40,
            'text-valign': 'bottom',
            'border-style' : 'solid',
            'border-color' : '#676D70',
            //'background-color': '#5FAB4F',  //serisunawatisakau
            'background-color': '#676D70',  //sekireinaku
    }},
    // edgeに対するスタイル
    {selector: 'edge',
        css: {
            'width': 1,
            'curve-style': 'bezier',
            //'line-color': '#5FAB4F',  //serisunawatisakau
            //'target-arrow-color': '#5FAB4F',  //serisunawatisakau
            'line-color': '#676D70',  //sekireinaku
            'target-arrow-color': '#676D70',  //sekireinaku
            'target-arrow-shape': 'triangle',
            'target-arrow-fill': 'filled',
            'arrow-scale': 0.6,
            'label': 'data(label)',
            'font-size': '10px'
    }},
];

// 座標記録
function addpositiontodata(){
    //console.log(petridata)
    var form = document.getElementById('id_petri_data')
    for (let i = 0; i < petridata.length; i++) {
        //console.log(petridata[i])
        if (petridata[i].data.hasOwnProperty('maiml_type')){
            petridata[i].position={
                'x': cy.getElementById(petridata[i].data.id)._private.position.x,
                'y': cy.getElementById(petridata[i].data.id)._private.position.y,
            };
        }
    }
    //console.log([petridata])
    document.getElementById('id_petri_data').value = JSON.stringify(petridata)
}

/* cytoscapeを使用した描画 */
window.onload = function drawpetrinetd() {
    // formからペトリネットの情報を取得する
    var form = document.getElementById('id_petri_data')
    petridata = JSON.parse(form.value)
    //console.log(petridata)

    // cytoscapeオブジェクトの初期化
    cy = cytoscape({
        container: document.getElementById('cy'),
        elements: petridata,
        style: style,
        layout: layoutConfig,
    });

    
    // 描画
    cy.ready(function () {
        var layout_out = layoutConfig_cola
        for(var i=0; i<petridata.length; i++){
            var keys = Object.keys(petridata[i])
            for(var j=0; j<keys.length; j++){
                if(keys[j] == 'position'){
                    layout_out = layoutConfig
                }
            }
        }
        //console.log(layout_out)
        const layout = cy.makeLayout(layout_out);
        layout.run();
    });
}


$(function () {
    $('#tiff_update_btn').click(function () {
        addpositiontodata();
        $('#fromidupload').submit();
    });
})
