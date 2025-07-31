<template>
  <div class="history-container">
    <div class="page-header">
      <h1>历史记录</h1>
      <p>查看和管理已生成的实验报告</p>
    </div>

    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索项目..."
          clearable
          style="width: 300px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 150px">
          <el-option label="全部" value="" />
          <el-option label="已完成" value="completed" />
          <el-option label="进行中" value="generating" />
          <el-option label="失败" value="failed" />
          <el-option label="草稿" value="draft" />
        </el-select>

        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 240px"
        />
      </div>
      
      <div class="toolbar-right">
        <el-button @click="exportHistory">
          <el-icon><Download /></el-icon>
          导出记录
        </el-button>
        <el-button type="danger" @click="clearHistory" :disabled="filteredProjects.length === 0">
          <el-icon><Delete /></el-icon>
          清空历史
        </el-button>
      </div>
    </div>

    <!-- 视图切换 -->
    <div class="view-switcher">
      <el-radio-group v-model="viewMode" size="small">
        <el-radio-button label="list">列表视图</el-radio-button>
        <el-radio-button label="grid">网格视图</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 项目列表 -->
    <div v-if="viewMode === 'list'" class="projects-list">
      <el-table
        :data="paginatedProjects"
        style="width: 100%"
        @row-click="viewProject"
        row-class-name="project-row"
      >
        <el-table-column prop="name" label="项目名称" min-width="200">
          <template #default="{ row }">
            <div class="project-name-cell">
              <el-icon size="16" :color="getStatusColor(row.status)">
                <component :is="getStatusIcon(row.status)" />
              </el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="description" label="描述" min-width="250" show-overflow-tooltip />
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="format" label="格式" width="100">
          <template #default="{ row }">
            <el-tag size="small" type="info">{{ row.format || 'Markdown' }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="fileCount" label="文件数" width="80" align="center" />
        
        <el-table-column prop="updatedAt" label="更新时间" width="120">
          <template #default="{ row }">
            {{ formatDate(row.updatedAt) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button text size="small" @click.stop="viewProject(row)">
                <el-icon><View /></el-icon>
              </el-button>
              <el-button text size="small" @click.stop="downloadProject(row)" :disabled="row.status !== 'completed'">
                <el-icon><Download /></el-icon>
              </el-button>
              <el-button text size="small" @click.stop="duplicateProject(row)">
                <el-icon><CopyDocument /></el-icon>
              </el-button>
              <el-dropdown @command="handleProjectAction" trigger="click">
                <el-button text size="small" @click.stop>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ action: 'edit', project: row }">编辑</el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'regenerate', project: row }">重新生成</el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'export', project: row }">导出</el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'delete', project: row }" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 项目网格 -->
    <div v-else class="projects-grid">
      <div
        v-for="project in paginatedProjects"
        :key="project.id"
        class="project-card fluent-card"
        @click="viewProject(project)"
      >
        <div class="card-header">
          <div class="project-status">
            <el-icon size="16" :color="getStatusColor(project.status)">
              <component :is="getStatusIcon(project.status)" />
            </el-icon>
            <el-tag :type="getStatusTagType(project.status)" size="small">
              {{ getStatusLabel(project.status) }}
            </el-tag>
          </div>
          <div class="card-actions">
            <el-dropdown @command="handleProjectAction" trigger="click">
              <el-button text size="small" @click.stop>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="{ action: 'edit', project }">编辑</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'regenerate', project }">重新生成</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'export', project }">导出</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'delete', project }" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="card-content">
          <h3 class="project-title">{{ project.name }}</h3>
          <p class="project-description">{{ project.description }}</p>
          
          <div class="project-meta">
            <div class="meta-item">
              <el-icon size="14"><Files /></el-icon>
              <span>{{ project.fileCount }} 个文件</span>
            </div>
            <div class="meta-item">
              <el-icon size="14"><Calendar /></el-icon>
              <span>{{ formatDate(project.updatedAt) }}</span>
            </div>
            <div class="meta-item" v-if="project.format">
              <el-icon size="14"><Document /></el-icon>
              <span>{{ project.format }}</span>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <el-button text size="small" @click.stop="viewProject(project)">
            <el-icon><View /></el-icon>
            查看
          </el-button>
          <el-button text size="small" @click.stop="downloadProject(project)" :disabled="project.status !== 'completed'">
            <el-icon><Download /></el-icon>
            下载
          </el-button>
          <el-button text size="small" @click.stop="duplicateProject(project)">
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredProjects.length === 0" class="empty-state">
      <el-icon size="48" color="#8a8886"><Clock /></el-icon>
      <p>{{ searchKeyword ? '未找到匹配的项目' : '暂无历史记录' }}</p>
      <el-button type="primary" @click="$router.push('/upload')">
        创建第一个项目
      </el-button>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="filteredProjects.length > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="filteredProjects.length"
        layout="total, sizes, prev, pager, next, jumper"
        background
      />
    </div>

    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedProject?.name"
      width="80%"
      center
    >
      <div v-if="selectedProject" class="project-detail">
        <div class="detail-header">
          <div class="project-info">
            <div class="info-row">
              <span class="label">状态:</span>
              <el-tag :type="getStatusTagType(selectedProject.status)">
                {{ getStatusLabel(selectedProject.status) }}
              </el-tag>
            </div>
            <div class="info-row">
              <span class="label">格式:</span>
              <span>{{ selectedProject.format || 'Markdown' }}</span>
            </div>
            <div class="info-row">
              <span class="label">文件数:</span>
              <span>{{ selectedProject.fileCount }}</span>
            </div>
            <div class="info-row">
              <span class="label">创建时间:</span>
              <span>{{ formatDateTime(selectedProject.createdAt) }}</span>
            </div>
            <div class="info-row">
              <span class="label">更新时间:</span>
              <span>{{ formatDateTime(selectedProject.updatedAt) }}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-content">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="项目描述" name="description">
              <div class="description-content">
                <p>{{ selectedProject.description || '暂无描述' }}</p>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="文件列表" name="files">
              <div class="files-content">
                <div v-if="selectedProject.files && selectedProject.files.length > 0" class="file-list">
                  <div
                    v-for="file in selectedProject.files"
                    :key="file.name"
                    class="file-item"
                  >
                    <el-icon size="16" :color="getFileIconColor(file.type)">
                      <component :is="getFileIcon(file.type)" />
                    </el-icon>
                    <span class="file-name">{{ file.name }}</span>
                    <span class="file-size">{{ formatFileSize(file.size) }}</span>
                  </div>
                </div>
                <div v-else class="no-files">
                  <p>暂无文件信息</p>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="生成日志" name="logs" v-if="selectedProject.logs">
              <div class="logs-content">
                <pre>{{ selectedProject.logs }}</pre>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="downloadProject(selectedProject)" :disabled="selectedProject?.status !== 'completed'">
          下载报告
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const searchKeyword = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const viewMode = ref('list')
const currentPage = ref(1)
const pageSize = ref(20)
const detailDialogVisible = ref(false)
const selectedProject = ref(null)
const activeTab = ref('description')

// 模拟项目数据
const projects = ref([
  {
    id: '1',
    name: '数据结构实验报告',
    description: '链表、栈、队列的实现与应用分析',
    status: 'completed',
    format: 'Markdown',
    fileCount: 5,
    createdAt: new Date('2024-01-15T10:30:00'),
    updatedAt: new Date('2024-01-15T14:20:00'),
    files: [
      { name: 'main.py', type: 'text/x-python', size: 2048 },
      { name: 'data_structures.py', type: 'text/x-python', size: 4096 },
      { name: 'test_results.png', type: 'image/png', size: 1024000 }
    ],
    logs: '2024-01-15 14:20:00 - 报告生成完成\n2024-01-15 14:18:00 - 开始格式转换\n2024-01-15 14:15:00 - AI 生成完成'
  },
  {
    id: '2',
    name: '机器学习实验',
    description: '线性回归模型的实现与性能分析',
    status: 'completed',
    format: 'LaTeX',
    fileCount: 8,
    createdAt: new Date('2024-01-14T09:15:00'),
    updatedAt: new Date('2024-01-14T16:45:00'),
    files: [
      { name: 'regression.py', type: 'text/x-python', size: 3072 },
      { name: 'dataset.csv', type: 'text/csv', size: 512000 },
      { name: 'results.png', type: 'image/png', size: 2048000 }
    ]
  },
  {
    id: '3',
    name: '网络编程实验',
    description: 'TCP/UDP 通信协议的实现与测试',
    status: 'generating',
    format: 'Word',
    fileCount: 3,
    createdAt: new Date('2024-01-13T15:20:00'),
    updatedAt: new Date('2024-01-13T15:25:00'),
    files: [
      { name: 'tcp_server.py', type: 'text/x-python', size: 1536 },
      { name: 'udp_client.py', type: 'text/x-python', size: 1024 }
    ]
  },
  {
    id: '4',
    name: '算法分析报告',
    description: '排序算法的时间复杂度分析',
    status: 'failed',
    format: 'Markdown',
    fileCount: 4,
    createdAt: new Date('2024-01-12T11:00:00'),
    updatedAt: new Date('2024-01-12T11:30:00'),
    files: [
      { name: 'sorting.py', type: 'text/x-python', size: 2560 },
      { name: 'benchmark.py', type: 'text/x-python', size: 1792 }
    ]
  },
  {
    id: '5',
    name: '数据库设计文档',
    description: '学生管理系统数据库设计',
    status: 'draft',
    format: 'Markdown',
    fileCount: 2,
    createdAt: new Date('2024-01-11T14:30:00'),
    updatedAt: new Date('2024-01-11T14:35:00'),
    files: [
      { name: 'schema.sql', type: 'text/plain', size: 4096 },
      { name: 'er_diagram.png', type: 'image/png', size: 1536000 }
    ]
  }
])

// 计算属性
const filteredProjects = computed(() => {
  let result = projects.value

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(project =>
      project.name.toLowerCase().includes(keyword) ||
      project.description.toLowerCase().includes(keyword)
    )
  }

  // 状态筛选
  if (filterStatus.value) {
    result = result.filter(project => project.status === filterStatus.value)
  }

  // 日期范围筛选
  if (dateRange.value && dateRange.value.length === 2) {
    const [startDate, endDate] = dateRange.value
    result = result.filter(project => {
      const projectDate = project.updatedAt.toISOString().split('T')[0]
      return projectDate >= startDate && projectDate <= endDate
    })
  }

  // 按更新时间倒序排列
  return result.sort((a, b) => b.updatedAt - a.updatedAt)
})

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredProjects.value.slice(start, end)
})

// 生命周期
onMounted(() => {
  // 初始化操作
})

// 方法
const getStatusIcon = (status) => {
  const iconMap = {
    completed: 'CircleCheck',
    generating: 'Loading',
    failed: 'CircleClose',
    draft: 'Edit'
  }
  return iconMap[status] || 'Document'
}

const getStatusColor = (status) => {
  const colorMap = {
    completed: '#107c10',
    generating: '#ff8c00',
    failed: '#d13438',
    draft: '#8a8886'
  }
  return colorMap[status] || '#605e5c'
}

const getStatusLabel = (status) => {
  const labelMap = {
    completed: '已完成',
    generating: '生成中',
    failed: '失败',
    draft: '草稿'
  }
  return labelMap[status] || '未知'
}

const getStatusTagType = (status) => {
  const typeMap = {
    completed: 'success',
    generating: 'warning',
    failed: 'danger',
    draft: 'info'
  }
  return typeMap[status] || 'info'
}

const getFileIcon = (fileType) => {
  if (fileType.startsWith('image/')) return 'Picture'
  if (fileType.includes('python')) return 'Document'
  if (fileType.includes('csv')) return 'Grid'
  return 'Document'
}

const getFileIconColor = (fileType) => {
  if (fileType.startsWith('image/')) return '#ff8c00'
  if (fileType.includes('python')) return '#3776ab'
  if (fileType.includes('csv')) return '#107c10'
  return '#605e5c'
}

const viewProject = (project) => {
  selectedProject.value = project
  detailDialogVisible.value = true
}

const downloadProject = (project) => {
  if (project.status !== 'completed') {
    ElMessage.warning('只能下载已完成的项目')
    return
  }
  
  // 模拟下载
  ElMessage.success(`正在下载 ${project.name}`)
}

const duplicateProject = (project) => {
  const newProject = {
    ...project,
    id: `${project.id}_copy_${Date.now()}`,
    name: `${project.name} (副本)`,
    status: 'draft',
    createdAt: new Date(),
    updatedAt: new Date()
  }
  
  projects.value.unshift(newProject)
  ElMessage.success('项目复制成功')
}

const handleProjectAction = ({ action, project }) => {
  switch (action) {
    case 'edit':
      editProject(project)
      break
    case 'regenerate':
      regenerateProject(project)
      break
    case 'export':
      exportProject(project)
      break
    case 'delete':
      deleteProject(project)
      break
  }
}

const editProject = (project) => {
  router.push({
    name: 'Generate',
    query: {
      projectId: project.id
    }
  })
}

const regenerateProject = (project) => {
  ElMessage.info('重新生成功能待实现')
}

const exportProject = (project) => {
  ElMessage.info('导出功能待实现')
}

const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm(`确定要删除项目 "${project.name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = projects.value.findIndex(p => p.id === project.id)
    if (index > -1) {
      projects.value.splice(index, 1)
      ElMessage.success('项目删除成功')
    }
  } catch {
    // 用户取消操作
  }
}

const exportHistory = () => {
  ElMessage.info('导出历史记录功能待实现')
}

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有历史记录吗？此操作不可撤销。', '确认清空', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    projects.value = []
    ElMessage.success('历史记录已清空')
  } catch {
    // 用户取消操作
  }
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

const formatDateTime = (date) => {
  return date.toLocaleString('zh-CN')
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.history-container {
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.page-header p {
  color: var(--color-text-secondary);
  margin: 0;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  gap: var(--spacing-md);
}

.toolbar-left {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  flex-wrap: wrap;
}

.view-switcher {
  margin-bottom: var(--spacing-lg);
}

.projects-list {
  margin-bottom: var(--spacing-lg);
}

.project-name-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.table-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.project-card {
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.project-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.project-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.card-content {
  margin-bottom: var(--spacing-md);
}

.project-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.project-description {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 var(--spacing-md) 0;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.card-footer {
  display: flex;
  gap: var(--spacing-sm);
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--spacing-md);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xxl);
  color: var(--color-text-secondary);
}

.empty-state p {
  margin: var(--spacing-md) 0 var(--spacing-lg) 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-xl);
}

.project-detail {
  padding: var(--spacing-md);
}

.detail-header {
  margin-bottom: var(--spacing-lg);
}

.project-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
}

.label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.description-content {
  padding: var(--spacing-md);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-medium);
}

.files-content {
  max-height: 300px;
  overflow-y: auto;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.file-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-medium);
}

.file-name {
  flex: 1;
  font-size: 14px;
}

.file-size {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.no-files {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.logs-content pre {
  background-color: var(--color-bg-tertiary);
  padding: var(--spacing-md);
  border-radius: var(--radius-medium);
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  line-height: 1.5;
  max-height: 300px;
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-container {
    padding: var(--spacing-lg);
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .toolbar-left {
    flex-direction: column;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .project-info {
    grid-template-columns: 1fr;
  }
  
  .card-footer {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
}
</style>
