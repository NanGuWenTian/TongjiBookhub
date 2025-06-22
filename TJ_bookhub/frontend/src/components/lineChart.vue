<template>
    <div class="line-chart-container">
      <canvas ref="chartCanvas" ></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  // 注册Chart.js组件
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
  
  // 初始化图表
  const initChart = () => {
    if (chartInstance) {
      chartInstance.destroy();
    }
    
    if (chartCanvas.value) {
      const ctx = chartCanvas.value.getContext('2d');
      
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: props.data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: ${context.raw}`;
                }
              }
            },
            legend: {
              position: 'top',
              labels: {
                font: {
                  size: 14
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            },
            x: {
              grid: {
                display: false
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            }
          },
          ...props.options
        }
      });
    }
  };
  
  // 监听数据变化
  watch(() => props.data, () => {
    initChart();
  }, { deep: true });
  
  // 组件挂载时初始化图表
  onMounted(() => {
    initChart();
  });
  </script>
  
  <style scoped>
  .line-chart-container {
    position: relative;
    width: 100%;
    height: 400px;
  }
  
  @media (max-width: 768px) {
    .line-chart-container {
      height: 300px;
    }
  }
  </style>