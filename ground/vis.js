function rand() { 
    return Math.random();
}
  
Plotly.plot('graph', [{
    x: [1,2,3],
    y: [1,1,1],
    mode: 'lines',
    line: {color: '#80CAF6'}
}]);

var cnt = 0;
var t = 3;

//some api / serial data request
var getNewData = function() {
    //data in the form of
    //[{x:int,y:int},...]

    var m = rand()*3 //1-3
    var data = []

    for (let i = 0; i<m; i++) {
        data[i] = {x:rand(),y:rand()};
    }

    return data
}

var updateGraph = function() {
    var data = getNewData()

    data.forEach(point => {
        Plotly.extendTraces('graph', {y: [[point.y]], x: [[point.x]]}, [0])
    });
    if(cnt === 100) clearInterval(interval);
}


var intervalId = window.setInterval(updateGraph, 1000);