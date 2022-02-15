<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <nav>
      <div class="logo">
        <img src="./assets/logo.png" alt="lost" />
        微波器件设计平台
      </div>
      <div class="nav-items">
        <li><a href="#" @click="goto_home()">主页</a></li>
        <li><a href="#" @click="goto_antenna()">天线设计</a></li>
        <li><a href="#" @click="goto_filter()">滤波器设计</a></li>
        <li><a href="#" @click="goto_architecture()">架构说明</a></li>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    // HelloWorld
  },
  methods: {

    goto_home () {
      this.$router.push({
        name: "home",
        path: '/home',
      })
    },
    goto_filter () {
      this.$router.push({
        name: "filter_design",
        path: '/filter_design',
      })
    },
    goto_antenna () {
      this.$router.push({
        name: "antenna_design",
        path: '/antenna_design',
      })
    },
    goto_architecture () {
      this.$router.push({
        name: "architecture",
        path: '/architecture',
      })
    }

  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
nav {
  background-color: #171c24;
  display: flex;
  flex-wrap: wrap;
  /* 让弹性盒元素在必要的时候拆行： */
  align-items: center;
  justify-content: space-between;
  height: 70px;
  padding: 0 80px 0 50px;
}

nav .logo {
  color: #fff;
  font-size: 30px;
  font-weight: 600;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  line-height: 70px;
}

nav .logo img {
  width: 60px;
  height: 60px;
  margin-right: 20px;
}

nav .nav-items {
  display: flex;
  list-style: none;
  padding: 0 0 0 40px;
}

nav .nav-items li {
  padding: 0 15px;
}

nav .nav-items li a {
  color: #fff;
  font-size: 20px;
  font-weight: 500;
  text-decoration: none;
}

nav .nav-items li a:hover {
  color: #ff3d00;
}
</style>
