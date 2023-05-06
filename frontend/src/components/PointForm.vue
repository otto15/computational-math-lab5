<template>
  <div class="container">
    <div v-if="showPointsTable" class="tb">
      <table class="points-table">
        <thead>
        <tr>
          <th>X</th>
          <th>Y</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(point, index) in points" :key="index">
          <td>
            <input type="number" v-model.number="point.x" step="0.01" :ref="`x${index}`">
            <div v-if="errorMessages[`x${index}`]" class="error-message">{{ errorMessages[`x${index}`] }}</div>
          </td>
          <td>
            <input type="number" v-model.number="point.y" step="0.01" :ref="`y${index}`">
            <div v-if="errorMessages[`y${index}`]" class="error-message">{{ errorMessages[`y${index}`] }}</div>
          </td>
          <td>
            <button @click="removePoint(index)" class="remove-btn">Remove</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="function-form">
      <div class="form-group">
        <label for="functionInput">Function</label>
        <select id="functionInput" class="form-control" v-model="func">
          <option v-for="(func, i) in functions" :key="i" :value="func">
            {{ func }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="intervalInput1">Start of Interval</label>
        <input ref="start" id="intervalInput1" type="number" class="form-control" v-model="start"/>
        <div v-if="errorMessages['interval1']" class="error-message">{{ errorMessages['interval1'] }}</div>
      </div>
      <div class="form-group">
        <label for="intervalInput2">End of Interval</label>
        <input ref="end" id="intervalInput2" type="number" class="form-control" v-model="end"/>
        <div v-if="errorMessages['interval2']" class="error-message">{{ errorMessages['interval2'] }}</div>
      </div>
      <div class="form-group">
        <label for="pointsInput">Number of Points</label>
        <input ref="numPoints" id="pointsInput" type="number" class="form-control" v-model.number="numPoints" min="1"
               max="10"/>
        <div v-if="errorMessages['numPoints']" class="error-message">{{ errorMessages['numPoints'] }}</div>
      </div>
    </div>
    <div class="buttons-container">
      <button @click="toggleView" class="toggle-btn">
        {{ showPointsTable ? 'Enter Function' : 'Enter Points' }}
      </button>
      <button @click="addPoint" :disabled="points.length >= 10 || !showPointsTable" class="add-btn">Add Point</button>
      <div class="file-upload">
        <label for="upload" class="custom-file-upload">
          <i class="fa fa-cloud-upload"></i> Choose File
        </label>
        <input id="upload" type="file" ref="fileInput" @click="resetImageUploader" @change="handleFileUpload"/>
      </div>
      <button :title="errorMessage" @click="sendPoints"
              :disabled="showPointsTable && (points.length < 2 || points.length > 10)"
              class="send-btn">
        Interpolate
      </button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showPointsTable: true,
      func: 'Math.exp(x)',
      interval: '',
      numPoints: '',
      points: [{x: null, y: null}],
      errorMessages: {},
      errorMessage: null,
      functions: ['Math.exp(x)', '(x)**3 - (x)**2 + 11'],
      start: null,
      end: null
    };
  },
  mounted() {
    this.focusLastX();
  },
  methods: {
    toggleView() {
      this.points = [{x: null, y: null}];
      this.errorMessages = {};
      this.showPointsTable = !this.showPointsTable;
    },
    isValid() {
      this.points.forEach((value, index) => {
        if (value.x === null || value.x === "") {
          this.errorMessages[`x${index}`] = 'X value must not be absent';
          this.$nextTick(() => {
            this.$refs[`x${index}`][0].addEventListener('input', () => {
              this.errorMessages[`x${index}`] = null;
            });
          });
        }
        if (value.y === null || value.y === "") {
          this.errorMessages[`y${index}`] = 'Y value must not be absent';
          this.$nextTick(() => {
            this.$refs[`y${index}`][0].addEventListener('input', () => {
              this.errorMessages[`y${index}`] = null;
            });
          });
        }
      });
      let only_x = this.points.map(point => point.x);
      let st = new Set(only_x)
      if (st.size !== only_x.length) {
        only_x.forEach((value, index) => {
          if (value !== null && value !== "" && only_x.indexOf(value) !== index) {
            this.errorMessages[`x${index}`] = 'X values must be unique';
            this.$nextTick(() => {
              this.$refs[`x${index}`][0].addEventListener('input', () => {
                this.errorMessages[`x${index}`] = null;
              });
            });
          }
        });
        return false;
      }

      return !!this.points.every(point => point.x !== null && point.y !== null && point.x !== "" && point.y !== "");


    },
    addPoint() {
      if (this.points.length < 10) {
        this.points.push({x: null, y: null});
        this.$nextTick(() => {
          this.focusLastX();
        });
      }
    },
    removePoint(index) {
      this.points.splice(index, 1);
    },
    preparePoints() {
      this.errorMessages = {};
      let validationResult = true;
      if (isNaN(this.start) || this.start === '' || this.start === null) {
        this.errorMessages[`interval1`] = 'Start of interval must be provided';
        validationResult = false;
      }
      if (this.end <= this.start || isNaN(this.end) || this.end === '' || this.end === null) {
        this.errorMessages[`interval2`] = 'End of interval must be provided and greater than start';
        validationResult = false;
      }
      if (this.numPoints > 10 || this.numPoints < 2 || this.numPoints % 1 !== 0 || isNaN(this.numPoints) || this.numPoints === '' || this.numPoints === null) {
        this.errorMessages[`numPoints`] = 'Number of points must be provided and in interval [2, 10]';
        validationResult = false;
      }

      if (!validationResult) return false;

      let step = (this.end - this.start) / (this.numPoints - 1);
      let first = this.start;

      this.points = [];
      for (let i = 0; i < this.numPoints; i++) {
        let x = first + i * step;
        this.points.push({x: x, y: eval(this.func)})
      }

      return true;
    },
    sendPoints() {
      if ((!this.showPointsTable && this.preparePoints()) || (this.showPointsTable && this.isValid())) {
        const p = this.points;
        console.log(this.points);
        axios
            .post(import.meta.env.VITE_BACKEND_URL + "/interpolation", {points: this.points})
            .then(response => {
              console.log(response.data);
              this.$emit('interpolation-result', {response: response.data, points: p});
            })
            .catch(() => {
              this.errorMessage = 'Error sending points to server';
            });
      }
    },
    focusLastX() {
      const lastIndex = this.points.length - 1;

      let xInput = this.$refs[`x${lastIndex}`][0];
      let yInput = this.$refs[`y${lastIndex}`][0];
      xInput.focus();

      xInput.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter') return;
        if (xInput.value !== '') {
          yInput.focus();
        }
      });
    },
    handleFileUpload(event) {
      if (!this.showPointsTable) this.showPointsTable = true;
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.errorMessages = {};
        const lines = reader.result.trim().split('\n');
        let i = 0
        let points = lines.map(line => {
          const [x, y] = line.trim().split(/\s+/);
          if (isNaN(Number(x))) {
            this.errorMessages[`x${i}`] = 'Invalid x value';
          }
          if (isNaN(Number(y))) {
            this.errorMessages[`y${i}`] = 'Invalid y value';
          }
          i++;
          return {x: Number(x), y: Number(y)};
        });
        this.points = [];
        points = points.slice(0, Math.min(points.length, 10));
        points.forEach((point, index) => {
          this.points.push({x: point.x, y: point.y});
          if (isNaN(point.x)) {
            this.$nextTick(() => {
              this.$refs[`x${index}`][0].addEventListener('input', () => {
                this.errorMessages[`x${index}`] = null;
              });
            });
          }
          if (isNaN(point.y)) {
            console.log("blah")
            this.$nextTick(() => {
              this.$refs[`y${index}`][0].addEventListener('input', () => {
                this.errorMessages[`y${index}`] = null;
              });
            });
          }
        });
        this.isValid();
      };
      reader.readAsText(file);
    },
    resetImageUploader() {
      this.$refs.fileInput.value = '';
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.points-table {
  border-style: hidden;
  border-collapse: collapse;
  width: 100%;
}

.tb {
  border: 2px solid #ccc;
  border-radius: 10px;
}

.points-table th,
.points-table td {
  font-family: Arial, serif;
  padding: 0.5rem;
  text-align: center;
  border: 2px solid #ccc;
}

.points-table th:first-child {
  border-radius: 10px 0 0 0;
}

.points-table th:last-child {
  border-radius: 0 10px 0 0;
}

.points-table th {
  background-color: #f5f5f5;
}

.points-table tr:last-child td:first-child {
  border-radius: 0 0 0 10px;
}

.points-table tr:last-child td:last-child {
  border-radius: 0 0 10px 0;
}

.points-table input[type="number"] {
  font-family: Arial, serif;
  width: 80%;
  padding: 0.5rem;
  border: none;
  text-align: center;
  font-size: 15px;
}

.buttons-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.toggle-btn,
.add-btn,
.send-btn,
.custom-file-upload,
.remove-btn {

  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #4caf50;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.add-btn:disabled,
.send-btn:disabled {
  opacity: 0.5;
  cursor: default;
}

.toggle-btn {
  background-color: #7c06c0;
}

.send-btn {
  background-color: #2196f3;
}

.remove-btn {
  background-color: #f44336;
}

.add-btn:hover {
  background-color: #3e8e41;
}

.send-btn:hover {
  background-color: #0673c0;
}

.remove-btn:hover {
  background-color: #b21e13;
}

.error-message {
  margin-top: 1rem;
  padding: 0.5rem;
  border: 1px solid #f44336;
  background-color: #ffebee;
  color: #f44336;
  font-size: 0.8rem;
  text-align: center;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  /* display: none; <- Crashes Chrome on hover */
  -webkit-appearance: none;
  margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}

.file-upload input[type="file"] {
  display: none;
}

.custom-file-upload {
  font-family: Arial, sans-serif;
  display: inline-block;
  padding: 10px 20px;
  cursor: pointer;
  background-color: #eca637;
  color: #fff;
  border-radius: 5px;
  border: none;
}

.custom-file-upload:hover {
  background-color: #ec9914;
}

.function-form {
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