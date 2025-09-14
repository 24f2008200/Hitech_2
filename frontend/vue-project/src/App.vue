<template>
  <div>
    <Navbar />
    <router-view />  <!-- Page content goes here -->
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue"

export default {
  components: { Navbar }
}
</script>
