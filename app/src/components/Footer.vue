<template>
  <footer id="footer">
    <div>
      <g-link to="/about/">About this site.</g-link>
    </div>
    <p class="copyright">&copy; Copyright {{ new Date().getFullYear() }} Daniel Herskowitz.</p>
  </footer>
</template>

<script>
export default {
  name: "Footer"
};
</script>

<style scoped>
#footer {
  background: rgba(102, 51, 153, 1);
  /* position: fixed; */
  /* bottom: 0;
  left: 0;
  width: 100%;
  z-index: -1; */
  height: 10rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.copyright {
  padding: 0;
}
</style>