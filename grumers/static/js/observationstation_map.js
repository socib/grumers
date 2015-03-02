ObservationStationMap = {
    COLORPALETTE: ['rgb(254,240,217)', 'rgb(253,212,158)', 'rgb(253,187,132)', 'rgb(252,141,89)', 'rgb(227,74,51)', 'rgb(179,0,0)'],
    color_step: null,
    map: null,

    generate: function(container, data) {
        // Set max value:
        var max_value = data[0].count;
        ObservationStationMap.color_step = max_value / (ObservationStationMap.COLORPALETTE.length - 1);

        var map_options = {
            projection: new OpenLayers.Projection("EPSG:3857"),
            displayProjection: new OpenLayers.Projection("EPSG:4326")
        };
        var map = new OpenLayers.Map(container, map_options);
        ObservationStationMap.map = map;
        var osmLayer = new OpenLayers.Layer.OSM();
        var emodnetBathymetryLayer = new OpenLayers.Layer.WMS("EMODnet bathymetry",
            "http://ows.emodnet-bathymetry.eu/wms", {
                layers: 'emodnet:mean_atlas_land',
                format: 'image/png'
            }, {
                opacity: 0.3,
                singleTile: false,
                isBaseLayer: false,
                projection: 'EPSG:4326',
                units: 'degrees',
                buffer: 0,
                gutter: 0,
                transitionEffect: 'resize',
                displayOutsideMaxExtent: 'true',
                attribution: '<a href="http://www.emodnet-bathymetry.eu/">EMODnet Bathymetry</a>'
            });

        var style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
        //style.fillColor = 'red';
        style.fillColor = '${fillColor}';
        style.fillOpacity = 1;
        style.pointRadius = 5;
        style.pointRadius = 5;
        style.strokeColor = "#444";
        style.strokeWidth = 2;
        style.strokeOpacity = 0.8;
        style.strokeDashstyle = 'solid';

        var stationDefaultStyle = new OpenLayers.Style(style, {
            context: {
                fillColor: ObservationStationMap.fillColor
            }
        });
        var stationPointStyle = new OpenLayers.StyleMap({
            'default': stationDefaultStyle,
        });
        var stationsLayer = new OpenLayers.Layer.Vector("Stations", {
            styleMap: stationPointStyle,
            preFeatureInsert: function(feature) {
                feature.geometry.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
            }
        });
        map.addLayers([stationsLayer, osmLayer, emodnetBathymetryLayer]);
        ObservationStationMap.addDataToLayer(stationsLayer, data);
        map.zoomToExtent(stationsLayer.getDataExtent());

        var selectFeatureControl = new OpenLayers.Control.SelectFeature(stationsLayer, {
            multiple: false,
            onSelect: ObservationStationMap.onFeatureSelect,
            onUnselect: ObservationStationMap.onFeatureUnselect
        });
        map.addControl(selectFeatureControl);
        selectFeatureControl.activate();

    },
    fillColor: function(feature) {
        var position = Math.round(feature.attributes.count / ObservationStationMap.color_step);
        return ObservationStationMap.COLORPALETTE[position];
    },
    addDataToLayer: function(layer, data) {
        var points = [];
        for (var i = 0, l = data.length; i < l; i++) {
            var point = new OpenLayers.Feature.Vector(
                new OpenLayers.Geometry.Point(data[i].lng, data[i].lat)
            );
            point.attributes = data[i];
            points.push(point);
        }
        layer.addFeatures(points);
    },
    onFeatureSelect: function(feature) {
        var popup = new OpenLayers.Popup.FramedCloud("popup",
            feature.geometry.getBounds().getCenterLonLat(),
            null,
            ObservationStationMap.printPopUpContent(feature),
            null, true, ObservationStationMap.onPopupClose);
        feature.popup = popup;
        ObservationStationMap.map.addPopup(popup);
    },
    onFeatureUnselect: function(feature) {
        ObservationStationMap.map.removePopup(feature.popup);
        feature.popup.destroy();
        feature.popup = null;
    },
    printPopUpContent: function(feature) {
        return "<b>Route:</b>" + feature.attributes.route + " <br/>" +
            "<b>Station:</b> " + feature.attributes.station + "<br />" +
            "<b>Observations:</b> " + feature.attributes.count;
    },

};