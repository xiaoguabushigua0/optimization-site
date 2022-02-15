<template>
  <div id="home">
    <div class="bg_img">
      <div class="home_content">
        <h1 class="animate__animated animate__fadeInDown">微波器件智能设计</h1>
        <h2 class="animate__animated animate__fadeInUp">
          以人工神经网络作为代理模型、内置遗传算法等优化算法
        </h2>
        <button
          class="btn_antenna animate__animated animate__fadeInUp"
          @click="goto_antenna()"
        >
          天线设计
        </button>
        <button
          class="btn_filter animate__animated animate__fadeInUp"
          @click="goto_filter()"
        >
          滤波器设计
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
    }
  },
  methods: {
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
    }
  }
}
</script>



<style>
body {
  background-image: url(../assets/bg.jpg);
}

h1 {
  color: rgba(255, 255, 255, 0.96);
  letter-spacing: 3px;
  font-size: 40px;
}

h2 {
  color: rgba(255, 255, 255, 0.96);
  letter-spacing: 1px;
  font-size: 27px;
  margin: 20px 0 20px 0;
}

.home_content {
  margin: 100px 0 0 100px;
}

.home_content button {
  width: 130px;
  height: 50px;
  font-size: 20px;
  color: #f2f2f2b2;
  background-color: #171c2400;
  border: 2px solid #171c2480;
  border-radius: 3px;
  letter-spacing: 2px;
  margin-top: 10px;
  cursor: pointer;
}

.home_content button:hover {
  border: 2px solid #ff3d00;
  color: #ffffff;
}

.btn_filter {
  margin-left: 60px;
}
</style>
