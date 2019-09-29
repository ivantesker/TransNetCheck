var apiURL = 'https://stery.rtuitlab.ru';
// var apiURL = 'http://localhost';

ymaps.ready(init);

var myMap;

function init() {
    myMap = new ymaps.Map('map', {
        center: [55.76, 37.64],
        zoom: 10,
        controls: [
            "zoomControl"
        ]
    });
    myMap.controls.get('zoomControl').options.set('position', {
        bottom: "130px",
        right: "15px"
    });
}
function GetMap(json) {
    if (json == {}) {
        return;
    }
    var objectManager = new ymaps.ObjectManager();
    // Добавляем описание объектов в формате JSON в менеджер объектов.
    objectManager.add(json);
    // Добавляем объекты на карту.
    myMap.geoObjects.add(objectManager);
}

var find = function (arr, find) {
    return arr.filter(function (value) {
        return value.toString().toLowerCase().indexOf(find.toLowerCase()) != -1;
    });
};

function getCitiesSuggestions() {
    ymaps.ready(function init() {
        var suggestView1 = new ymaps.SuggestView('toCity', {
            results: 5
        });
        var suggestView2 = new ymaps.SuggestView('fromCity', {
            results: 5
        });
    });
}

flightRouteData = {
    arrayStArrival: [],
    arrayStDeparture: []
};

function getSuggestionsOfStDeparture(stDeparture) {
    ymaps.ready(function init() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                flightRouteData['arrayStDeparture'] = JSON.parse(xmlHttp.responseText);
            }
        }
        xmlHttp.open("GET", apiURL + `/stations?city="${stDeparture}"`, true);
        xmlHttp.send();

        var suggestView3 = new ymaps.SuggestView('stDeparture', {
            results: 7,
            provider: {
                suggest: function (request, options) {
                    var res = find(Object.keys(flightRouteData['arrayStDeparture']), request),
                        arrayResult = [],
                        results = Math.min(options.results, res.length);
                    for (var i = 0; i < results; i++) {
                        arrayResult.push({ displayName: res[i], value: res[i] })
                    }
                    return ymaps.vow.resolve(arrayResult);
                }
            }
        });
    });
}
function getSuggestionsOfStArrival(stArrival) {
    ymaps.ready(function init() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                flightRouteData['arrayStArrival'] = JSON.parse(xmlHttp.responseText)
            }
        }
        xmlHttp.open("GET", apiURL + `/stations?city="${stArrival}"`, true);
        xmlHttp.send();

        var suggestView4 = new ymaps.SuggestView('stArrival', {
            results: 7,
            provider: {
                suggest: function (request, options) {
                    var res = find(Object.keys(flightRouteData['arrayStArrival']), request),
                        arrayResult = [],
                        results = Math.min(options.results, res.length);
                    for (var i = 0; i < results; i++) {
                        arrayResult.push({ displayName: res[i], value: res[i] })
                    }
                    return ymaps.vow.resolve(arrayResult);
                }
            }
        });
    });
}
function getSuggestionsOfTrainFlight(trainFlightFrom, trainFlightTo) {
    ymaps.ready(function init() {
        var arr = [];

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                arr = JSON.parse(xmlHttp.responseText)
                console.log(arr);
            }
        }
        xmlHttp.open("POST", apiURL + `/routes?start_point=${trainFlightFrom}&end_point=${trainFlightTo}`, true);
        xmlHttp.send();

        var suggestView5 = new ymaps.SuggestView('trainFlight', {
            results: 5,
            provider: {
                suggest: function (request, options) {
                    var res = find(Object.values(arr), request),
                        arrayResult = [],
                        results = Math.min(options.results, res.length);
                    for (var i = 0; i < results; i++) {
                        arrayResult.push({ displayName: res[i], value: res[i] })
                    }
                    return ymaps.vow.resolve(arrayResult);
                }
            }
        });
    });
}

;
//# sourceMappingURL=scripts.js.map