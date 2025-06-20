<template>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch,defineProps } from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  const props = defineProps({
    data: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({})
    }
  });
  
  const chartCanvas = ref(null);
  let chartInstance = null;
  
  const initChart = () => {
    if (chartInstance) {
      chartInstance.destroy();
    }
    
    if (chartCanvas.value) {
      const ctx = chartCanvas.value.getContext('2d');
      
      chartInstance = new Chart(ctx, {
        type: 'pie',
        data: props.data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right',
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          },
          ...props.options
        }
      });
    }
  };
  
  onMounted(() => {
    initChart();
  });
  
  watch(() => props.data, () => {
    initChart();
  }, { deep: true });
  </script>
  
  <style scoped lang="scss">
  .chart-wrapper {
    position: relative;
    width: 100%;
    height: 400px;
    canvas {
      padding-top: 5px;
      width: 100%;
    }
  }
  </style>