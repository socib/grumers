JellyfishObservationMap = {
    COLORPALETTE: ['rgb(254,240,217)', 'rgb(253,212,158)', 'rgb(253,187,132)', 'rgb(252,141,89)', 'rgb(227,74,51)', 'rgb(179,0,0)'],
    color_step: null,
    map: null,

    generate: function(container, data) {
        // Set max value:
        var max_value = data[0].count;
        JellyfishObservationMap.color_step = max_value / (JellyfishObservationMap.COLORPALETTE.length - 1);

        var map_options = {
            projection: new OpenLayers.Projection("EPSG:3857"),
            displayProjection: new OpenLayers.Projection("EPSG:4326")
        };
        var map = new OpenLayers.Map(container, map_options);
        JellyfishObservationMap.map = map;
        var osmLayer = new OpenLayers.Layer.OSM();

        var style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
        style.fillColor = '${fillColor}';
        style.fillOpacity = 1;
        style.pointRadius = 5;

        var stationDefaultStyle = new OpenLayers.Style(style, {
            context: {
                fillColor: JellyfishObservationMap.fillColor
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
        map.addLayers([stationsLayer, osmLayer]);
        JellyfishObservationMap.addDataToLayer(stationsLayer, data);
        map.zoomToExtent(stationsLayer.getDataExtent());

        var selectFeatureControl = new OpenLayers.Control.SelectFeature(stationsLayer, {
            multiple: false,
            onSelect: JellyfishObservationMap.onFeatureSelect,
            onUnselect: JellyfishObservationMap.onFeatureUnselect
        });
        map.addControl(selectFeatureControl);
        selectFeatureControl.activate();

    },
    fillColor: function(feature) {
        var position = Math.round(feature.attributes.count / JellyfishObservationMap.color_step);
        return JellyfishObservationMap.COLORPALETTE[position];
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
            JellyfishObservationMap.printPopUpContent(feature),
            null, true, JellyfishObservationMap.onPopupClose);
        feature.popup = popup;
        JellyfishObservationMap.map.addPopup(popup);
    },
    onFeatureUnselect: function(feature) {
        JellyfishObservationMap.map.removePopup(feature.popup);
        feature.popup.destroy();
        feature.popup = null;
    },
    printPopUpContent: function(feature) {
        return "<b>Route:</b>" + feature.attributes.route + " <br/>" +
            "<b>Station:</b> " + feature.attributes.station + "<br />" +
            "<b>Observations:</b> " + feature.attributes.count;
    },

};


/*
        onLoadedLayers: function() {

            if(Drifter.Map.totalDeployments * 2 > Drifter.aLayers.length){
                return;
            }

            // Add feature control to display the popup
            Drifter.selectControl = new OpenLayers.Control.SelectFeature(Drifter.aLayers,
            {onSelect: Drifter.Map.onFeatureSelect, onUnselect: Drifter.Map.onFeatureUnselect});
            Drifter.map.addControl(Drifter.selectControl);
            Drifter.selectControl.activate();

            //var bounds = new OpenLayers.Bounds();
            //for (vectorBounds in vectorsBounds){
                //bounds.extend(vectorsBounds);
            //}

            //map.setCenter(bounds.getCenterLatLon());
            //map.zoomToExtent(vectorsBounds);

        },
        printPopUpContent: function(feature){
            // Getting the popup html content from the properties.html fearture
            return feature.data['html'];
        },
        onFeatureSelect: function(feature) {

            Drifter.selectedFeature = feature;
            popup = new OpenLayers.Popup.FramedCloud("chicken",
                                     feature.geometry.getBounds().getCenterLonLat(),
                                     null,
                                     Drifter.Map.printPopUpContent(feature),
                                     null, true, Drifter.Map.onPopupClose);
            feature.popup = popup;
            Drifter.map.addPopup(popup);
        },
        onPopupClose: function (evt) {
            Drifter.selectControl.unselect(Drifter.selectedFeature);
        },
        onFeatureUnselect: function(feature) {
            Drifter.map.removePopup(feature.popup);
            feature.popup.destroy();
            feature.popup = null;
        }
*/