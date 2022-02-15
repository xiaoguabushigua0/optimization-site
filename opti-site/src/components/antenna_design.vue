<template>
  <div id="antenna_design">
    <div class="slidershow middle">
      <div class="slides">
        <input type="radio" name="r" id="r1" checked />
        <input type="radio" name="r" id="r2" />
        <input type="radio" name="r" id="r3" />

        <div class="slide s1">
          <div id="part_design_target" class="part_content">
            <div id="target-left">
              <p class="title_design">一、设计目标</p>
              <p class="description_filter" style="margin-bottom: 13px">
                U 缝贴片天线
              </p>
              <img
                src="../assets/structure_a.svg"
                alt="lost"
                id="img_structure"
              />
              <p class="description_filter1">
                可设计的结构参数为贴片和缝的相关结构尺寸
              </p>
            </div>

            <div id="target-right">
              <p class="bandpass" style="font-weight: 600; letter-spacing: 1px">
                设计频带范围 (GHz)
              </p>
              <br />
              <div class="design_specifications">
                <span class="bandpass">低频</span>
                <input
                  type="text"
                  name=""
                  v-model="f_low_a"
                  placeholder="GHz"
                  class="frequencies"
                  id="f_low"
                />
                <span class="bandpass" id="bandpass_high">高频</span>
                <input
                  type="text"
                  name=""
                  v-model="f_high_a"
                  placeholder="GHz"
                  class="frequencies"
                  id="f_high"
                />
                <button id="btn_target">目标谱线生成</button>
              </div>
              <div id="charu1">
                <img
                  :src="require('../assets/' + path_src_a)"
                  alt=""
                  id="img_target"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="slide">
          <div id="part_inverse" class="part_content"></div>
        </div>

        <div class="slide">
          <div id="part_optimization" class="part_content"></div>
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
      path_src_a: 'blank_target_a.svg',
      f_low_a: '4.5',
      f_high_a: '6',
    }
  },
}
</script>

<style>
#antenna_design {
  position: absolute;
  width: 100%;
  height: 90.3%;
  background-image: url(../assets/bg4.png);
}
</style>
    
