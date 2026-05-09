<template>
  <div class="home-container">
    <!-- 背景装饰 -->
    <div class="bg-decor">
      <div class="bg-decor-circle bg-decor-circle--1" />
      <div class="bg-decor-circle bg-decor-circle--2" />
    </div>

    <!-- 头部 -->
    <header class="header">
      <div class="header-accent" />
      <h1 class="brand-title">Planner</h1>
      <p class="brand-subtitle">智能旅行助手</p>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 左侧：表单输入 -->
      <el-card class="form-card" shadow="never">
        <template #header>
          <div class="card-header">
            <div class="card-header-icon">
              <el-icon :size="16"><Location /></el-icon>
            </div>
            <span class="card-header-text">行程规划</span>
          </div>
        </template>

        <el-form :model="formData" label-position="top" @submit.prevent="handleSubmit" class="trip-form">
          <!-- 城市和日期 -->
          <div class="form-section">
            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
                <el-form-item label="目的地城市" required>
                  <el-input
                    v-model="formData.city"
                    placeholder="例如：北京、上海、成都"
                    size="large"
                  >
                    <template #prefix>
                      <el-icon><Location /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="6">
                <el-form-item label="出发日期" required>
                  <el-date-picker
                    v-model="formData.start_date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                    value-format="YYYY-MM-DD"
                    size="large"
                  />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="6">
                <el-form-item label="返回日期" required>
                  <el-date-picker
                    v-model="formData.end_date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                    value-format="YYYY-MM-DD"
                    size="large"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 旅行天数显示 -->
            <el-alert
              v-if="travelDays > 0"
              :title="`共 ${travelDays} 天行程`"
              type="info"
              :closable="false"
              show-icon
              class="days-alert"
            />
          </div>

          <div class="section-divider" />

          <!-- 偏好设置 -->
          <div class="form-section">
            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
                <el-form-item label="交通方式">
                  <el-select v-model="formData.transportation" style="width: 100%" size="large">
                    <el-option label="🚇 公共交通" value="公共交通" />
                    <el-option label="🚗 自驾" value="自驾" />
                    <el-option label="🚶 步行" value="步行" />
                    <el-option label="🔀 混合" value="混合" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="住宿偏好">
                  <el-select v-model="formData.accommodation" style="width: 100%" size="large">
                    <el-option label="💰 经济型酒店" value="经济型酒店" />
                    <el-option label="🏨 舒适型酒店" value="舒适型酒店" />
                    <el-option label="⭐ 豪华酒店" value="豪华酒店" />
                    <el-option label="🏡 民宿" value="民宿" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <div class="section-divider" />

          <!-- 旅行偏好 -->
          <div class="form-section">
            <el-form-item label="旅行偏好">
              <el-checkbox-group v-model="formData.preferences" class="preference-group">
                <el-checkbox label="历史文化" border>🏛️ 历史文化</el-checkbox>
                <el-checkbox label="自然风光" border>🏞️ 自然风光</el-checkbox>
                <el-checkbox label="美食" border>🍜 美食</el-checkbox>
                <el-checkbox label="购物" border>🛍️ 购物</el-checkbox>
                <el-checkbox label="艺术" border>🎨 艺术</el-checkbox>
                <el-checkbox label="休闲" border>☕ 休闲</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </div>

          <div class="section-divider" />

          <!-- 额外要求 -->
          <div class="form-section">
            <el-form-item label="额外要求">
              <el-input
                v-model="formData.free_text_input"
                type="textarea"
                :rows="3"
                placeholder="请输入您的额外要求，例如：想去看升旗、需要无障碍设施..."
              />
            </el-form-item>
          </div>

          <div class="section-divider" />

          <!-- 预算设置 -->
          <div class="form-section">
            <el-form-item label="预算范围">
              <div class="budget-slider-container">
                <el-slider
                  v-model="formData.budget"
                  range
                  :min="500"
                  :max="10000"
                  :step="100"
                  :format-tooltip="(val: number) => `¥${val}`"
                />
                <div class="budget-display">
                  <el-tag type="success" effect="light" size="large">¥{{ formData.budget[0] }}</el-tag>
                  <span class="budget-separator">—</span>
                  <el-tag type="warning" effect="light" size="large">¥{{ formData.budget[1] }}</el-tag>
                  <span class="budget-label">{{ budgetLevel }}</span>
                </div>
              </div>
            </el-form-item>
          </div>

          <div class="section-divider" />

          <!-- LLM 选择 -->
          <div class="form-section">
            <el-form-item label="AI 模型">
              <el-radio-group v-model="formData.llm_provider" class="model-selector">
                <el-radio label="deepseek" border size="large">DeepSeek</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>

          <!-- 提交按钮 -->
          <div class="form-section submit-section">
            <el-form-item>
              <el-button
                v-if="!isLoading"
                type="primary"
                size="large"
                @click="handleSubmit"
                class="submit-btn"
              >
                <el-icon class="btn-icon"><Promotion /></el-icon>
                <span>开始规划行程</span>
              </el-button>
              <el-button
                v-else
                plain
                size="large"
                @click="handleStop"
                class="stop-btn"
              >
                <el-icon class="btn-icon"><Close /></el-icon>
                <span>终止规划</span>
              </el-button>
            </el-form-item>
          </div>
        </el-form>
      </el-card>

      <!-- 右侧：执行进度 -->
      <div class="right-column">
        <el-card v-if="isLoading || steps.length > 0" class="progress-card" shadow="never">
          <template #header>
            <div class="card-header">
              <div class="card-header-icon progress-icon">
                <el-icon :size="16"><Loading /></el-icon>
              </div>
              <span class="card-header-text">Agent 执行进度</span>
            </div>
          </template>

          <el-timeline class="progress-timeline">
            <el-timeline-item
              v-for="(step, index) in steps"
              :key="index"
              :type="getStepType(step.status)"
              :title="step.node"
            >
              <div class="step-content">
                <div class="step-header">
                  <span class="step-name">{{ getNodeName(step.node) }}</span>
                  <el-tag :type="getStepType(step.status)" size="small" effect="light" class="step-tag">
                    {{ step.status }}
                  </el-tag>
                </div>
                <div v-if="step.message" class="step-message">
                  {{ step.message }}
                </div>
                <div v-if="step.error" class="step-error">
                  <el-icon><WarningFilled /></el-icon>
                  {{ step.error }}
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>

          <!-- 当前状态提示 -->
          <div v-if="isLoading && currentMessage" class="current-status">
            <el-icon class="is-loading status-icon"><Loading /></el-icon>
            <span>{{ currentMessage }}</span>
          </div>

          <el-progress
            v-if="isLoading"
            :percentage="progress"
            :status="progressStatus"
            :stroke-width="6"
            class="progress-bar"
          />
        </el-card>

        <!-- 空状态引导 -->
        <div v-else class="empty-guide">
          <div class="empty-guide-icon">
            <el-icon :size="28"><Promotion /></el-icon>
          </div>
          <p class="empty-guide-title">开始你的旅程</p>
          <p class="empty-guide-desc">填写左侧表单，AI 将为你规划完美行程</p>
        </div>
      </div>
    </main>

    <!-- 底部链接 -->
    <footer class="footer">
      <el-button text @click="$router.push('/chat')" class="footer-link">
        <el-icon><ChatDotRound /></el-icon>
        <span>切换到对话模式</span>
      </el-button>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Location, Promotion, Loading, WarningFilled, ChatDotRound, Close } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { useTripStore } from '@/stores/trip'
import type { TripRequest, AgentStep } from '@/types'

const router = useRouter()
const tripStore = useTripStore()

const formData = ref<TripRequest>({
  city: '',
  start_date: '',
  end_date: '',
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: '',
  llm_provider: 'deepseek',
  budget: [1000, 3000] as [number, number]
})

const isLoading = ref(false)
const isStopped = ref(false)
const steps = ref<AgentStep[]>([])
const progress = ref(0)
const currentStep = ref('')
const currentMessage = ref('')
const abortController = ref<AbortController | null>(null)

const travelDays = computed(() => {
  if (formData.value.start_date && formData.value.end_date) {
    const start = dayjs(formData.value.start_date)
    const end = dayjs(formData.value.end_date)
    const days = end.diff(start, 'day') + 1
    return days > 0 ? days : 0
  }
  return 0
})

const budgetLevel = computed(() => {
  const max = formData.value.budget[1]
  if (max <= 1500) return '经济出行'
  if (max <= 3000) return '舒适旅行'
  if (max <= 5000) return '品质游玩'
  if (max <= 8000) return '高端体验'
  return '奢华之旅'
})

watch(travelDays, (days) => {
  formData.value.travel_days = days
})

const progressStatus = computed(() => {
  if (progress.value >= 100) return 'success'
  if (progress.value >= 80) return 'warning'
  return ''
})

function getStepType(status: string): 'primary' | 'success' | 'danger' | 'info' {
  switch (status) {
    case 'completed': return 'success'
    case 'running': return 'primary'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

function getNodeName(node: string): string {
  const names: Record<string, string> = {
    'init': '🚀 初始化',
    'poi_search': '🔍 景点搜索',
    'weather': '🌤️ 天气查询',
    'hotel': '🏨 酒店推荐',
    'planner': '📋 行程规划',
    'human_review': '👤 等待审核',
    'complete': '✅ 完成',
    'stopped': '⏹️ 已终止',
    'error': '❌ 错误'
  }
  return names[node] || node
}

async function handleSubmit() {
  if (!formData.value.city || !formData.value.start_date || !formData.value.end_date) {
    ElMessage.warning('请填写完整信息')
    return
  }

  isLoading.value = true
  isStopped.value = false
  steps.value = []
  progress.value = 0
  currentStep.value = '正在准备...'
  currentMessage.value = '正在初始化...'

  const sessionId = `session_${Date.now()}`
  tripStore.setSessionId(sessionId)

  abortController.value = new AbortController()

  try {
    const baseUrl = import.meta.env.DEV ? '' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
    const response = await fetch(`${baseUrl}/api/trip/plan/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...formData.value, session_id: sessionId }),
      signal: abortController.value.signal
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('无法读取响应流')
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      if (isStopped.value) {
        reader.cancel()
        break
      }

      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            handleStreamEvent(data)
          } catch (e) {
            console.error('Failed to parse SSE data:', e)
          }
        }
      }
    }

    if (buffer.startsWith('data: ')) {
      try {
        const data = JSON.parse(buffer.slice(6))
        handleStreamEvent(data)
      } catch (e) {
        console.error('Failed to parse remaining SSE data:', e)
      }
    }

  } catch (error: any) {
    if (error.name === 'AbortError') {
      ElMessage.info('已终止规划')
      steps.value.push({ node: 'stopped', status: 'failed', message: '用户终止' })
    } else {
      console.error('[Home] 请求错误:', error)
      ElMessage.error(error.message || '请求失败')
      tripStore.addError(error.message)
      steps.value.push({ node: 'error', status: 'failed', error: error.message })
    }
  } finally {
    isLoading.value = false
    abortController.value = null
  }
}

function handleStreamEvent(data: any) {
  console.log('[Home] 收到事件:', data)

  if (data.message) {
    currentMessage.value = data.message
  }

  if (data.step) {
    progress.value = Math.min(data.step * 10, 90)
  }

  if (data.node) {
    const existingIndex = steps.value.findIndex(s => s.node === data.node)
    const step: AgentStep = {
      node: data.node,
      status: data.status,
      message: data.message,
      data: data.data
    }

    if (existingIndex >= 0) {
      steps.value[existingIndex] = step
    } else {
      steps.value.push(step)
    }
  }

  if (data.node === 'complete' && data.status === 'completed') {
    progress.value = 100

    if (data.data?.itinerary) {
      tripStore.setTripPlan(data.data.itinerary as any)
      tripStore.setStatus('completed')
      tripStore.setNeedHumanReview(false)

      ElMessage.success('行程规划完成！')

      setTimeout(() => {
        router.push('/result')
      }, 500)
    }
  }

  if (data.status === 'failed' || data.node === 'error') {
    ElMessage.error(data.message || '规划失败')
  }
}

function handleStop() {
  if (abortController.value) {
    isStopped.value = true
    abortController.value.abort()
  }
}
</script>

<style scoped>
/* ============================================
   Container & Background
   ============================================ */
.home-container {
  min-height: 100vh;
  background: #FAFAFA;
  padding: 88px 32px 64px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.bg-decor {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.bg-decor-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
}

.bg-decor-circle--1 {
  width: 640px;
  height: 640px;
  background: radial-gradient(circle, #7B61FF 0%, transparent 70%);
  top: -280px;
  right: -180px;
}

.bg-decor-circle--2 {
  width: 480px;
  height: 480px;
  background: radial-gradient(circle, #9BA5B3 0%, transparent 70%);
  bottom: -160px;
  left: -120px;
}

/* ============================================
   Header
   ============================================ */
.header {
  text-align: center;
  margin-bottom: 72px;
  position: relative;
  z-index: 1;
  animation: fadeUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.header-accent {
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #7B61FF, #4F6EF7);
  border-radius: 2px;
  margin: 0 auto 24px;
}

.brand-title {
  font-size: 52px;
  font-weight: 700;
  color: #0B0C0E;
  letter-spacing: -0.04em;
  line-height: 1;
  margin: 0 0 12px;
  background: linear-gradient(135deg, #0B0C0E 0%, #2D2F33 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 14px;
  color: #6B7685;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0;
}

/* ============================================
   Main Content Layout
   ============================================ */
.main-content {
  max-width: 1120px;
  width: 100%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 32px;
  flex: 1;
  position: relative;
  z-index: 1;
  animation: fadeUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.1s both;
}

.right-column {
  display: flex;
  flex-direction: column;
}

/* ============================================
   Cards
   ============================================ */
.form-card,
.progress-card {
  border-radius: 20px;
  border: 1px solid #EBECEE;
  background: #FFFFFF;
  transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-card:hover {
  box-shadow:
    0 0 0 1px rgba(11, 12, 14, 0.04),
    0 4px 16px rgba(11, 12, 14, 0.04),
    0 16px 40px rgba(11, 12, 14, 0.03);
}

.progress-card {
  box-shadow:
    0 0 0 1px rgba(11, 12, 14, 0.03),
    0 2px 8px rgba(11, 12, 14, 0.03);
}

/* ============================================
   Card Header
   ============================================ */
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-header-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: #F5F5F7;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5F6B7A;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-icon {
  background: #F0F6F6;
  color: #4A6C6F;
}

.card-header-text {
  font-size: 15px;
  font-weight: 600;
  color: #0B0C0E;
  letter-spacing: -0.01em;
}

/* ============================================
   Form Layout
   ============================================ */
.trip-form {
  padding: 4px 0;
}

.form-section {
  padding: 4px 0;
}

.section-divider {
  height: 1px;
  background: #F3F4F5;
  margin: 20px 0;
}

.submit-section {
  padding-top: 12px;
  margin-top: 4px;
}

/* ============================================
   Days Alert
   ============================================ */
.days-alert {
  margin-top: 8px;
  border-radius: 10px;
  border: none;
}

/* ============================================
   Preference Group
   ============================================ */
.preference-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preference-group :deep(.el-checkbox) {
  margin-right: 0;
}

/* ============================================
   Budget Slider
   ============================================ */
.budget-slider-container {
  width: 100%;
  padding: 8px 0 0;
}

.budget-display {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.budget-separator {
  color: #C8CDD4;
  font-weight: 300;
  font-size: 13px;
}

.budget-label {
  color: #5F6B7A;
  font-size: 12px;
  font-weight: 500;
  margin-left: 4px;
  letter-spacing: 0.02em;
}

/* ============================================
   Model Selector
   ============================================ */
.model-selector {
  display: flex;
  gap: 10px;
}

.model-selector :deep(.el-radio) {
  margin-right: 0;
  flex: 1;
}

/* ============================================
   Buttons
   ============================================ */
.submit-btn {
  width: 100%;
  height: 54px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.02em;
  border-radius: 14px;
  background: linear-gradient(135deg, #0B0C0E 0%, #2D2F33 100%) !important;
  border: none !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(11, 12, 14, 0.18) !important;
}

.submit-btn:active {
  transform: translateY(0);
}

.stop-btn {
  width: 100%;
  height: 54px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.02em;
  border-radius: 14px;
  border-color: #EBECEE !important;
  color: #5F6B7A !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.stop-btn:hover {
  border-color: #0B0C0E !important;
  color: #0B0C0E !important;
  background: #FAFAFA !important;
}

.btn-icon {
  margin-right: 8px;
  font-size: 16px;
}

/* ============================================
   Progress Timeline
   ============================================ */
.progress-timeline {
  padding-left: 2px;
}

.progress-timeline :deep(.el-timeline-item__node) {
  border-width: 2px;
}

.progress-timeline :deep(.el-timeline-item__tail) {
  border-left-width: 1.5px;
}

.step-content {
  padding: 2px 0 14px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.step-name {
  font-weight: 500;
  color: #0B0C0E;
  font-size: 13px;
}

.step-tag {
  font-weight: 500;
  border-radius: 6px;
  font-size: 11px;
}

.step-message {
  color: #5F6B7A;
  font-size: 12px;
  margin-top: 6px;
  line-height: 1.6;
}

.step-error {
  color: #A05050;
  font-size: 12px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  line-height: 1.5;
}

/* ============================================
   Current Status
   ============================================ */
.current-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #F9FAFB;
  border-radius: 12px;
  color: #2D2F33;
  font-size: 13px;
  font-weight: 500;
  margin-top: 20px;
  border: 1px solid #F3F4F5;
}

.status-icon {
  font-size: 15px;
  color: #6B7685;
}

/* ============================================
   Progress Bar
   ============================================ */
.progress-bar {
  margin-top: 24px;
}

/* ============================================
   Empty Guide (右侧空状态)
   ============================================ */
.empty-guide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 64px 32px;
  background: #FFFFFF;
  border-radius: 20px;
  border: 1px solid #EBECEE;
  flex: 1;
  min-height: 280px;
}

.empty-guide-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #F5F5F7;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9BA5B3;
  margin-bottom: 20px;
}

.empty-guide-title {
  font-size: 16px;
  font-weight: 600;
  color: #0B0C0E;
  margin: 0 0 8px;
  letter-spacing: -0.02em;
}

.empty-guide-desc {
  font-size: 13px;
  color: #9BA5B3;
  margin: 0;
  line-height: 1.6;
  max-width: 200px;
}

/* ============================================
   Footer
   ============================================ */
.footer {
  text-align: center;
  margin-top: 56px;
  position: relative;
  z-index: 1;
  animation: fadeUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
}

.footer-link {
  color: #9BA5B3;
  font-weight: 500;
  font-size: 13px;
  letter-spacing: 0.02em;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 8px 16px;
  border-radius: 10px;
}

.footer-link:hover {
  color: #0B0C0E;
  background: #F3F4F5;
}

.footer-link :deep(.el-icon) {
  margin-right: 6px;
  font-size: 14px;
}

/* ============================================
   Animations
   ============================================ */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
    max-width: 640px;
  }

  .empty-guide {
    min-height: 160px;
    padding: 40px 24px;
  }
}

@media (max-width: 640px) {
  .home-container {
    padding: 56px 16px 48px;
  }

  .header {
    margin-bottom: 44px;
  }

  .header-accent {
    width: 32px;
    height: 3px;
    margin-bottom: 20px;
  }

  .brand-title {
    font-size: 38px;
  }

  .brand-subtitle {
    font-size: 12px;
    letter-spacing: 0.1em;
  }

  .form-card,
  .progress-card,
  .empty-guide {
    border-radius: 16px;
  }

  .section-divider {
    margin: 16px 0;
  }
}
</style>
