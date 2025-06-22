<template>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch} from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  const props = defineProps({
    data: {
      type: Object,
      default: () => ({
        labels: ['默认类别'],
        datasets: [{
          label: '默认数据',
          data: [100],
          backgroundColor: ['#8d6e63']
        }]
      })
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
        type: 'bar',
        data: props.data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `借阅数量: ${context.raw}`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: '借阅数量'
              }
            },
            x: {
              title: {
                display: true,
                text: '书籍类别'
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
    canvas{
      height: 100% !important;
      width: 100%;
      padding-top: 5px;
    }
  }
  </style>