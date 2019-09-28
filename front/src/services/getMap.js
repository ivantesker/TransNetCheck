
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

        var searchFromSity = new ymaps.control.SearchControl({
            options: {
                kind: 'locality',
                position: {
                    left: "15px",
                    top: "10px"
                }
            }
        });

        myMap.controls.add(searchFromSity);

        var searchToSity = new ymaps.control.SearchControl({

            options: {
                kind: 'locality',
                position: {
                    left: "15px",
                    top: "40px"
                }
            }
        });

        myMap.controls.add(searchToSity);

    });
}