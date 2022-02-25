function rand() { 
    return Math.random();
}
  
Plotly.plot('graph', [{
    x: [],
    y: [],
    mode: 'lines',
    line: {color: '#80CAF6'}
}]);

var cnt = 0;

//some api / serial data request
async function getNewData() {
    var res = await fetch("/getData"+cnt)
    var d   = await res.json()
            
    var data = []
    for (let i = 0; i<d.length; i++) {
        cnt += 1;
        data[i] = {x: d[i][0], y: d[i][1]};
    }

    return data;
}

var updateGraph = async function() {
    var data = await getNewData()

    data.forEach(point => {
        Plotly.extendTraces('graph', {y: [[point.y]], x: [[point.x]]}, [0])
    });
}


var intervalId = window.setInterval(updateGraph, 1000);