<template>
  <div class="change_location">
    <div id="geocoder"></div>
  </div>
</template>

<script>
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
#geocoder, .mapboxgl-ctrl-geocoder, .mapboxgl-ctrl-geocoder--input {
  width: 100% !important;
}
</style>
