<template>
  <div class="change_location">
    <places
      v-model="form.country.label"
      placeholder="What city are you in?"
      @change="val => onSubmit(val)"
      :options="options"
      @keyup.native.enter="onSubmit"
    ></places>
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
        type: "city",
        templates: {
            value: function (suggestion) {
              return `${suggestion.name}, ${suggestion.countryCode == 'us' ? suggestion.administrative : suggestion.country}`;
            }
        }
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
    onSubmit(place_data) {
      let vm = this;
      let input = document.querySelector(".ap-input");
      if (input.value != "") {
        let post_data = {
          location: place_data.latlng,
          city: place_data.name,
          region: place_data.administrative,
          country: place_data.countryCode.toUpperCase()
        };
        vm.$emit("close_location");
        vm.$emit("updateData", post_data);
      }
    }
  }
};
</script>

<style>
.change_location {
  width: 25rem;
  max-width: 100%;
  display: flex;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease-out;
}
.change_location--open {
  opacity: 1;
  pointer-events: all;
}
.change_location__content__form {
  display: flex;
  justify-content: center;
  align-items: center;
}
span.algolia-places input {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.change_location__content__submit {
  margin: 0;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  width: 10rem;
  height: 40px;
  border: 1px solid #CCC;
  border-left: none;
}
.ap-input-icon {
  top: 50%;
  transform: translateY(-50%);
}
.ap-dropdown-menu {
  text-align: left;
}
</style>
