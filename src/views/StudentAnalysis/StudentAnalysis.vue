<script setup>
import { ref, provide } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { logout } from '@/api/users'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'

const router = useRouter()
const tableData = ref([
  {
    date: '2025-01-01',
    name: '课程主题1',
    address: '科目1',
    key: 1
  },
  {
    date: '2025-01-02',
    name: '课程主题2',
    address: '科目2',
    key: 2
  },
  {
    date: '2025-01-01',
    name: '课程主题3',
    address: '科目3',
    key: 3
  },
  {
    date: '2025-01-02',
    name: '课程主题4',
    address: '科目4',
    key: 4
  },
  {
    date: '2025-01-02',
    name: '课程主题5',
    address: '科目5',
    key: 5
  },
  {
    date: '2025-01-01',
    name: '课程主题6',
    address: '科目6',
    key: 6
  },
  {
    date: '2025-01-02',
    name: '课程主题7',
    address: '科目7',
    key: 7
  }
])

const selectedRowKey = ref(null)

const option = ref({
  title: {
    text: '学生作业正确率',
    left: 'center',
    textStyle: {
      color: '#000',
      fontSize: 18
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b} : {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: ['90-100', '80-90', '70-80', '60-70', '60以下']
  },
  series: [
    {
      name: '学生作业正确率',
      type: 'pie',
      radius: '55%',
      center: ['50%', '60%'],
      data: [
        { value: 335, name: '90-100' },
        { value: 310, name: '80-90' },
        { value: 234, name: '70-80' },
        { value: 135, name: '60-70' },
        { value: 1548, name: '60以下' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent])
provide(THEME_KEY, 'light') // 设置主题为 'light'

const handleRowClick = row => {
  selectedRowKey.value = row.key
  ElMessageBox.alert(`选中了行: ${row.name}`, '提示', {
    confirmButtonText: '确定',
    type: 'info'
  })
}

const getRowClassName = ({ row }) => {
  return row.key === selectedRowKey.value ? 'selected-row' : ''
}
</script>

<template>
  <div class="card-container">
    <el-card class="card1">
      <v-chart class="chart" :option="option" autoresize />
    </el-card>
    <el-card class="card2">
      <el-table
        :data="tableData"
        border
        style="width: 100%; height: 100%;"
        v-infinite-scroll="loadMoreData"
        @row-click="handleRowClick"
        :row-class-name="getRowClassName"
        :highlight-current-row="true"
        :current-row-key="selectedRowKey"
      >
        <el-table-column prop="date" label="日期" width="auto" align="center" />
        <el-table-column prop="name" label="课程主题" width="auto" align="center" />
        <el-table-column prop="address" label="科目" width="auto" align="center" />
      </el-table>
    </el-card>
    <el-card class="card3" style="flex: 100%; margin: 10px; height: 50vh; width: 98vw;">
      <!-- 在这里添加 card3 的内容 -->
    </el-card>
  </div>
</template>

<style scoped>
.card-container {
  margin-right: 10px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.card1,
.card2 {
  flex: 1;
  margin: 10px;
  height: 50vh;
  width: 30vw;
  overflow: auto; /* 允许内容滚动 */
}

.card2 {
  scrollbar-width: none; /* 隐藏滚动条（Firefox） */
  -ms-overflow-style: none; /* 隐藏滚动条（IE 10+） */
}

.card2::-webkit-scrollbar {
  display: none; /* 隐藏滚动条（Chrome, Safari, Opera） */
}

.chart {
  height: 40vh;
  width: 75vh;
}

.el-table .selected-row {
  background-color: #e6f7ff; /* 浅蓝色 */
}
</style>