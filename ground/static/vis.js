function rand() { 
    return Math.random();
}

function dynamicGraph(div, apiEnd, updateTime, title) {
    let layout = {
        title: {
            text: title
        }
    };

    let data = [{
        x: [],
        y: [],
        mode: 'lines',
        line: {color: '#80CAF6'}
    }];

    Plotly.plot(div, data, layout);

    graph = {
        div : div,
        url : apiEnd,
        numPoints : 0, 
    };

    window.setInterval(updateGraph, updateTime, graph);

    return graph
    
}


//some api / serial data request "/getData"+cnt
async function getNewData(graph) {
    var res = await fetch(graph.url + graph.numPoints)
    var d   = await res.json()
            
    var data = []
    for (let i = 0; i<d.length; i++) {
        graph.numPoints += 1;
        data[i] = {x: d[i][0], y: d[i][1]};
    }

    return data;
}

var updateGraph = async function(graph) {
    var data = await getNewData(graph)

    data.forEach(point => {
        Plotly.extendTraces(graph.div, {y: [[point.y]], x: [[point.x]]}, [0])
    });
}

data = [["/api/accelX/", "accelX", "Acceleration X vs Time"],["/api/accelY/", "accelY", "Acceleration Y vs Time"],["/api/accelZ/", "accelZ", "Acceleration Z vs Time"]]
graphs = []

for (let i = 0; i<data.length; i++) {
    graphs[i] = dynamicGraph(data[i][1], data[i][0], 1000, data[i][2])
}
