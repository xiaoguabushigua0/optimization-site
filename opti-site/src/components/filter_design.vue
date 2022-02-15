<template>
  <div id="filter_design">
    <el-alert
      title="特征处理完毕"
      type="success"
      @close="feature_alert()"
      id="feature_alert"
      style="width: 20%; margin: 25% auto; z-index: 99; display: none"
    >
    </el-alert>
    <el-alert
      :title="'优化完毕，用时' + opti_time + '秒'"
      type="success"
      @close="opti_alert()"
      id="opti_alert"
      style="width: 25%; margin: 25% auto; z-index: 99; display: none"
    >
    </el-alert>
    <div class="slidershow middle">
      <div class="slides">
        <input type="radio" name="r" id="r1" checked />
        <input type="radio" name="r" id="r2" />
        <input type="radio" name="r" id="r3" />

        <div class="slide s1">
          <div id="part_design_target" class="part_content">
            <div id="target-left">
              <p class="title_design">一、设计目标</p>
              <p class="description_filter">金属腔体交指滤波器</p>
              <img
                src="../assets/structure.svg"
                alt="lost"
                id="img_structure"
              />
              <p class="description_filter1">
                可设计的结构参数为谐振杆的长度和间距
              </p>
            </div>

            <div id="target-right">
              <p class="bandpass" style="font-weight: 600; letter-spacing: 1px">
                通带频率范围 (GHz)
              </p>
              <br />
              <div class="design_specifications">
                <span class="bandpass">低频</span>
                <input
                  type="text"
                  name=""
                  v-model="f_low"
                  placeholder="GHz"
                  class="frequencies"
                  id="f_low"
                />
                <span class="bandpass" id="bandpass_high">高频</span>
                <input
                  type="text"
                  name=""
                  v-model="f_high"
                  placeholder="GHz"
                  class="frequencies"
                  id="f_high"
                />
                <button id="btn_target" @click="draw_target">
                  目标谱线生成
                </button>
              </div>
              <div id="charu1">
                <img
                  :src="require('../assets/' + path_src)"
                  alt=""
                  id="img_target"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="slide">
          <div id="part_inverse" class="part_content">
            <div id="inverse-left">
              <p class="title_design">二、逆向设计</p>
              <p class="description_filter">由设计目标得到对应的结构参数</p>
              <p class="description_dnn">使用深度神经网络(DNN)做逆向设计</p>
              <div class="dnn_inverse_results">
                <input
                  type="button"
                  id="btn_dnn_inverse"
                  value="DNN预测"
                  @click="inverse_dnn"
                />
                <div style="margin-top: 10px">
                  <div style="margin-left: 12px">
                    <span class="bandpass">L1</span>
                    <input
                      type="text"
                      class="inverse_predictions"
                      id="L1_dnn"
                      v-model="L1_dnn"
                      placeholder="mm"
                    />
                    <span class="bandpass" style="margin-left: 12px">L2</span>
                    <input
                      type="text"
                      class="inverse_predictions"
                      id="L2_dnn"
                      v-model="L2_dnn"
                      placeholder="mm"
                    />
                  </div>
                  <br />
                  <span class="bandpass" style="margin-left: -3px">d12</span>
                  <input
                    type="text"
                    class="inverse_predictions"
                    id="d12_dnn"
                    v-model="d12_dnn"
                    placeholder="mm"
                  />
                  <span class="bandpass" style="margin-left: -2px">d23</span>
                  <input
                    type="text"
                    class="inverse_predictions"
                    id="d23_dnn"
                    v-model="d23_dnn"
                    placeholder="mm"
                  />
                </div>
              </div>
              <hr id="divider" />
              <p class="description_cnn">使用卷积神经网络(CNN)做逆向设计</p>
              <div style="display: flex; margin-top: -5px">
                <div style="width: 50%">
                  <input
                    type="button"
                    id="btn_feature"
                    value="特征处理"
                    @click="feature"
                  />
                  <div id="feature_maps_div">
                    <div class="demo-image__preview">
                      <el-image
                        style="width: 100px; height: 100px"
                        :src="require('../assets/' + path_src1)"
                        :preview-src-list="[
                          require('../assets/' + feature_map1),
                          require('../assets/' + feature_map2),
                          require('../assets/' + feature_map3),
                          require('../assets/' + feature_map4),
                        ]"
                      >
                      </el-image>
                    </div>
                  </div>
                </div>
                <div style="width: 50%">
                  <el-container
                    v-loading="loading_cnn"
                    style="top: 20%; left: 17%"
                  >
                  </el-container>
                  <input
                    type="button"
                    id="btn_cnn_inverse"
                    value="CNN预测"
                    @click="inverse_cnn"
                  />
                  <div style="margin-top: -10px">
                    <div style="margin-left: -40px">
                      <span class="bandpass">L1</span>
                      <input
                        type="text"
                        class="inverse_predictions1"
                        id="L1_cnn"
                        v-model="L1_cnn"
                        placeholder="mm"
                      />
                      <span class="bandpass" style="margin-left: 0px">L2</span>
                      <input
                        type="text"
                        class="inverse_predictions1"
                        id="L2_cnn"
                        v-model="L2_cnn"
                        placeholder="mm"
                      />
                    </div>
                    <br />
                    <div style="margin-left: -53px">
                      <span class="bandpass">d12</span>
                      <input
                        type="text"
                        class="inverse_predictions1"
                        id="d12_cnn"
                        v-model="d12_cnn"
                        placeholder="mm"
                      />
                      <span class="bandpass" style="margin-left: -18px"
                        >d23</span
                      >
                      <input
                        type="text"
                        class="inverse_predictions1"
                        id="d23_cnn"
                        v-model="d23_cnn"
                        placeholder="mm"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div id="inverse-right">
              <p
                class="bandpass"
                style="
                  display: inline-block;
                  margin-bottom: 20px;
                  font-weight: 600;
                "
              >
                &nbsp;&nbsp;验证谱线
              </p>
              <br />
              <div class="design_specifications">
                <input
                  type="button"
                  id="btn_target"
                  value="前向模型验证"
                  @click="forward_prediction"
                />
                <input
                  type="button"
                  id="btn_target"
                  value="HFSS验证"
                  @click="inverse_hfss"
                />
              </div>
              <el-container
                v-loading="loading_inverse_forward"
                style="top: 35%; left: -2%"
              >
              </el-container>
              <img
                :src="require('../assets/' + path_src2)"
                alt=""
                id="img__forward"
              />
            </div>
          </div>
        </div>

        <div class="slide">
          <div id="part_optimization" class="part_content">
            <div id="optimization_left">
              <p class="title_design">三、代理优化</p>
              <p class="description_filter">
                逆向设计结果作为优化初值，前向模型实现代理
              </p>
              <div style="display: flex">
                <div style="width: 40%">
                  <p
                    style="font-size: 18px; font-weight: 600; margin: 20px 50px"
                  >
                    选择初值
                  </p>
                  <p class="D_C" @click="dnn_or_cnn('dnn')" id="opti_DNN">
                    DNN
                  </p>
                  <p
                    class="D_C"
                    @click="dnn_or_cnn('cnn')"
                    id="opti_CNN"
                    style="margin-top: 15px"
                  >
                    CNN
                  </p>
                </div>

                <div style="width: 60%">
                  <div style="margin-top: 60px">
                    <div style="margin-left: 12px">
                      <span class="bandpass">L1</span>
                      <input
                        type="text"
                        class="initial_values_text"
                        id="L1_init"
                        v-model="L1_init"
                        placeholder="mm"
                      />
                      <span class="bandpass" style="margin-left: 12px">L2</span>
                      <input
                        type="text"
                        class="initial_values_text"
                        id="L2_init"
                        v-model="L2_init"
                        placeholder="mm"
                      />
                    </div>
                    <br />
                    <span class="bandpass" style="margin-left: -3px">d12</span>
                    <input
                      type="text"
                      class="initial_values_text"
                      id="d12_init"
                      v-model="d12_init"
                      placeholder="mm"
                    />
                    <span class="bandpass" style="margin-left: -2px">d23</span>
                    <input
                      type="text"
                      class="initial_values_text"
                      id="d23_init"
                      v-model="d23_init"
                      placeholder="mm"
                    />
                  </div>
                </div>
              </div>
              <hr id="divider1" />
              <p style="font-size: 18px; font-weight: 600; margin: 20px 50px">
                选择算法
              </p>
              <div style="display: flex">
                <div
                  style="
                    display: flex;
                    flex-direction: column;
                    width: 35%;
                    margin-top: 5px;
                    margin-left: 50px;
                  "
                >
                  <p
                    class="algorithmns"
                    @click="which_algorithmn('GA')"
                    id="GA"
                  >
                    遗传算法
                  </p>
                  <p
                    class="algorithmns"
                    @click="which_algorithmn('PSO')"
                    id="PSO"
                  >
                    粒子群算法
                  </p>
                  <p
                    class="algorithmns"
                    @click="which_algorithmn('DE')"
                    id="DE"
                  >
                    差分进化算法
                  </p>
                </div>

                <div style="width: 20%; margin-left: 15px; margin-top: -10px">
                  <span class="bandpass">种群大小</span>
                  <br />
                  <input
                    type="text"
                    class="inverse_predictions1"
                    id="population"
                    v-model="population"
                    style="margin-bottom: 10px; margin-top: 4px; width: 80%"
                  />
                  <br />
                  <span class="bandpass">迭代次数</span>
                  <br />
                  <input
                    type="text"
                    class="inverse_predictions1"
                    id="iteration"
                    v-model="iteration"
                    style="margin-top: 4px; width: 80%"
                  />
                  <input
                    type="button"
                    id="btn_target"
                    value="开始优化"
                    @click="start_opti"
                    style="margin-left: -4px; width: 90%; margin-top: 15px"
                  />
                </div>

                <div style="width: 45%; margin-top: -0px">
                  <el-container
                    v-loading="loading_optimization"
                    style="top: 50%; left: 35%"
                  >
                  </el-container>
                  <div style="margin-left: 30px; margin-top: 5px">
                    <p
                      class="bandpass"
                      style="
                        margin-top: -25px;
                        margin-left: 15px;
                        margin-bottom: 15px;
                      "
                    >
                      优化结果
                    </p>
                    <span class="bandpass">L1</span>
                    <input
                      type="text"
                      class="optimization_structure"
                      id="L1_opti"
                      v-model="L1_opti"
                      placeholder="mm"
                    />
                    <br />
                    <span class="bandpass" style="margin-left: 0px">L2</span>
                    <input
                      type="text"
                      class="optimization_structure"
                      id="L2_opti"
                      v-model="L2_opti"
                      placeholder="mm"
                    />
                    <br />
                    <span class="bandpass" style="margin-left: -13px">d12</span>
                    <input
                      type="text"
                      class="optimization_structure"
                      id="d12_opti"
                      v-model="d12_opti"
                      placeholder="mm"
                    />
                    <br />
                    <span class="bandpass" style="margin-left: -13px">d23</span>
                    <input
                      type="text"
                      class="optimization_structure"
                      id="d23_opti"
                      v-model="d23_opti"
                      placeholder="mm"
                    />
                  </div>
                  <!-- <span class="bandpass">优化时长</span>
                  <br />
                  <input
                    type="text"
                    class="inverse_predictions1"
                    id="opti_time"
                    v-model="opti_time"
                    style="width: 31%; margin-top: 4px"
                    placeholder="秒"
                  /> -->
                </div>
              </div>
            </div>

            <div id="optimization_right">
              <p
                class="bandpass"
                style="
                  display: inline-block;
                  margin-bottom: 20px;
                  font-weight: 600;
                "
              >
                &nbsp;&nbsp;验证谱线
              </p>
              <br />
              <div class="design_specifications">
                <input
                  type="button"
                  id="btn_target"
                  value="前向模型验证"
                  @click="forward_prediction_opti"
                />
                <input
                  type="button"
                  id="btn_target"
                  value="HFSS验证"
                  @click="opti_hfss"
                />
              </div>
              <img
                :src="require('../assets/' + path_src3)"
                alt=""
                id="img__opti"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="navigation">
      <label for="r1" class="bar"></label>
      <label for="r2" class="bar"></label>
      <label for="r3" class="bar"></label>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';

export default {
  name: 'filter_design',
  data () {
    return {
      loading_optimization: false,
      loading_inverse_forward: false,
      loading_cnn: false,
      path_src: 'blank_target.svg',
      path_src1: 'target.png',
      path_src2: 'blank_target.svg',
      path_src3: 'blank_target.svg',
      srcList: [
      ],
      feature_map1: 'target.png',
      feature_map2: 'target.png',
      feature_map3: 'target.png',
      feature_map4: 'target.png',
      f_low: '2.4',
      f_high: '3.4',
      temp_low: '',
      temp_high: '',
      L1_dnn: '',
      L2_dnn: '',
      d12_dnn: '',
      d23_dnn: '',
      L1_cnn: '',
      L2_cnn: '',
      d12_cnn: '',
      d23_cnn: '',
      flag_dnn_cnn: '',
      L1_init: '',
      L2_init: '',
      d12_init: '',
      d23_init: '',
      population: '20',
      iteration: '15',
      opti_time: '',
      L1_opti: '',
      L2_opti: '',
      d12_opti: '',
      d23_opti: '',
      opti_method: '',
      F: [],
    }
  },
  methods: {
    draw_target () {
      axios({
        method: 'post',
        url: '/API',
        data: {
          frequencies: [this.f_low, this.f_high]
        }
      }).then(res => {
        this.path_src = 'target.svg';
      });
      // 异步加载图片背景
      //   https://blog.csdn.net/weixin_30412013/article/details/96432724?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link
    },
    inverse_dnn () {
      axios({
        method: 'post',
        url: '/inverse_dnn',
        data: {
          frequencies: [this.f_low, this.f_high]
        }
      }).then(res => {
        this.L1_dnn = res.data.L1;
        this.L2_dnn = res.data.L2;
        this.d12_dnn = res.data.d12;
        this.d23_dnn = res.data.d23;
      });
    },
    feature () {
      axios({
        url: 'feature',
        method: 'post',
        data: {
          frequencies: [this.f_low, this.f_high]
        }
      }).then(res => {
        console.log(res.data);
        this.feature_map1 = 'mergex1.png';
        this.feature_map2 = '1x.png';
        this.feature_map3 = '2x.png';
        this.feature_map4 = '3x.png';
        document.querySelector('#feature_alert').style.display = 'block';
      })
    },
    feature_alert () {
      document.querySelector('#feature_alert').style.display = 'none';
    },
    inverse_cnn () {
      this.loading_cnn = true;
      axios({
        method: 'post',
        url: '/inverse_cnn',
        data: {
          name: './imgs/merge.png'
        }
      }).then(res => {
        // console.log(res.data);
        this.loading_cnn = false;
        this.L1_cnn = res.data.L1;
        this.L2_cnn = res.data.L2;
        this.d12_cnn = res.data.d12;
        this.d23_cnn = res.data.d23;
      });
    },
    forward_prediction () {
      this.loading_inverse_forward = true;
      axios({
        url: '/forward_prediction',
        method: 'post',
        data: {
          parameters: [this.L1_dnn, this.L2_dnn, this.d12_dnn, this.d23_dnn,
          this.L1_cnn, this.L2_cnn, this.d12_cnn, this.d23_cnn,
          this.f_low, this.f_high]
        }
      }).then(res => {
        this.loading_inverse_forward = false;
        this.path_src2 = 'forward_prediction.svg';
      })
    },
    inverse_hfss () {
      axios({
        url: '/inverse_hfss',
        method: 'post',
        data: {
          parameters: [this.L1_cnn, this.L2_cnn, this.d12_cnn, this.d23_cnn, this.f_low, this.f_high]
        }
      }).then(res => {
        this.path_src2 = 'inverse_hfss.svg';
      })
    },
    dnn_or_cnn (s) {
      if (s === 'dnn') {
        document.querySelector("#opti_DNN").style.backgroundColor = '#fff';
        document.querySelector("#opti_DNN").style.fontWeight = 600;
        document.querySelector("#opti_DNN").style.color = '#ff3d00';
        document.querySelector("#opti_DNN").style.border = '2px solid #6e6a69';
        document.querySelector("#opti_CNN").style.backgroundColor = '';
        document.querySelector("#opti_CNN").style.fontWeight = 500;
        document.querySelector("#opti_CNN").style.color = 'black';
        document.querySelector("#opti_CNN").style.border = '2px solid black';
        this.L1_init = this.L1_dnn;
        this.L2_init = this.L2_dnn;
        this.d12_init = this.d12_dnn;
        this.d23_init = this.d23_dnn;
      } else {
        document.querySelector("#opti_CNN").style.backgroundColor = '#fff';
        document.querySelector("#opti_CNN").style.fontWeight = 600;
        document.querySelector("#opti_CNN").style.color = '#ff3d00';
        document.querySelector("#opti_CNN").style.border = '2px solid #6e6a69';
        document.querySelector("#opti_DNN").style.backgroundColor = '';
        document.querySelector("#opti_DNN").style.fontWeight = 500;
        document.querySelector("#opti_DNN").style.color = 'black';
        document.querySelector("#opti_DNN").style.border = '2px solid black';
        this.L1_init = this.L1_cnn;
        this.L2_init = this.L2_cnn;
        this.d12_init = this.d12_cnn;
        this.d23_init = this.d23_cnn;
      }
    },
    which_algorithmn (s) {
      if (s === 'GA') {
        document.querySelector("#GA").style.backgroundColor = '#fff';
        document.querySelector("#GA").style.fontWeight = 600;
        document.querySelector("#GA").style.color = '#ff3d00';
        document.querySelector("#GA").style.border = '2px solid #6e6a69';
        document.querySelector("#DE").style.backgroundColor = '';
        document.querySelector("#DE").style.fontWeight = 500;
        document.querySelector("#DE").style.color = 'black';
        document.querySelector("#DE").style.border = '2px solid black';
        document.querySelector("#PSO").style.backgroundColor = '';
        document.querySelector("#PSO").style.fontWeight = 500;
        document.querySelector("#PSO").style.color = 'black';
        document.querySelector("#PSO").style.border = '2px solid black';
        this.opti_method = 'GA';
      } else if (s === 'PSO') {
        document.querySelector("#PSO").style.backgroundColor = '#fff';
        document.querySelector("#PSO").style.fontWeight = 600;
        document.querySelector("#PSO").style.color = '#ff3d00';
        document.querySelector("#PSO").style.border = '2px solid #6e6a69';
        document.querySelector("#DE").style.backgroundColor = '';
        document.querySelector("#DE").style.fontWeight = 500;
        document.querySelector("#DE").style.color = 'black';
        document.querySelector("#DE").style.border = '2px solid black';
        document.querySelector("#GA").style.backgroundColor = '';
        document.querySelector("#GA").style.fontWeight = 500;
        document.querySelector("#GA").style.color = 'black';
        document.querySelector("#GA").style.border = '2px solid black';
        this.opti_method = 'PSO';
      } else {
        document.querySelector("#DE").style.backgroundColor = '#fff';
        document.querySelector("#DE").style.fontWeight = 600;
        document.querySelector("#DE").style.color = '#ff3d00';
        document.querySelector("#DE").style.border = '2px solid #6e6a69';
        document.querySelector("#PSO").style.backgroundColor = '';
        document.querySelector("#PSO").style.fontWeight = 500;
        document.querySelector("#PSO").style.color = 'black';
        document.querySelector("#PSO").style.border = '2px solid black';
        document.querySelector("#GA").style.backgroundColor = '';
        document.querySelector("#GA").style.fontWeight = 500;
        document.querySelector("#GA").style.color = 'black';
        document.querySelector("#GA").style.border = '2px solid black';
        this.opti_method = 'DE';
      }
    },
    start_opti () {
      this.loading_optimization = true;
      this.L1_opti = '';
      this.L2_opti = '';
      this.d12_opti = '';
      this.d23_opti = '';
      if (this.L1_init === '') {
        alert("请选择初值！");
      } else {
        if (this.opti_method === '') {
          alert("请选择优化算法！");
        } else {
          let name = '';
          if (this.opti_method === 'GA') {
            name = '/optimization_ga';
          } else if (this.opti_method === 'PSO') {
            name = '/optimization_pso';
          } else {
            name = '/optimization_de';
          }
          axios({
            url: name,
            method: 'post',
            data: {
              parameters: [this.population, this.iteration, this.L1_init, this.L2_init, this.d12_init,
              this.d23_init, this.f_low, this.f_high]
            }
          }).then(res => {
            // alert("优化完毕，用时" + res.data.time + "秒");
            this.opti_time = res.data.time;
            this.L1_opti = res.data.L1;
            this.L2_opti = res.data.L2;
            this.d12_opti = res.data.d12;
            this.d23_opti = res.data.d23;
            this.F = res.data.F
            document.querySelector('#opti_alert').style.display = 'block';
            this.loading_optimization = false;
          })
        }
      }
      //   this.opti_method = '';
    },
    opti_alert () {
      document.querySelector('#opti_alert').style.display = 'none';
    },
    forward_prediction_opti () {
      axios({
        url: '/forward_opti',
        method: 'post',
        data: {
          parameters: [this.L1_opti, this.L2_opti, this.d12_opti, this.d23_opti, this.f_low, this.f_high, this.F]
        }
      }).then(res => {
        this.path_src3 = 'forward_prediction_opti.svg';
      })
    },
    opti_hfss () {
      axios({
        url: '/opti_hfss',
        method: 'post',
        data: {
          parameters: [this.L1_opti, this.L2_opti, this.d12_opti, this.d23_opti, this.f_low, this.f_high, this.F]
        }
      }).then(res => {
        this.path_src3 = 'optimization_hfss.svg';
      })
    },
  },
  watch: {
    f_low: {
      handler () {
        this.f_high = '';
        this.L1_dnn = '';
        this.L2_dnn = '';
        this.d12_dnn = '';
        this.d23_dnn = '';
        this.L1_cnn = '';
        this.L2_cnn = '';
        this.d12_cnn = '';
        this.d23_cnn = '';
        this.path_src = 'blank_target.svg';
        this.path_src1 = 'target.png';
        this.path_src2 = 'blank_target.svg';
        this.path_src3 = 'blank_target.svg';
        this.L1_init = '';
        this.L2_init = '';
        this.d12_init = '';
        this.d23_init = '';
        this.L1_opti = '';
        this.L2_opti = '';
        this.d12_opti = '';
        this.d23_opti = '';
      },
    },
  },
}
</script>

<style>
button {
  cursor: pointer;
}
#filter_design {
  position: absolute;
  width: 100%;
  height: 90.3%;
  background-image: url(../assets/bg4.png);
}

.slidershow {
  width: 1050px;
  height: 520px;
  overflow: hidden;
  border-radius: 20px;
}
.middle {
  position: absolute;
  top: 46%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.navigation {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
}
.bar {
  /* position: absolute; */
  width: 50px;
  height: 15px;
  border: 2px solid #171c24;
  margin: 5px 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.4s;
}
.bar:hover {
  background: #171c24;
}

input[name="r"] {
  position: absolute;
  visibility: hidden;
}

.slides {
  width: 300%;
  height: 100%;
  display: flex;
}

.slide {
  width: 33.33%;
  transition: 0.6s;
}
.slide .part_content {
  width: 100%;
  height: 100%;
}

#r1:checked ~ .s1 {
  margin-left: 0;
}
#r2:checked ~ .s1 {
  margin-left: -33.33%;
}
#r3:checked ~ .s1 {
  margin-left: -66.66%;
}

#part_design_target {
  background-color: #eae3c8;
  display: flex;
}
#part_inverse {
  background-color: #cfc5a5;
  display: flex;
}
#part_optimization {
  background-color: #c2b092;
  display: flex;
}

#target-left {
  width: 100%;
  margin-left: 5%;
  padding-top: 1%;
}
#target-right {
  width: 100%;
  margin-left: 0%;
  padding-top: 3%;
}

.title_design {
  font-weight: 800;
  font-size: 25px;
  margin-left: 50px;
  padding-top: 20px;
}
.description_filter {
  font-weight: 600;
  font-size: 20px;
  margin-left: 50px;
  margin-top: 25px;
}
#img_structure {
  width: 70%;
  margin-left: 50px;
  margin-top: 15px;
  border-radius: 5px;
}
.description_filter1 {
  font-weight: 500;
  font-size: 18px;
  margin-left: 50px;
  margin-top: 15px;
}
.bandpass {
  font-weight: 500;
  font-size: 18px;
  margin-top: 15px;
  margin-right: 12px;
}
.frequencies {
  width: 10%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
}
#bandpass_high {
  margin-left: 30px;
}
#btn_target {
  margin-left: 13%;
  width: 25%;
  height: 35px;
  border-color: aliceblue;
  border: 2px solid rgb(131, 131, 131);
  border-radius: 3px;
  font-weight: 600;
  font-size: 17px;
  cursor: pointer;
}
#img_target {
  width: 85%;
  margin-top: 3%;
  border-radius: 5px;
}
#img__forward {
  width: 85%;
  margin-top: 3%;
  border-radius: 5px;
  margin-left: 15px;
}
#img__opti {
  width: 85%;
  margin-top: 3%;
  border-radius: 5px;
  margin-left: 15px;
}
#inverse-left {
  width: 50%;
  margin-left: 5%;
  padding-top: 1%;
}
#inverse-right {
  width: 50%;
  margin-left: 0%;
  padding-top: 3%;
}
.description_dnn {
  font-weight: 400;
  font-size: 17px;
  margin-left: 90px;
  margin-top: 25px;
}
.description_cnn {
  font-weight: 400;
  font-size: 17px;
  margin-left: 90px;
  margin-top: 25px;
}
.inverse_predictions {
  width: 18%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
  margin-right: 60px;
}
.inverse_predictions1 {
  width: 22%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
  margin-right: 40px;
}
.initial_values_text {
  width: 18%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
  margin-right: 60px;
}
#btn_dnn_inverse {
  width: 30%;
  height: 35px;
  border-color: aliceblue;
  border: 2px solid rgb(131, 131, 131);
  border-radius: 3px;
  font-weight: 600;
  font-size: 16px;
  margin: 30px 40px 30px 30px;
  cursor: pointer;
}
.dnn_inverse_results {
  display: flex;
  margin: 20px 0;
}
#divider {
  border-top: 1px solid rgb(165, 165, 165);
  width: 90%;
  margin-top: -10px;
}
#divider1 {
  border-top: 1px solid rgb(165, 165, 165);
  width: 80%;
  margin-top: 20px;
  margin-left: 50px;
}
#btn_cnn_inverse {
  width: 32%;
  height: 35px;
  border-color: aliceblue;
  border: 2px solid rgb(131, 131, 131);
  border-radius: 3px;
  font-weight: 600;
  font-size: 16px;
  margin: 20px 40px 30px 30px;
  margin-left: 40px;
  cursor: pointer;
}
#btn_feature {
  width: 30%;
  height: 35px;
  border-color: aliceblue;
  border: 2px solid rgb(131, 131, 131);
  border-radius: 3px;
  font-weight: 600;
  font-size: 16px;
  margin: 20px 40px 30px 30px;
  margin-left: 45px;
  cursor: pointer;
}
#feature_maps_div {
  width: 100px;
  margin-left: 12%;
  margin-top: -5%;
}
#feature_maps {
  width: 100%;
}

#optimization_left {
  width: 50%;
  margin-left: 5%;
  padding-top: 1%;
}
#optimization_right {
  width: 50%;
  margin-left: 0%;
  padding-top: 3%;
}
.D_C {
  border-radius: 5px;
  border: 2px solid black;
  padding: 3px 7px;
  margin-left: 90px;
  display: inline-block;
  margin-top: 10px;
}
.D_C:hover {
  background-color: #fff;
  color: #ff3d00;
  border: 2px solid #6e6a69;
  cursor: pointer;
  font-weight: 600;
}
.initial_values_text {
  width: 22%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
  margin-right: 30px;
}
#opti_DNN {
  margin-top: -20px;
}
.algorithmns {
  border-radius: 5px;
  border: 2px solid black;
  padding: 3px 7px;
  margin: 7px auto;
}
.algorithmns:hover {
  background-color: #fff;
  color: #ff3d00;
  border: 2px solid #6e6a69;
  cursor: pointer;
  font-weight: 600;
}
#btn_start_opti {
  border-radius: 5px;
  border: 2px solid black;
  padding: 3px 7px;
  margin-left: 10px;
  display: inline-block;
}
#btn_start_opti:hover {
  background-color: #fff;
  color: #ff3d00;
  border: 2px solid #6e6a69;
  cursor: pointer;
  font-weight: 600;
}
.optimization_structure {
  width: 36%;
  border-radius: 5px;
  height: 25px;
  border: 1px solid rgb(131, 131, 131);
  font-size: 19px;
  margin-bottom: 10px;
}
</style>
