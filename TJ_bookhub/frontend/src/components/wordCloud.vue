<!-- <template>
    <div ref="wordCloudContainer" class="word-cloud-container"></div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch,defineProps } from 'vue';
  import * as d3 from 'd3';
  import cloud from 'd3-cloud';
  
  const props = defineProps({
    words: {
      type: Array,
      default: () => [
        { text: '默认', value: 100 },
        { text: '数据', value: 80 }
      ]
    }
  });
  
  const wordCloudContainer = ref(null);
  
  const drawWordCloud = () => {
    if (!wordCloudContainer.value || !props.words.length) return;
    
    // 清除现有内容
    d3.select(wordCloudContainer.value).selectAll("*").remove();
    
    const width = wordCloudContainer.value.clientWidth;
    const height = wordCloudContainer.value.clientHeight;
    // const height = 400;
    
    // 设置词云布局
    const layout = cloud()
      .size([width, height])
      .words(props.words.map(d => ({
        text: d.text,
        size: d.value * 0.5
      })))
      .padding(8.5)
      .rotate(() => (~~(Math.random() * 11) - 5))
      .font("Noto Serif SC")
      .fontSize(d => d.size)
      .on("end", draw);
    
    layout.start();
    
    function draw(words) {
      d3.select(wordCloudContainer.value)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width/2},${height/2})`)
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", d => `${d.size}px`)
        .style("font-family", "Noto Serif SC")
        .style("fill", () => {
          var letters = "0123456789ABCDEF";
          var color = "#";
          for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
          }
          return color;
        })
        .attr("text-anchor", "middle")
        .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
        .text(d => d.text);
    }
  };
  
  onMounted(() => {
    drawWordCloud();
  });
  
  watch(() => props.words, () => {
    drawWordCloud();
  }, { deep: true });
  </script>
  
  <style scoped>
  .word-cloud-container {
    width: 100%;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style> -->

  <template>
    <div ref="wordCloudContainer" class="word-cloud-container"></div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, defineProps } from 'vue';
  import * as d3 from 'd3';
  import cloud from 'd3-cloud';
  
  const props = defineProps({
    words: {
      type: Array,
      default: () => [
        { text: '默认', value: 100, url: '#' },
        { text: '数据', value: 80, url: '#' }
      ]
    }
  });
  
  const wordCloudContainer = ref(null);
  
  const drawWordCloud = () => {
    if (!wordCloudContainer.value || !props.words.length) return;
    
    // 清除现有内容
    d3.select(wordCloudContainer.value).selectAll("*").remove();
    
    const width = wordCloudContainer.value.clientWidth;
    const height = wordCloudContainer.value.clientHeight;
    
    // 设置词云布局
    const layout = cloud()
      .size([width, height])
      .words(props.words.map(d => ({
        text: d.text,
        size: d.value * 0.5,
        url: d.url || '#' // 默认跳转链接
      })))
      .padding(8.5)
      .rotate(() => (~~(Math.random() * 11) - 5))
      .font("Noto Serif SC")
      .fontSize(d => d.size)
      .on("end", draw);
    
    layout.start();
    
    function draw(words) {
      const svg = d3.select(wordCloudContainer.value)
        .append("svg")
        .attr("width", width)
        .attr("height", height);
      
      const g = svg.append("g")
        .attr("transform", `translate(${width/2},${height/2})`);
      
      const text = g.selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", d => `${d.size}px`)
        .style("font-family", "Noto Serif SC")
        .style("fill", () => {
          var letters = "0123456789ABCDEF";
          var color = "#";
          for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
          }
          return color;
        })
        .style("cursor", "pointer")
        .style("transition", "all 0.3s ease")
        .attr("text-anchor", "middle")
        .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
        .text(d => d.text)
        // 鼠标悬停效果
        .on("mouseover", function(event, d) {
          d3.select(this)
            .style("opacity", 1)
            .style("font-weight", "bold")
            .style("font-size", `${d.size * 1.2}px`);
          
          // 其他文字模糊处理
          text.style("opacity", 0.3);
          d3.select(this).style("opacity", 1);
        })
        // 鼠标移出效果
        .on("mouseout", function() {
          text.style("opacity", 1)
            .style("font-weight", "normal")
            .style("font-size", d => `${d.size}px`);
        })
        // 点击跳转
        .on("click", function(event, d) {
          window.open(d.url, '_blank');
        });
    }
  };
  
  onMounted(() => {
    drawWordCloud();
  });
  
  watch(() => props.words, () => {
    drawWordCloud();
  }, { deep: true });
  </script>
  
  <style scoped>
  .word-cloud-container {
    width: 100%;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style>