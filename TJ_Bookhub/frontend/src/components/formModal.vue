<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>{{ formTitle }}</h3>
        <button @click="closeModal" class="close-button">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submitForm">
          <div class="form-row" v-for="(row, index) in groupFormFields()" :key="index">
            <div v-for="field in row" :key="field.name" class="form-group">
              <label :for="field.name" class="form-label">{{ field.label }}</label>
              <input 
                v-if="field.type === 'text'"
                :type="field.type" 
                :id="field.name" 
                v-model="formData[field.name]" 
                :placeholder="field.placeholder"
                class="form-input"
                :required="field.required"
              >
              <input 
                v-if="field.type === 'number'"
                type="number"
                :id="field.name"
                v-model.number="formData[field.name]"
                :placeholder="field.placeholder"
                class="form-input"
                :required="field.required"
              />
              <select 
                v-if="field.type === 'select'"
                :id="field.name" 
                v-model="formData[field.name]" 
                class="form-input"
                :required="field.required"
              >
                <option value="">请选择</option>
                <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
              <textarea 
                v-if="field.type === 'textarea'"
                :id="field.name" 
                v-model="formData[field.name]" 
                :rows="field.rows || 4"
                class="form-textarea"
                :required="field.required"
              ></textarea>
              <div v-if="field.type === 'date'" class="form-date">
                <input 
                  type="date" 
                  :id="field.name" 
                  v-model="formData[field.name]" 
                  class="form-input"
                  :required="field.required"
                >
                <input 
                  type="time" 
                  :id="field.name + '-time'" 
                  v-model="formData[field.name + '_time']" 
                  class="form-input"
                  :required="field.required"
                >
              </div>
              <div v-if="errors[field.name]" class="error-message">{{ errors[field.name] }}</div>
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button @click="closeModal" class="cancel-button">取消</button>
        <button @click="submitForm" class="submit-button">{{ submitText }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  formTitle: {
    type: String,
    default: '表单'
  },
  submitText: {
    type: String,
    default: '提交'
  },
  formFields: {
    type: Array,
    default: () => []
  },
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      type_id: '',
      image: '',
      start_time: '',
      end_time: '',
      location: '',
      brief: '',
      organizer: '',
      theme: '',
      is_featured: false
    })
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  recordId: {
    type: Number,
    default: null
  }
});

const emits = defineEmits(['close', 'submit']);

const formData = ref({ ...props.initialData });
const errors = ref({});

const groupFormFields = () => {
  const grouped = [];
  let currentRow = [];
  for (const field of props.formFields) {
    if (currentRow.length < 2) {
      currentRow.push(field);
    } else {
      grouped.push(currentRow);
      currentRow = [field];
    }
  }
  if (currentRow.length > 0) {
    grouped.push(currentRow);
  }
  return grouped;
};

onMounted(() => {
  console.log("组件重新挂载");
  const initial = { ...props.initialData };
  
  // 处理 publish_date 拆分
  if (initial.publish_date) {
    const date = new Date(initial.publish_date);
    if (!isNaN(date.getTime())) {
      // yyyy-MM-dd
      const yyyyMMdd = date.toISOString().slice(0, 10);
      // HH:mm
      const hhmm = date.toTimeString().slice(0, 5);

      initial.publish_date = yyyyMMdd;
      initial.publish_date_time = hhmm;
    }
  }

  formData.value = initial;
});

const closeModal = () => {
  emits('close');
};

const validateForm = () => {
  const newErrors = {};
  let isValid = true;
  
  for (const field of props.formFields) {
    const value = formData.value[field.name];

    if (field.required && (value === undefined || value === null || value === '')) {
      newErrors[field.name] = `${field.label} 是必填项`;
      isValid = false;
    } else if (field.type === 'email' && value && !isValidEmail(value)) {
      newErrors[field.name] = '请输入有效的邮箱地址';
      isValid = false;
    } else if (field.type === 'date' && value && formData.value[field.name + '_time']) {
      const dateStr = `${value}T${formData.value[field.name + '_time']}`;
      if (isNaN(Date.parse(dateStr))) {
        newErrors[field.name] = '请输入有效的日期和时间';
        isValid = false;
      }
    } else if (field.type === 'number') {
      if (!Number.isInteger(value)) {
        newErrors[field.name] = `${field.label} 必须是整数`;
        isValid = false;
      } else if (value < 0) {
        newErrors[field.name] = `${field.label} 不能为负数`;
        isValid = false;
      }
    }
  }

  errors.value = newErrors;
  return isValid;
};

const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const prepareSubmitData = () => {
  const data = { ...formData.value };
  for (const field of props.formFields) {
    if (field.type === 'date' && data[field.name] && data[field.name + '_time']) {
      data[field.name] = `${data[field.name]}T${data[field.name + '_time']}`;
      delete data[field.name + '_time'];
    }
  }
  return data;
};

const submitForm = () => {
  if (validateForm()) {
    const data = prepareSubmitData();
    emits('submit', {
      data,
      isEdit: props.isEdit,
      recordId: props.recordId
    });
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px; /* 增加最大宽度 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-textarea {
  resize: vertical;
}

.form-date {
  display: flex;
  gap: 10px;
}

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.cancel-button, .submit-button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #333;
  margin-right: 10px;
}

.submit-button {
  background-color: #3498db;
  color: white;
}
</style>