<script setup>
import PointForm from "@/components/PointForm.vue";
import MathPlot from "@/components/MathPlot.vue";
</script>

<template>
  <header>
    <h1>Computational Lab #5</h1>
  </header>
  <main>
    <div class="x-form">
      <div class="form-group">
        <label for="x">Desired X:</label>
        <input ref="start" id="x" type="number" class="form-control" v-model="x"/>
      </div>
    </div>
    <PointForm @interpolation-result="handleInterpolationResult"/>
    <div v-if="show" class="result-block">
      <h2>Result:</h2>
      <p class="result">L({{ argument === '' ? 'x' : argument }}) = {{ lagrange }}
        {{ argument === '' ? '' : '= ' + lagrange_res }}</p>
      <p class="result">N({{ argument === '' ? 'x' : argument }}) = {{ newton }}
        {{ argument === '' ? '' : '= ' + newton_res }}</p>
    </div>
    <div v-if="show" class="plots">
      <div class="plot">
        <MathPlot :range="range" :newton="newton" :points="points" :func="lagrange"/>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      x: '',
      lagrange: null,
      newton: null,
      points: null,
      show: false,
      argument: '',
      lagrange_res: null,
      newton_res: null,
      range: null
    }
  },
  methods: {
    handleInterpolationResult(result) {
      this.lagrange = result.response.lagrange;
      this.newton = result.response.newton;
      this.show = true;
      this.points = result.points;
      this.argument = this.x;
      let x = this.x;
      this.lagrange_res = eval(this.lagrange);
      this.newton_res = eval(this.newton);
      const l = this.points.map(point => point.x);
      const ys = this.points.map(point => point.y);
      let min_x = l[0], max_x = l[0], min_y = ys[0], max_y = ys[0]
      for (let i = 0; i < l.length; i++) {
        if (l[i] < min_x) min_x = l[i];
        if (l[i] > max_x) max_x = l[i];
        if (ys[i] < min_y) min_y = ys[i];
        if (ys[i] > max_y) max_y = ys[i];
      }
      this.range = [min_x, max_x, min_y, max_y]
    }
  },
}
</script>

<style scoped>
header {
  font-family: Montserrat, sans-serif;
  color: black;
  padding: 20px;
  text-align: center;
}

header h1 {
  margin: 0;
}

.plots {
  width: 80%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
}

.plot {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 400px;
  height: 300px;
  border: 1px solid #ddd;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  padding: 10px;
}

.plot canvas {
  width: 100%;
  height: 80%;
}

.plot-title {
  font-family: Montserrat, sans-serif;
  font-size: 0.8rem;
  font-weight: bold;
  margin-top: 10px;
}

.result-block {
  width: 50%;
  font-family: Montserrat, sans-serif;
  font-size: 1.0rem;
  font-weight: bold;
  margin: 0 auto;
  text-align: center;
}

.x-form {
  font-family: Arial, sans-serif;
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
