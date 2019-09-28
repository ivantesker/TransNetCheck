
function GetMap(json) {
    ymaps.ready(function init() {
        var myMap = new ymaps.Map('map', {
            center: [55.733835, 37.588227],
            zoom: 11,
            controls: [
                "zoomControl"
            ]
        });
        var objectManager = new ymaps.ObjectManager();
        // Добавляем описание объектов в формате JSON в менеджер объектов.
        objectManager.add(json);
        // Добавляем объекты на карту.
        myMap.geoObjects.add(objectManager);

        myMap.controls.get('zoomControl').options.set('position', {
            bottom: "35vh",
            right: "15px"
        });
    });
}

var stDeparture = [
    "Эйс/Бэт-пес",
    "Эретик (Левиафан)",
    "Элемент Герл",
    "Эндрю Беннет",
    "Эквинокс",
    "Юга Хан",
    "Юошио Натсуми",
    "Ядовитый Плющ",
    "Ястреб и Голубь",
    "B’wana Beast",
    "Bat Lash",
    "Bernadeth",
    "Blackbriar Thorn",
    "Pow Wow Smith",
    "Machiste"];
var stArrival = [
    "Эйс/Бэт-пес",
    "Эретик (Левиафан)",
    "Элемент Герл",
    "Эндрю Беннет",
    "Эквинокс",
    "Юга Хан",
    "Юошио Натсуми",
    "Ядовитый Плющ",
    "Ястреб и Голубь",
    "B’wana Beast",
    "Bat Lash",
    "Bernadeth",
    "Blackbriar Thorn",
    "Pow Wow Smith",
    "Machiste"];
var trainFlight = [
    "Эйс/Бэт-пес",
    "Эретик (Левиафан)",
    "Элемент Герл",
    "Эндрю Беннет",
    "Эквинокс",
    "Юга Хан",
    "Юошио Натсуми",
    "Ядовитый Плющ",
    "Ястреб и Голубь",
    "B’wana Beast",
    "Bat Lash",
    "Bernadeth",
    "Blackbriar Thorn",
    "Pow Wow Smith",
    "Machiste"];

var find = function (arr, find) {
    return arr.filter(function (value) {
        return (value + "").toLowerCase().indexOf(find.toLowerCase()) != -1;
    });
};
function getDataProvider(arr) {
    return {
        suggest: function (request, options) {
            var res = find(arr, request),
                arrayResult = [],
                results = Math.min(options.results, res.length);
            for (var i = 0; i < results; i++) {
                arrayResult.push({ displayName: res[i], value: res[i] })
            }
            return ymaps.vow.resolve(arrayResult);
        }
    };
}

function getCustomSuggestions() {
    ymaps.ready(function init() {
        var suggestView1 = new ymaps.SuggestView('toCity', {
            results: 5
        });
        var suggestView2 = new ymaps.SuggestView('fromCity', {
            results: 5
        });
        var suggestView2 = new ymaps.SuggestView('stDeparture', {
            results: 5,
            provider: getDataProvider(stDeparture)
        });
        var suggestView3 = new ymaps.SuggestView('stArrival', {
            results: 5,
            provider: getDataProvider(stArrival)
        });
        var suggestView4 = new ymaps.SuggestView('trainFlight', {
            results: 5,
            provider: getDataProvider(trainFlight)
        });
    });
}