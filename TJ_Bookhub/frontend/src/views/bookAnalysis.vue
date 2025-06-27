<template>
  <div class="book-stats-view">    
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>图书馆书籍借阅统计</h1>
    </div>
    
    <!-- 借阅统计图表 - 并排显示 -->
    <section class="stats-section">
      <div class="section-header">
        <h2>各类书籍借阅情况</h2>
      </div>
      
      <div class="dual-chart-container">
        <div class="chart-half barChart">
          <h3>借阅数量对比</h3>
          <barChart :data="borrowData" :options="barOptions" />
        </div>
        <div class="chart-half pieChart">
          <h3>借阅比例分布</h3>
          <pieChart class="pie_chart" :data="borrowData" :options="pieOptions" />
        </div>
      </div>
    </section>
    
    <!-- 书籍排行榜 -->
    <section class="ranking-section">
      <div class="section-header">
        <h2>书籍借阅排行榜</h2>
        <div class="category-selector">
          <select v-model="selectedCategory">
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="ranking-table">
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>书名</th>
              <th>借阅次数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in topBooks[selectedCategory]" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ book.title }}</td>
              <td>{{ book.borrows }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    
    <!-- 新增折线图 -->
    <section class="linechart-section">
      <div class="section-header">
        <h2>书籍借阅趋势分析</h2>
        <div class="chart-controls">
          <select v-model="selectedLineCategory" class="control-select">
            <option value="all">全部类别</option>
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <select v-model="selectedTimeRange" class="control-select">
            <option value="12">最近12个月</option>
            <option value="6">最近6个月</option>
            <option value="3">最近3个月</option>
          </select>
        </div>
      </div>
      <div class="chart-container">
        <lineChart :data="filteredLineData" :options="lineOptions" />
      </div>
    </section>
    
    <!-- 词云图 -->
    <section class="wordcloud-section">
      <div class="section-header">
        <h2>借阅热书词云</h2>
      </div>
      <div class="wordcloud-container">
        <wordCloud :words="wordCloudData" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import barChart from '@/components/barChart.vue';
import pieChart from '@/components/pieChart.vue';
import lineChart from '@/components/lineChart.vue';
import wordCloud from '@/components/wordCloud.vue';

// 模拟数据
const categories = ref([
  { id: 1, name: '文学' },
  { id: 2, name: '历史' },
  { id: 3, name: '科学' },
  { id: 4, name: '艺术' },
  { id: 5, name: '哲学' }
]);

const borrowData = reactive({
  labels: ['文学', '历史', '科学', '艺术', '哲学'],
  datasets: [{
    label: '借阅数量',
    data: [1250, 890, 760, 680, 520],
    backgroundColor: function(context) {
      const dataIndex = context.dataIndex;
      // 根据数据索引返回不同颜色
      const colors = ['#FF6384', '#36A2EB', '#ffec3d', '#4BC0C0', '#9966FF'];
      return colors[dataIndex];
    },
    hoverOffset: 10
  }]
});

const topBooks = ref({
  1: [
    { title: '百年孤独', borrows: 381 },
    { title: '哈姆雷特', borrows: 320 },
    { title: '活着', borrows: 256 },
    { title: '局外人', borrows: 243 },
    { title: '月亮与六便士', borrows: 224 }
  ],
  2: [
    { title: '康熙的红票', borrows: 195 },
    { title: '大明王朝1566', borrows: 180 },
    { title: '万历十五年', borrows: 155 },
    { title: '明朝那些事儿', borrows: 140 },
    { title: '三国志', borrows: 131 },
  ],
  3: [
    { title: '数据结构', borrows: 210 },
    { title: '计算机系统结构', borrows: 185 },
    { title: '人类简史', borrows: 165 },
    { title: '量子物理', borrows: 142 },
    { title: '宇宙的奥秘', borrows: 128 }
  ],
  4: [
    { title: '艺术的故事', borrows: 195 },
    { title: '西方美术史', borrows: 175 },
    { title: '中国绘画史', borrows: 158 },
    { title: '设计心理学', borrows: 146 },
    { title: '美的历程', borrows: 132 }
  ],
  5: [
    { title: '置身事内', borrows: 185 },
    { title: '苏菲的世界', borrows: 165 },
    { title: '理想国', borrows: 152 },
    { title: '查拉图斯特拉', borrows: 138 },
    { title: '道德经', borrows: 125 }
  ]
});

// 折线图相关数据
const allTimeLabels = [
  '2023.5', '2023.6', '2023.7', '2023.8', '2023.9', '2023.10', '2023.11', '2023.12', 
  '2024.1', '2024.2', '2024.3', '2024.4', '2024.5', '2024.6', '2024.7', '2024.8', '2024.9', '2024.10', '2024.11', '2024.12'
];

const lineChartData = {
  1: [300, 280, 310, 290, 330, 320, 350, 340, 370, 360, 390, 380, 410, 400, 430, 420, 450, 440, 470, 490, 450, 550],
  2: [320, 260, 330, 250, 280, 260, 310, 290, 260, 280, 320, 350, 280, 300, 290, 340, 360, 300, 310, 350, 340, 400],
  3: [280, 290, 270, 280, 300, 290, 250, 220, 290, 310, 330, 320, 340, 330, 350, 340, 360, 350, 380, 410, 390, 470],
  4: [250, 260, 240, 250, 270, 260, 280, 270, 220, 280, 200, 290, 210, 200, 220, 210, 230, 320, 350, 380, 360, 440],
  5: [230, 240, 220, 230, 250, 240, 260, 290, 270, 260, 280, 270, 290, 280, 300, 290, 310, 300, 330, 360, 380, 420]
};

const selectedLineCategory = ref('all');
const selectedTimeRange = ref('12');

const filteredLineData = computed(() => {
  // const data = lineChartData[selectedLineCategory.value];
  const range = parseInt(selectedTimeRange.value);
  const startIndex = allTimeLabels.length - range;
  
  if (selectedLineCategory.value === 'all') {
    // Show all categories when "all" is selected
    return {
      labels: allTimeLabels.slice(startIndex),
      datasets: categories.value.map(category => ({
        label: category.name + '类',
        data: lineChartData[category.id].slice(startIndex),
        borderColor: getCategoryColor(category.id),
        backgroundColor: 'rgba(255, 255, 255, 0)',
        fill: false,
        tension: 0.4,
        hidden: false
      }))
    };
  } else {
    // Show single category when specific one is selected
    return {
      labels: allTimeLabels.slice(startIndex),
      datasets: [{
        label: categories.value.find(c => c.id == selectedLineCategory.value)?.name + '类',
        data: lineChartData[selectedLineCategory.value].slice(startIndex),
        borderColor: '#8d6e63',
        backgroundColor: 'rgba(141, 110, 99, 0.1)',
        fill: true,
        tension: 0.4
      }]
    };
  }
});

// Helper function to get consistent colors for categories
function getCategoryColor(categoryId) {
  const colors = ['#ffadd5', '#ffdbdd', '#ffec3d', '#c7ffe7', '#85edff'];
  return colors[(categoryId - 1) % colors.length];
}

const wordCloudData = ref([
  { text: '康熙的红票', value: 120 ,url: '/book/5'},
  { text: '百年孤独', value: 110 ,url: '/book/4'},
  { text: '二战经济学', value: 115 },
  { text: '哈姆雷特', value: 110 },
  { text: '水浒传', value: 95 },
  { text: '新发展常态', value: 110 },
  { text: '当代中国故事', value: 30 },
  { text: '三体', value: 30 },
  { text: '一带一路战略', value: 50 },
  { text: '认知觉醒', value: 95 },
  { text: '杀死一只知更鸟', value: 90 },
  { text: '也许你该找个人聊聊', value: 93 },
  { text: '平凡的世界', value: 103 ,url: '/book/3'},
  { text: '过度焦虑', value: 55 },
  { text: '孤独修心课', value: 60 },
  { text: '亲密关系', value: 40 },
  { text: '追风筝的人', value: 25 },
  { text: '局外人', value: 40 },
  { text: '白夜行', value: 120 },
  { text: '围城', value: 90 },
  { text: '睡觉革命', value: 95 },
  { text: '断舍离', value: 60 },
  { text: '深度工作', value: 30 },
  { text: '万历十五年', value: 40 },
  { text: '大明王朝1566', value: 120 },
  { text: '叫魂', value: 80 },
  { text: '存在与时间', value: 100 },
  { text: '苏菲的世界', value: 90 },
  { text: '有限与无限的游戏', value: 25 },
  { text: '长安的荔枝', value: 80 },
  { text: '苏东坡传', value: 60 },
  { text: '活着', value: 40 },
  { text: '红楼梦', value: 25 },
  { text: '小王子', value: 80 },
  { text: '计算机系统结构', value: 95 ,url:"/book/1" },
  { text: '计算机网络', value: 20 },
  { text: '计算机组成原理', value: 20 },
  { text: '数据结构', value: 100 ,url:'/book/2'},
  { text: '操作系统', value: 30 },
  { text: '中国梦', value: 40 },
  { text: '三天读懂中国经济', value: 30 },
  { text: '当代中国经济', value: 25 },
  { text: '金砖力量', value: 40 },
  { text: '围城', value: 60 },
  { text: '赶时间的人', value: 40 },
  { text: '偶然', value: 55 },
  { text: '人性的弱点', value: 40 },
  { text: '资本论', value: 45 },
  { text: '解忧杂货店', value: 40 },
  { text: '沟通的艺术', value: 50 },
  { text: '麦田里的守望者', value: 65 },
  { text: '云边有个小卖部', value: 60 },
  { text: '置身事内', value: 80 ,url:'/book/6'}
]);

// 图表选项
const barOptions = reactive({
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '借阅数量',
        font: {
          size: 15
        }
      },
      ticks: {
        font: {
          size: 15
        }
      }
    },
    x: {
      title: {
        display: true,
        text: '书籍类别',
        fontSize:15
      },
      ticks: {
        fontSize:15
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      bodyFont: {
        size: 14
      }
    }
  }
});

const pieOptions = reactive({
  responsive: true,
  animation:{
    duration: 0
  },
  plugins: {
    legend: {
      position: 'bottom',
      align: 'center',
      labels: {
        boxWidth:20,
        font: {
          size: 14
        }
      }
    },
    tooltip: {
      bodyFont: {
        size: 14
      }
    }
  }
});

const lineOptions = reactive({
  responsive: true,
  interaction: {
    mode: 'index',
    intersect: false
  },
  scales: {
    y: {
      beginAtZero: false,
      title: {
        display: true,
        text: '借阅数量',
        font: {
          size: 14
        }
      },
      ticks: {
        font: {
          size: 12
        }
      }
    },
    x: {
      title: {
        display: true,
        text: '时间',
        font: {
          size: 14
        }
      },
      ticks: {
        font: {
          size: 12
        }
      },
      padding:{
        top:10
      }
    }
  },
  plugins: {
    legend: {
      position:'top',
      labels: {
        font: {
          size: 15
        },
        // usePointStyle: true//图例使用点样式
      },
      onClick: (e, legendItem, legend) => {
        const index = legendItem.datasetIndex;
        const ci = legend.chart;
        const meta = ci.getDatasetMeta(index);
        
        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
        ci.update();
      }
    },
    tooltip: {
      bodyFont: {
        size: 14
      },
      callbacks: {
        label: function(context) {
          return context.dataset.label + ': ' + context.parsed.y;
        }
      }
    }
  }
});

const selectedCategory = ref(1);
</script>

<style scoped lang="scss">
.book-stats-view {
  max-width: 1100px;
  width: 90%;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
  color: #2c3e50;
  background-color: #f5f9ff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(74, 137, 220, 0.1);

  .page-header {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e6f0fd;

    h1 {
      font-size: 1.8rem;
      font-weight: 600;
      color: #2c3e50;
      margin: 20px 0px;
      background: linear-gradient(135deg, #4a89dc 0%, #3b7dd8 100%);
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #e6f0fd;

    h2 {
      font-size: 1.3rem;
      font-weight: 600;
      color: #4a89dc;
      margin: 0;
    }
  }

  .dual-chart-container {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 1.5rem;

    .pieChart, .barChart {
      background-color: #fff;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(74, 137, 220, 0.1);
      border: 1px solid #e6f0fd;
      
      h3 {
        font-size: 1.1rem;
        color: #4a89dc;
        margin: 0 0 0.8rem;
        text-align: center;
        font-weight: 500;
      }
    }

    .pieChart {
      width: 32%;
    }
    
    .barChart {
      width: 60%;
    }

    @media (max-width: 768px) {
      flex-direction: column;
      
      .pieChart, .barChart {
        width: 100%;
      }
    }
  }

  .chart-container {
    background-color: #fff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(74, 137, 220, 0.1);
    margin-bottom: 1.5rem;
    border: 1px solid #e6f0fd;
  }

  .category-selector {
    select {
      padding: 0.5rem 0.8rem;
      background-color: #e6f0fd;
      border: 1px solid #d4e1f8;
      border-radius: 6px;
      color: #2c3e50;
      font-size: 0.9rem;
      transition: all 0.3s ease;
      
      &:focus {
        outline: none;
        border-color: #4a89dc;
        box-shadow: 0 0 0 2px rgba(74, 137, 220, 0.1);
      }
    }
  }

  .chart-controls {
    display: flex;
    gap: 0.8rem;
    
    .control-select {
      padding: 0.5rem 0.8rem;
      background-color: #e6f0fd;
      border: 1px solid #d4e1f8;
      border-radius: 6px;
      color: #2c3e50;
      font-size: 0.9rem;
      transition: all 0.3s ease;
      
      &:focus {
        outline: none;
        border-color: #4a89dc;
      }
    }
  }

  .ranking-table {
    background-color: #fff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(74, 137, 220, 0.1);
    margin-bottom: 1.5rem;
    border: 1px solid #e6f0fd;
    overflow-x: auto;

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 500px;

      th, td {
        padding: 0.8rem;
        text-align: center;
        border-bottom: 1px solid #e6f0fd;
        font-size: 0.9rem;
      }

      th {
        background-color: #f5f9ff;
        color: #4a89dc;
        font-weight: 500;
      }

      tr:hover {
        background-color: #f5f9ff;
      }
    }
  }

  .wordcloud-container {
    background-color: #fff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(74, 137, 220, 0.1);
    border: 1px solid #e6f0fd;
    height: 400px;
  }

  /* 响应式设计 */
  @media (max-width: 768px) {
    width: 95%;
    padding: 1rem;
    
    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.8rem;
    }
    
    .chart-controls {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .ranking-table {
      padding: 0.5rem;
      
      table {
        th, td {
          padding: 0.6rem;
        }
      }
    }
    
    .wordcloud-container {
      height: 300px;
    }
  }
}
</style>