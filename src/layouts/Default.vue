<template>
  <div class="layout">
    <noscript v-html="`<div id='noscript'>This site requires javascript.</div>`"/>
    <!-- <header class="header">
      <strong>
        <g-link to="/">{{ $static.metadata.siteName }}</g-link>
      </strong>
      <nav class="nav">
        <g-link class="nav__link" to="/">Home</g-link>
        <g-link class="nav__link" to="/about/">About</g-link>
      </nav>
    -->
    <slot/>
    <!-- <Footer/> -->
  </div>
</template>

<static-query>
query {
  metadata {
    siteName
  }
}
</static-query>

<script>
import Footer from "~/components/Footer.vue";

export default {
  components: {
    Footer
  },
}
</script>

<style>
html, body {
  height: 100%;
}
body {
  font-family: -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  margin:0;
  padding:0;
  line-height: 1.5;
}
#app {
  position: relative;
  overflow-x: hidden;
  height: 100%;
}
@media(max-height: 445px) {
  #app {
    height: auto;
  }
}
.show-footer {
  margin-bottom: 10rem;
}
#noscript {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 0.5rem;
  color: #fff;
  text-align: center;
  z-index: 999999;
  background: red;
}
/* .layout {
  max-width: 760px;
  margin: 0 auto;
  padding-left: 20px;
  padding-right: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  height: 80px;
}

.nav__link {
  margin-left: 20px;
} */
</style>
