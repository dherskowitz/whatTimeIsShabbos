<template>
  <div class="change_location">
    <div id="geocoder"></div>
  </div>
</template>

<script>
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';

export default {
  name: "ChangeLocation",
  mounted: function() {
    const vm = this;
    const geocoder = new MapboxGeocoder({
      accessToken: process.env.GRIDSOME_MAPBOX_API_KEY,
      types: 'country,region,place,postcode,locality,neighborhood'
    });
    geocoder.addTo('#geocoder');
    geocoder.on('result', function (e) {
      console.log(e);
      console.log(e.result.place_name);

        let post_data = {
          location: {
            "lng": e.result.geometry.coordinates[0],
            "lat": e.result.geometry.coordinates[1]
          },
          city: e.result.place_name.split(',')[0].trim(),
          region: e.result.place_name.split(',')[1].trim(),
          country: e.result.place_name.split(',')[2].trim()
        };
        vm.$emit("close_location");
        vm.$emit("updateData", post_data);
    });
  }
};
</script>

<style>

.change_location {
  width: 25rem;
  height: 40px;
  max-width: 100%;
  display: flex;
  justify-content: center;
}
#geocoder, .mapboxgl-ctrl-geocoder {
  width: 100%;
}
</style>
