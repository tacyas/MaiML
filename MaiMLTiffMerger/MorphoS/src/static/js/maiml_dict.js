// html div className --> maiml_style.css
const divclass = 'divclass'
const div1class = 'div1class'  
const div2class = 'div2class'  //method,results,log階層
const div3class = 'div3class'  //instance,trace
const div4class = 'div4class'  //event,property,content
const div5class = 'div5class'  //property,content
const div6class = 'div6class'  //property,content
const pclass = 'pclass'
const spanclass = 'spanclass'
labelclass = 'labelclass'

const valueEscape = function (str) {
    //return str
    return str.replace(/\"/g, '&quot;');

    //        .replace(/\'/g, "\\'")
    //        .replace(/\"/g, '\\"')
    //        .replace(/\//g, '\\/');
};

//////////////////////////////////////////////////////////////////////////////////////////////
//  form内の汎用データコンテナをhtmlタグに変換
////////////////////////////////////////////
function generalpurposedata(div3, elementname, globaluuid, properties_json, hierarchy, y=''){
    var properties_keyList = Object.keys(properties_json)  //properties_keyList=0/1/2/3/4
    var classname = 'div'+ hierarchy + 'class'
    for (let k4s in properties_keyList){ // k4s=0,1,2,3,4
        const details1 = document.createElement('details')
        details1.setAttribute('open','')
        details1.className = classname
        const summary1 = document.createElement('summary')
        summary1.innerHTML = elementname
        details1.appendChild(summary1)
        
        //divタグを生成
        var div4 = document.createElement('div');
        div4.id = elementname+k4s+'_id'
        div4.className = classname
        var property_json = properties_json[k4s];   // property_json = {'key':'','xsi:type':'','value':'','property':{}} : propertied_json[0/1/2/3/4]
        if (property_json !== null && property_json !== undefined){
            var property_keyList = Object.keys(property_json)  // property_keyList=['@key','@xsi:type','value','property']
            for (let k4 in property_keyList){  //一つ目のpropertyのコンテンツ分のループ  // k4='@key'/'@xsi:type'/'value'/'property'
                if(!y){
                    w = elementname.substr(0,1) + k4s
                }else{
                    w = y + elementname.substr(0,1) + k4s + ""
                }
                if (Object.prototype.toString.call(property_json[property_keyList[k4]])  === "[object Array]" || Object.prototype.toString.call(property_json[property_keyList[k4]])  === "[object Object]") { 
                    var n_properties_json = property_json[property_keyList[k4]];   //>=1
                    div4 = generalpurposedata(div4, property_keyList[k4], globaluuid, n_properties_json, hierarchy+1, w)
                } else {
                    var htmlID = property_keyList[k4] + w + globaluuid
                    var p4 = {}
                    if(property_keyList[k4].substring(0,1) === "@"){
                        p4 = document.createElement('p');
                    }else{
                        p4 = document.createElement('p');
                    }
                    if (!property_json[property_keyList[k4]]){
                        p4.innerHTML = `<label class="${labelclass}">${property_keyList[k4]}:</label><input type="text" id="${htmlID}" value="""" />`
                    }else{
                        p4.innerHTML = `<label class="${labelclass}">${property_keyList[k4]}:</label><input type="text" id="${htmlID}" value="${valueEscape(property_json[property_keyList[k4]])}" />`
                    }
                    div4.appendChild(p4)
                }
            }
        }
        details1.appendChild(div4)
        div3.appendChild(details1)
    }
    return div3
}
////////////////////////////////////////////////////////////////////////////////////////////////////

/////[form data --> input data]/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
window.onload = function getFormValues() {
    var form = document.getElementById('id_maiml_dict')
    var maiml = JSON.parse(form.value)

    // create input data erea
    // document========================================================================================================================
    var document_json = maiml.maiml.document;
    var documentvalue = document.getElementById('documentvalue');
    documentvalue.textContent = JSON.stringify(document_json);
    //end document========================================================================================================================
    
    // protocol========================================================================================================================
    var protocol_json = maiml.maiml.protocol;
    var protocolvalue = document.getElementById('protocolvalue');
    protocolvalue.textContent = JSON.stringify(protocol_json);
    // end protocol========================================================================================================================

    // data========================================================================================================================
    var data_json = maiml.maiml.data;
    var datavalue = document.getElementById('datavalue');

    // data->results->material/condition/result->property
    const data_keyList = Object.keys(data_json)
    for (let k1 in data_keyList){
        if (Object.prototype.toString.call(data_json[data_keyList[k1]])  === "[object Array]" || Object.prototype.toString.call(data_json[data_keyList[k1]])  === "[object Object]") { 
            const details1 = document.createElement('details')
            details1.setAttribute('open','')
            details1.className = div2class
            const summary1 = document.createElement('summary')
            summary1.innerHTML = data_keyList[k1]  //要素名:data要素直下の要素名（results）
            details1.appendChild(summary1)
            //孫をもつdivタグを生成
            const div2 = document.createElement('div');
            div2.id = data_keyList[k1]+'_id'
            div2.className = div2class
            //div2.innerHTML = data_keyList[k1]  //要素名:data要素直下の要素名（results）
            const results_json = data_json[data_keyList[k1]];   //results は{}
            const results_keyList = Object.keys(results_json)  //results_jsonのkeyを全て取得（results直下の要素名のリスト:material,condition,result）
            for (let k2 in results_keyList){ //resultsが持つキーの数分ループ
                if (Object.prototype.toString.call(results_json[results_keyList[k2]])  === "[object Array]" || Object.prototype.toString.call(results_json[results_keyList[k2]])  === "[object Object]") {  //１以上の要素の場合
                    //次の階層のコンテンツ(material,condition,result)
                    //results_jsonの一つのキーに対する値がオブジェクト（つまり複数データ）の場合の処理 データ例：material:[{'@id':"",property:{}},{'@id':"",}]
                    const instances_json = results_json[results_keyList[k2]];  //instances_json=[{},{}] : (results_json['material'/'condition'/'result'])
                    const instances_keyList = Object.keys(instances_json)    // instances_keyList=0,1,2,3,4,
                    for (let k3s in instances_keyList){  //listから一つずつ(0,1,2,3)
                        const details2 = document.createElement('details')
                        details2.setAttribute('open','')
                        details2.className = div3class
                        const summary2 = document.createElement('summary')
                        summary2.innerHTML = results_keyList[k2]  //instanceの要素名
                        details2.appendChild(summary2)
                        //divタグを生成
                        var div3 = document.createElement('div');
                        div3.id = results_keyList[k2]+k3s+'_id'
                        div3.className = div3class
                        //div3.innerHTML = results_keyList[k2]  //instanceの要素名
                        const instance_json = instances_json[instances_keyList[k3s]];    // instance_json={'@id':"",'uuid':'','name':',property:[{}]}  : results_json["material"][0/1/2/3]
                        const instance_keyList = Object.keys(instance_json)   // instance_keyList=['@id','uuid','name','property']
                        const globaluuid = instance_json['uuid']  // globaluuid=material-uuid/condition-uuid/result-uuid
                        for (let k3 in instance_keyList){
                            if (Object.prototype.toString.call(instance_json[instance_keyList[k3]])  === "[object Array]" || Object.prototype.toString.call(instance_json[instance_keyList[k3]])  === "[object Object]") { 
                                insertion_json = instance_json[instance_keyList[k3]]
                                if (instance_keyList[k3] == 'insertion' ){
                                    const hierarchy = 4
                                    var insertion_keyList = Object.keys(insertion_json) 
                                    //var insertion_keyList = Object.keys(instance_json[instance_keyList[k3]])
                                    var classname = 'div' + hierarchy + 'class'
                                    const details3 = document.createElement('details')
                                    details3.setAttribute('open', '')
                                    details3.className = classname
                                    const summary3 = document.createElement('summary')
                                    summary3.innerHTML = instance_keyList[k3]
                                    details3.appendChild(summary3)
                                    var div4 = document.createElement('div');
                                    div4.id = instance_keyList[k3] + k3 + '_id'
                                    div4.className = classname
                                    for (let k4s in insertion_keyList) { // k4s=0,1,2,3,4
                                        //uri,hash=1
                                        //uuid,format=0,1
                                        p4 = document.createElement('p')
                                        if (!insertion_json[insertion_keyList[k4s]]) {
                                            p4.innerHTML = `<label class="${labelclass}">${insertion_keyList[k4s]}:</label><input type="text" id="${htmlID}" value="""" />`
                                        } else {
                                            p4.innerHTML = `<label class="${labelclass}">${insertion_keyList[k4s]}:</label><input type="text" id="${htmlID}" value="${valueEscape(insertion_json[insertion_keyList[k4s]])}" />`
                                        }
                                        div4.appendChild(p4)
                                    }
                                    details3.appendChild(div4)
                                    div3.appendChild(details3)
                                }else{
                                    //一つ目のproperty  再帰関数スタート
                                    const properties_json = instance_json[instance_keyList[k3]];   // instance_keyList[k3]='property'or'content'  properties_json=[{'key':'','xsi:type':'','value':''},{'key':'','xsi:type':'','value':''}]
                                    const hierarchy = 4
                                    div3 = generalpurposedata(div3, instance_keyList[k3], globaluuid, properties_json, hierarchy)
                                }
                            } else {  // '@id','uuid','name'...  : material/condition/resultの単一コンテンツ
                                var htmlID = instance_keyList[k3] + globaluuid
                                var p3 = {}
                                if(instance_keyList[k3].substring(0,1) === "@"){  // attribute
                                    p3 = document.createElement('p');
                                }else{  // child-element
                                    p3 = document.createElement('p');
                                }
                                p3.innerHTML = `<label class="${labelclass}">${instance_keyList[k3]}:</label><input type="text" id="${htmlID}" value="${valueEscape(instance_json[instance_keyList[k3]])}" />`
                                div3.appendChild(p3)
                            }
                        }
                        details2.appendChild(div3)
                        div2.appendChild(details2)
                    }
                } else {
                    var htmlID = results_keyList[k2] + results_json['uuid']
                    var p2 = {}
                    if(results_keyList[k2].substring(0,1) === "@"){
                        p2 = document.createElement('p');
                    }else{
                        p2 = document.createElement('p');
                    }
                    p2.innerHTML = `<label class="${labelclass}">${results_keyList[k2]}:</label><input type="text" id="${htmlID}" value="${valueEscape(results_json[results_keyList[k2]])}" />`
                    div2.appendChild(p2)
                }
            }
            details1.appendChild(div2)
            datavalue.appendChild(details1)
        } else { 
            var htmlID = data_keyList[k1] + data_json['uuid']
            var p1 = {}
            if(data_keyList[k1].substring(0,1) === "@"){
                p1 = document.createElement('p');
            }else{
                p1 = document.createElement('p');
            }
            p1.innerHTML = `<label class="${labelclass}">${data_keyList[k1]}:</label><input type="text" id="${htmlID}" value="${data_json[data_keyList[k1]]}" />`
            datavalue.appendChild(p1)
        }
    }
    // end data========================================================================================================================


    //eventLog========================================================================================================================
    var eventLog_json = maiml.maiml.eventLog;
    var eventLogvalue = document.getElementById('eventLogvalue'); //div要素を取得
    const eventlog_keyList = Object.keys(eventLog_json)
    for (let k1 in eventlog_keyList){
        if (Object.prototype.toString.call(eventLog_json[eventlog_keyList[k1]]) === "[object Array]" || Object.prototype.toString.call(eventLog_json[eventlog_keyList[k1]]) === "[object Object]") {  //１以上の要素の場合
            const details1 = document.createElement('details')
            details1.setAttribute('open','')
            details1.className = div2class
            const summary1 = document.createElement('summary')
            summary1.innerHTML = eventlog_keyList[k1]  //log
            details1.appendChild(summary1)
            //孫をもつdivタグを生成
            const div2 = document.createElement('div');
            div2.id = eventlog_keyList[k1] + '_id'
            div2.className = div2class
            const log_json = eventLog_json[eventlog_keyList[k1]][0];  //eventLog はlist[]
            const log_keyList = Object.keys(log_json)
            for (let k2 in log_keyList) {
                if (Object.prototype.toString.call(log_json[log_keyList[k2]]) === "[object Array]" || Object.prototype.toString.call(log_json[log_keyList[k2]]) === "[object Object]") {  //１以上の要素の場合
                    const details2 = document.createElement('details')
                    details2.setAttribute('open','')
                    details2.className = div3class
                    const summary2 = document.createElement('summary')
                    summary2.innerHTML = log_keyList[k2]  //trace
                    details2.appendChild(summary2)
                    //divタグを生成
                    const div3 = document.createElement('div');
                    div3.id = log_keyList[k2] + '_id'
                    div3.className = div3class
                    //div3.innerHTML = log_keyList[k2]
                    const trace_json = log_json[log_keyList[k2]][0];  // 今回は1つ指定
                    const trace_keyList = Object.keys(trace_json)
                    for (let k3 in trace_keyList) {
                        if (Object.prototype.toString.call(trace_json[trace_keyList[k3]]) === "[object Array]" || Object.prototype.toString.call(trace_json[trace_keyList[k3]]) === "[object Object]") {  //１以上の要素の場合
                            //event_jsonの数分ループ
                            const events_json = trace_json[trace_keyList[k3]];   //>=1
                            const events_keyList = Object.keys(events_json)
                            for (let k4s in events_keyList) {
                                const details3 = document.createElement('details')
                                details3.setAttribute('open','')
                                details3.className = div4class
                                const summary3 = document.createElement('summary')
                                summary3.innerHTML = trace_keyList[k3]  //event
                                details3.appendChild(summary3)
                                //divタグを生成
                                var div4 = document.createElement('div');
                                div4.id = trace_keyList[k3] + k4s + '_id'
                                div4.className = div4class
                                //div4.innerHTML = trace_keyList[k3]
                                const event_json = events_json[k4s];
                                const event_keyList = Object.keys(event_json)
                                globaluuid =event_json['uuid']
                                for (let k4 in event_keyList) {
                                    const properties_json = event_json[event_keyList[k4]];   //>=1
                                    if (Object.prototype.toString.call(properties_json) === "[object Array]" || Object.prototype.toString.call(properties_json) === "[object Object]") {  //１以上の要素の場合
                                        //event_jsonの数分ループ
                                        const hierarchy = 5
                                        div4 = generalpurposedata(div4, event_keyList[k4], globaluuid, properties_json, hierarchy)

                                    } else {
                                        var htmlID = event_keyList[k4] + k4s + globaluuid
                                        const p4 = document.createElement('p');
                                        p4.innerHTML = `${event_keyList[k4]}:<input type="text" id="${htmlID}" value="${properties_json}" />`
                                        div4.appendChild(p4)
                                    }
                                }
                                details3.appendChild(div4)
                                div3.appendChild(details3)
                            }
                        } else {
                            var htmlID = trace_keyList[k3] + trace_json['uuid']
                            const p3 = document.createElement('p');
                            p3.innerHTML = `${trace_keyList[k3]}:<input type="text" id="${htmlID}" value="${trace_json[trace_keyList[k3]]}" />`
                            div3.appendChild(p3)
                        }
                    }
                    details2.appendChild(div3)
                    div2.appendChild(details2)
                } else { 
                    var htmlID = log_keyList[k2] + log_json['uuid']
                    const p2 = document.createElement('p');
                    p2.innerHTML = `${log_keyList[k2]}:<input type="text" id="${htmlID}" value="${log_json[log_keyList[k2]]}" />`
                    div2.appendChild(p2)
                }
            }
            details1.appendChild(div2)
            eventLogvalue.appendChild(details1)
        } else {
            // htmlタグを生成
            var htmlID = eventlog_keyList[k1] + eventLog_json['uuid']
            const p1 = document.createElement('p');
            p1.innerHTML = `${eventlog_keyList[k1]}:<input type="text" id="${htmlID}" value="${eventLog_json[eventlog_keyList[k1]]}" />`
            // 生成したタグをdiv id="eventLogvalue" の子要素に追加
            eventLogvalue.appendChild(p1)
        }
    }
    //end eventLog========================================================================================================================
    
};
/////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////
// 汎用データコンテナの入力値からformデータへ変換
//////////////////////////////////////////////////
function regeneralpurposedata(instance_json, elementname, globaluuid, properties_json, hierarchy, y=''){
    var properties_keyList = Object.keys(properties_json)  //properties_keyList=0/1/2/3/4
    for (let k4s in properties_keyList){ // k4s=0,1,2,3,4
        const property_json = properties_json[k4s];   // property_json = {'key':'','xsi:type':'','value':'','property':{}} : propertied_json[0/1/2/3/4]
        if (property_json !== null && property_json !== undefined) {
            const property_keyList = Object.keys(property_json)   // property_keyList=['@key','@xsi:type','value','htmlID','property']
            for (let k4 in property_keyList){  //一つ目のpropertyのコンテンツ分のループ // k4='@key'/'@xsi:type'/'value'/'property'
                if(!y){
                    w = elementname.substr(0,1) + k4s
                }else{
                    w = y + elementname.substr(0,1) + k4s + ""
                }
                if (Object.prototype.toString.call(property_json[property_keyList[k4]])  === "[object Array]" || Object.prototype.toString.call(property_json[property_keyList[k4]])  === "[object Object]") { 
                    property_json[property_keyList[k4]] = regeneralpurposedata(instance_json, property_keyList[k4], globaluuid, property_json[property_keyList[k4]], hierarchy+1, w)

                } else { // '@key','@xsi:type','value','htmlID'
                    var htmlID = property_keyList[k4] + w + globaluuid
                    property_json[property_keyList[k4]] = document.getElementById(htmlID).value  
                }
            }
        }
    }
    return properties_json
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////

////[input date --> form data]/////////////////////////////////////////////////////////////////////////////////////////////////////
function setFormValues() {
    var form = document.getElementById('id_maiml_dict')
    const maiml = JSON.parse(form.value)

    // data========================================================================================================================
    var data_json = maiml.maiml.data; // data要素の元データ

    const data_keyList = Object.keys(data_json)
    for (let k1 in data_keyList){
        if (Object.prototype.toString.call(data_json[data_keyList[k1]])  === "[object Array]" || Object.prototype.toString.call(data_json[data_keyList[k1]])  === "[object Object]") { 

            const results_json = data_json[data_keyList[k1]];   //results は{}
            const results_keyList = Object.keys(results_json)  //results_jsonのkeyを全て取得（results直下の要素名のリスト:@id,uuid,name,description,material,condition,result,,,）
            for (let k2 in results_keyList){ //resultsが持つキーの数分ループ
                if (Object.prototype.toString.call(results_json[results_keyList[k2]])  === "[object Array]" || Object.prototype.toString.call(results_json[results_keyList[k2]])  === "[object Object]") {  //１以上の要素の場合
                    //次の階層のコンテンツ(results下のリスト構造の要素：material,condition,result)
                    //データ例：{material:[{'@id':"",'uuid':"",property:{}},{'@id':"",}]},{condition:[{'@id':"",'uuid':"",property:[{}{}]},{'@id':"",}]}
                    const instances_json = results_json[results_keyList[k2]];  //material:[{'@id':"",property:{}},{'@id':"",}]
                    const instances_keyList = Object.keys(instances_json)   // 0,1,2,3....
                    for (let k3s in instances_keyList){ 
                        const instance_json = instances_json[instances_keyList[k3s]];   //instance_json={'@id':"",property:{}},{'@id':"",} : material[0]
                        const instance_keyList = Object.keys(instance_json)  // instance_keyList=['@id','uuid','property'....]
                        for (let k3 in instance_keyList){
                            var properties_json = instance_json[instance_keyList[k3]];   // properties_json=[{},{},{}] : material['property']
                            if (Object.prototype.toString.call(properties_json)  === "[object Array]" || Object.prototype.toString.call(properties_json)  === "[object Object]") { 
                                const hierarchy = 4
                                properties_json = regeneralpurposedata(instance_json, instance_keyList[k3], instance_json['uuid'], properties_json, hierarchy)
                            } else {  // instance_keyList[k3]:material-@id,uuid,name,.....
                                var htmlID = instance_keyList[k3]+instance_json['uuid']
                                properties_json = document.getElementById(htmlID).value
                            }
                        }
                    }
                } else { //（results下の単一データ要素：results-uuid,results-name,results-description,,,,）
                    var htmlID = results_keyList[k2] + results_json['uuid']
                    results_json[results_keyList[k2]] = document.getElementById(htmlID).value //変更後の値をformの持つjsonデータに格納
                }
            }
        } else {   //（data要素下の単一コンテンツ：data-uuid,@id,name,description,insertion,,,,）
            var htmlID = data_keyList[k1] + data_json['uuid']
            data_json[data_keyList[k1]] = document.getElementById(htmlID).value  //変更後の値をformの持つjsonデータに格納
        }
    }
    // end data========================================================================================================================

    // eventLog========================================================================================================================
    var eventLog_json = maiml.maiml.eventLog;
    var eventLogvalue = document.getElementById('eventLogvalue'); //div要素を取得

    // eventLog->log->trace->event->property
    const eventlog_keyList = Object.keys(eventLog_json)
    for (let k1 in eventlog_keyList) {
        if (Object.prototype.toString.call(eventLog_json[eventlog_keyList[k1]]) === "[object Array]" || Object.prototype.toString.call(eventLog_json[eventlog_keyList[k1]]) === "[object Object]") {  //１以上の要素の場合
            const log_json = eventLog_json[eventlog_keyList[k1]][0];  //eventLog はlist[]
            const log_keyList = Object.keys(log_json)
            for (let k2 in log_keyList) {
                if (Object.prototype.toString.call(log_json[log_keyList[k2]]) === "[object Array]" || Object.prototype.toString.call(log_json[log_keyList[k2]]) === "[object Object]") {  //１以上の要素の場合
                    const trace_json = log_json[log_keyList[k2]][0];
                    const trace_keyList = Object.keys(trace_json)
                    for (let k3 in trace_keyList) {
                        if (Object.prototype.toString.call(trace_json[trace_keyList[k3]]) === "[object Array]" || Object.prototype.toString.call(trace_json[trace_keyList[k3]]) === "[object Object]") {  //１以上の要素の場合
                            //event_jsonの数分ループ
                            const events_json = trace_json[trace_keyList[k3]];   //>=1
                            const events_keyList = Object.keys(events_json)
                            for (let k4s in events_keyList) {
                                const event_json = events_json[k4s];
                                const event_keyList = Object.keys(event_json)
                                for (let k4 in event_keyList) {
                                    var properties_json = event_json[event_keyList[k4]];   //>=1
                                    if (Object.prototype.toString.call(properties_json) === "[object Array]" || Object.prototype.toString.call(properties_json) === "[object Object]") {  //１以上の要素の場合
                                        const hierarchy = 5
                                        properties_json = regeneralpurposedata(event_json, event_keyList[k4], event_json['uuid'], properties_json, hierarchy)
                                    } else {
                                        properties_json = document.getElementById(event_keyList[k4] + k4s + event_json['uuid']).value  //変更後の値
                                    }
                                }
                            }
                        } else {
                            trace_json[trace_keyList[k3]] = document.getElementById(trace_keyList[k3] + trace_json['uuid']).value  //変更後の値
                        }
                    }
                } else {
                    log_json[log_keyList[k2]] = document.getElementById(log_keyList[k2] + log_json['uuid']).value  //変更後の値
                }
            }
        } else {
            eventLog_json[eventlog_keyList[k1]] = document.getElementById(eventlog_keyList[k1] + eventLog_json['uuid']).value  //変更後の値
        }
    }
    // end eventLog========================================================================================================================
    document.getElementById('id_maiml_dict').value = JSON.stringify(maiml)
};
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

$(function () {
    $('#maiml_update_btn').click(function () {
        // バリデーションチェックを実装
        setFormValues();
        $('#updateForm').submit();
    });
})