<template>
  <el-row>
    <el-col :span="24">
      <div class="grid-content ep-bg-purple-dark"/>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple"/>
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
  </el-row>

  <el-row>
    <el-col :span="12">
      <el-row>
        <el-col :span="12">
          <div class="grid-content ep-bg-gg"/>
        </el-col>
        <el-col :span="6" :offset="3">
          <div class="grid-content ep-bg-gg2"/>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light"/>
    </el-col>
  </el-row>

  <el-row>
    <el-col>
      <div style="width: 500px" class="grid-content ep-bg-gg"/>
      <div style="width: 500px" class="grid-content ep-bg-gg2"/>
    </el-col>
  </el-row>

</template>

<script setup lang="ts">

</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.ep-bg-purple-dark {
  background: #409EFF;
}

.ep-bg-purple {
  background: #c9c4c4;
}

.ep-bg-purple-light {
  background: red;
}

.ep-bg-gg {
  background: green;
}


.ep-bg-gg2 {
  background: salmon;
}
</style>