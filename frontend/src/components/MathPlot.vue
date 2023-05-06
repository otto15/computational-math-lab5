<template>
  <div ref="plot"/>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  props: {
    newton: {
      type: String,
      required: true
    },
    points: {
      default: null
    },
    func: {
      type: String,
      required: true,
      default: "x"
    },
    range: {
      type: Array,
      default: () => [-10, 10]
    },
    numPoints: {
      type: Number,
      default: 100
    }
  },
  watch: {
    func: 'renderPlot'
  },
  mounted() {
    this.renderPlot();
  },
  methods: {
    renderPlot() {
      const {func, newton, range, numPoints, points} = this;
      const xs = [];
      const ys = [];
      const step = (range[1] - range[0]) / numPoints;
      for (let x = range[0]; x <= range[1]; x += step) {
        xs.push(x);
        ys.push(eval(func));
      }

      const trace = {
        x: xs,
        y: ys,
        name: 'Lagrange'
      };

      const n_xs = [];
      const n_ys = [];

      for (let x = range[0]; x <= range[1]; x += step) {
        n_xs.push(x);
        n_ys.push(eval(newton));
      }

      const trace1 = {
        x: n_xs,
        y: n_ys,
        name: 'Newton'
      }

      const trace2 = {
        x: points.map(point => point.x),
        y: points.map(point => point.y),
        mode: 'markers',
        name: 'Points'
      };

      const layout = {
        xaxis: {
          title: 'x'
        },
        yaxis: {
          title: 'y',
          range: [range[2], range[3]]
        }
      };

      Plotly.newPlot(this.$refs.plot, [trace, trace1, trace2], layout);
    }
  }
};
</script>

<style scoped>
div {
  width: 100%;
  height: 100%;
}
</style>
