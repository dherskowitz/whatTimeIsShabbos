<template>
  <div class="change_location">
    <div class="change_location__title">
      <span>Change Location</span>
      <span class="change_location__close" @click="$emit('close_location');">❌</span>
    </div>
    <div class="change_location__content">
      <p>Search By City</p>
      <places
        v-model="form.country.label"
        placeholder="Where are we going ?"
        @change="val => { form.country.data = val }"
        @keyup.enter="onSubmit"
        :options="options"
      ></places>
    </div>
  </div>
</template>

<script>
import Places from "vue-places";

export default {
  name: "ChangeLocation",
  components: {
    Places
  },
  data() {
    return {
      options: {
        // appId: <YOUR_PLACES_APP_ID>,
        // apiKey: <YOUR_PLACES_API_KEY>,
        // countries: ['US'],
        type: "city"
      },
      form: {
        country: {
          label: null,
          data: {}
        }
      }
    };
  },
  methods: {
    updateData(post_data) {
      let vm = this;
      fetch(
        "https://ymgbnproc2.execute-api.us-east-1.amazonaws.com/default/get_zmanim",
        {
          method: "POST",
          body: JSON.stringify(post_data)
        }
      )
        .then(response => response.json())
        .then(data => {
          let response_data = {
            city: data.ip_data.city,
            region: data.ip_data.region,
            country: data.ip_data.country,
            status: data.ip_data.status,
            candle_lighting: data.zman_data.items.filter(
              item => item.category == "candles"
            )[0],
            parsha: data.zman_data.items.filter(
              item => item.category == "parashat"
            )[0],
            havdalah: data.zman_data.items.filter(
              item => item.category == "havdalah"
            )[0]
          };
          vm.cache = {
            ...response_data,
            last_loaded: new Date()
          };
          vm.form.country.label = "";
          localStorage.setItem("zman_data", JSON.stringify(vm.cache));
          vm.$emit("update_data", response_data);
        });
    },
    onSubmit() {
      let vm = this;
      let place_data = this.form.country.data;
      let input = document.querySelector(".ap-input");
      if (input.value != "") {
        let post_data = {
          location: place_data.latlng,
          city: place_data.name,
          region: place_data.administrative,
          country: place_data.countryCode.toUpperCase()
        };
        vm.$emit("close_location");
        vm.$emit("updatingData");
        vm.updateData(post_data);
      }
    }
  }
};
</script>

<style>
.change_location {
  position: fixed;
  height: 100%;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9;
  background: #fff;
  transform: translateX(100vw);
  transition: transform 0.3s ease-in;
}
.change_location--open {
  transform: translateX(0);
}
.change_location__title {
  position: relative;
  background: rgba(1, 50, 67, 1);
  color: #fff;
  font-size: 2rem;
  padding: 0.5rem 0;
  text-align: center;
}
.change_location__content {
  padding: 1rem;
}
.change_location__close {
  position: absolute;
  right: 10px;
  top: 10px;
  cursor: pointer;
}
</style>
