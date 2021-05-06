<template>
  <Layout>
    <section class="home" :class="{ 'home--add-pad': show_location_form }">
      <h1 class="main_title">{{ $static.metadata.siteName }}</h1>
      <div class="notice" v-if="show_location_error">
        <p>We couldn't find your location so we are showing times for Jerusalem IL</p>
        <p>
          You can change your location by
          <button
            class="notice__button"
            @click="toggle_location_menu"
          >clicking here</button> or using the button below.
        </p>
      </div>
      <p class="text-lg" v-if="!show_location_error">{{location_msg}}</p>
      <span v-if="!loading">
        <p class="text-lg">This week is Shabbos {{parsha.title}}</p>
        <p class="text-lg">{{candle_lighting.title}} ({{time_before_lighting}}min)</p>
        <p class="text-lg">{{havdalah.title}}</p>
        <button class="change_location__button" v-bind:class="{ 'change_location__button--active': show_location_form }" @click="toggle_location_menu">Change Location<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clip-rule="evenodd"></path></svg></button>
      </span>
      <transition name="fadeIn" mode="out-in">
        <ChangeLocation
          v-if="show_location_form"
          ref="placesForm"
          v-on:updateData="get_zman_data"
          v-on:close_location="toggle_location_menu"
        />
      </transition>
    </section>
    <div v-if="show_toast" class="toast">
      <span>{{toast_message}}</span>
      <span @click="show_toast=!show_toast" class="toast__close"><svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg></span>
    </div>
    <div class="loader" v-if="loading">
      <span class="loader__spinner"></span>
    </div>
  </Layout>
</template>

<static-query>
query {
  metadata {
    siteName
  }
}
</static-query>

<script>
import ChangeLocation from "~/components/ChangeLocation.vue";

export default {
  components: {
    ChangeLocation
  },
  data() {
    return {
      location: "",
      location_msg: "",
      show_location_error: false,
      candle_lighting: {},
      time_before_lighting: "",
      parsha: {},
      havdalah: {},
      cache: {},
      formatted_date: "",
      loading: false,
      show_toast: false,
      toast_message: "",
      show_location_form: false
    };
  },
  methods: {
    focusOnPlaces() {
      this.$nextTick(() => {
        document.querySelector(".mapboxgl-ctrl-geocoder--input").focus();
      });
    },
    toggle_location_menu() {
      this.show_location_form = !this.show_location_form;
      this.show_location_form ? this.focusOnPlaces() : '';
      this.loading = false;
    },
    diff_hours() {
      let last_updated = new Date(
        JSON.parse(localStorage.getItem("zman_data")).last_loaded
      );
      let now = new Date();
      let diffTime = Math.abs(last_updated - now);
      let diffHours = (diffTime / (1000 * 60 * 60)).toFixed(2);
      return parseFloat(diffHours);
    },
    async get_zman_data(post_data) {
      let vm = this;
      let url = "https://ymgbnproc2.execute-api.us-east-1.amazonaws.com/default/get_zmanim";
      let response;
      if (post_data) {
        if (post_data.city == JSON.parse(localStorage.getItem("zman_data")).city) {
          vm.show_toast = true;
          vm.toast_message = `You already viewing the Zman for ${post_data.city}`;
          document.querySelector(".ap-input").value = "";
          setTimeout(() => {
            vm.show_toast = false;
          }, 5000);
          return false;
        }
        this.loading = true;
        let post_options = {
          method: "POST",
          body: JSON.stringify(post_data)
        };
        response = await fetch(url, post_options);
      } else {
        this.loading = true;
        response = await fetch(url);
      }
      let data = await response.json();

      // Set data with response
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
      vm.setData(response_data);

      // Cache response
      vm.cache = {
        ...response_data,
        last_loaded: new Date()
      };
      localStorage.setItem("zman_data", JSON.stringify(vm.cache));
    },
    update_location_msg(data) {
      let vm = this;
      if (data.status == "ip_error") {
        vm.show_location_error = true;
        vm.location_msg = "";
      } else if (data.status == "user_location") {
        vm.show_location_error = false;
        if (data.country == "US") {
          vm.location_msg = `Times for ${data.city}, ${data.region}`;
        } else {
          vm.location_msg = `Times for ${data.city}, ${data.country}`;
        }
      } else {
        vm.show_location_error = false;
        if (data.country == "US") {
          vm.location_msg = `It looks like you are in ${data.city}, ${data.region}`;
        } else {
          vm.location_msg = `It looks like you are in ${data.city}, ${data.country}`;
        }
      }
    },
    setData(data) {
      let vm = this;
      vm.candle_lighting = data.candle_lighting;
      vm.parsha = data.parsha;
      vm.havdalah = data.havdalah;
      vm.ip_error = data.status;

      // Format Date
      let date = new Date(data.candle_lighting.date);
      let options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
      };
      vm.formatted_date = new Intl.DateTimeFormat("en-US", options).format(
        date
      );

      // If user in US use city/state combo else city/country
      if (data.country == "US") {
        vm.location = `${data.city}, ${data.region}`;
      } else {
        vm.location = `${data.city}, ${data.country}`;
      }
      // If user in Jerusalem light 40min before else 18min before
      if (data.city == "Jerusalem") {
        vm.time_before_lighting = "40";
      } else {
        vm.time_before_lighting = "18";
      }
      vm.update_location_msg(data);
      vm.loading = false;
    }
  },
  created() {
    this.loading = true;
  },
  mounted: function() {
    let vm = this;
    if (localStorage.getItem("zman_data")) {
      let local_data = JSON.parse(localStorage.getItem("zman_data"));
      let time_elapsed = vm.diff_hours();
      vm.update_location_msg(local_data);

      console.log(time_elapsed);
      // Clear cache and fetch new data if more than 6 hours since last load
      if (time_elapsed > 6) {
        // localStorage.removeItem('zman_data');
        vm.get_zman_data();
        return;
      }
      // Set data from local storage
      vm.setData(local_data);
    } else {
      this.get_zman_data();
    }
  }
};
</script>

<style>
* + * {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
.home-links a {
  margin-right: 1rem;
}
.home {
  text-align: center;
  height: 100%;
  padding: 0 1rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  background-image: url(/images/bg.jpg);
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  transform: translatez(0);
  -webkit-transform: translatez(0);
}
.home--add-pad {
  padding-bottom: 2rem;
}
.home::before {
  content: "";
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: -1;
}
.home > p {
  margin: 0.5em;
}
.main_title {
  font-family: Permanent Marker, cursive;
  text-transform: capitalize;
  font-size: 4rem;
  color: rgba(1, 50, 67, 1);
  margin: 0;
  padding: 1rem 0;
}
.text-lg {
  font-size: 2rem;
  color: #fff;
  text-shadow: 1px 3px 4px #333;
}
.change_location__button {
  background: rgba(1, 50, 67, 1);
  border: none;
  color: #fff;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}
button.change_location__button svg {
  width: 1.2rem;
  margin-left: 0.5rem;
  transition: transform 0.25s ease-out;
}
.change_location__button.change_location__button--active {
  background: rgba(58, 83, 155, 1);
}
.change_location__button.change_location__button--active svg {
  transform: rotate(-180deg);
}
.notice {
  background: rgba(255, 148, 120, 0.5);
  max-width: 100%;
  width: 35em;
  border: 1px solid #333;
  border-radius: 5px;
  font-size: 1.25rem;
  padding: 0.5rem;
}
.notice__button {
  border: none;
  background: none;
  padding: 0;
  margin: 0;
  color: #fff;
  cursor: pointer;
  font-size: inherit;
}
.toast {
  position: absolute;
  bottom: 4rem;
  left: 50%;
  z-index: 9999;
  transform: translateX(-50%);
  background: rgba(42, 187, 155, 1);
  padding: 1rem;
  border-radius: 5px;
  box-shadow: 0px 4px 6px 0px rgba(36, 37, 42, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem;
}
.toast__close {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 0 0 0.5rem;
  cursor: pointer;
}
.toast__close svg {
  width: 1.5rem;
}
.fadeIn-enter-active,
.fadeIn-leave-active {
  transition: opacity 0.25s ease-out;
}
.fadeIn-enter,
.fadeIn-leave-to {
  opacity: 0;
  /* pointer-events: none; */
}
.loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 999;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.loader__spinner,
.loader__spinner:after {
  border-radius: 50%;
  width: 10em;
  height: 10em;
}
.loader__spinner {
  margin: 60px auto;
  font-size: 10px;
  position: relative;
  text-indent: -9999em;
  border-top: 1.1em solid rgba(0, 0, 0, 0.2);
  border-right: 1.1em solid rgba(0, 0, 0, 0.2);
  border-bottom: 1.1em solid rgba(0, 0, 0, 0.2);
  border-left: 1.1em solid #000000;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation: load8 1.1s infinite linear;
  animation: load8 1.1s infinite linear;
}
@-webkit-keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@media (max-width: 768px) {
  .main_title {
    font-size: 3rem;
  }
  .text-lg {
    font-size: 1.25rem;
  }
  .toast {
    left: 0;
    transform: translateX(0);
    bottom: 1rem;
  }
}
@media (max-height: 830px) {
  .ap-dropdown-menu {
    top: -310px !important;
  }
}
</style>
