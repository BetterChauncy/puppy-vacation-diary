<script setup lang="ts">
import { reactive } from 'vue'
import type { Pet, PetFormData } from '../types'

const props = defineProps<{ pet?: Pet | null }>()
const emit = defineEmits<{
  save: [data: PetFormData]
  cancel: []
}>()

const form = reactive<PetFormData>({
  name: props.pet?.name ?? '',
  species: props.pet?.species ?? 'dog',
  gender: props.pet?.gender ?? '公',
  age: props.pet?.age ?? 1,
  avatar: props.pet?.avatar ?? null,
  address: props.pet?.address ?? '',
  birthday: props.pet?.birthday ?? '',
  bio: props.pet?.bio ?? '',
})

function submit() {
  emit('save', { ...form })
}
</script>

<template>
  <form @submit.prevent="submit" class="pet-form">
    <div class="form-group">
      <label>宠物名称</label>
      <input v-model="form.name" required placeholder="如：旺财" />
    </div>
    <div class="form-group">
      <label>种类</label>
      <select v-model="form.species">
        <option value="dog">狗</option>
        <option value="cat">猫</option>
        <option value="rabbit">兔子</option>
        <option value="hamster">仓鼠</option>
        <option value="bird">鸟</option>
        <option value="other">其他</option>
      </select>
    </div>
    <div class="form-group">
      <label>性别</label>
      <select v-model="form.gender">
        <option value="公">公</option>
        <option value="母">母</option>
      </select>
    </div>
    <div class="form-group">
      <label>年龄</label>
      <input v-model.number="form.age" type="number" min="0" max="50" required />
    </div>
    <div class="form-group">
      <label>头像 URL（可选）</label>
      <input v-model="form.avatar" placeholder="https://..." />
    </div>
    <div class="form-group">
      <label>地址（可选）</label>
      <input v-model="form.address" placeholder="如：北京市朝阳区" />
    </div>
    <div class="form-group">
      <label>生日（可选）</label>
      <input v-model="form.birthday" type="date" />
    </div>
    <div class="form-group">
      <label>个性签名（可选）</label>
      <textarea v-model="form.bio" rows="2" placeholder="一只快乐的小狗"></textarea>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary">
        {{ pet ? '保存修改' : '添加宠物' }}
      </button>
      <button type="button" class="btn btn-outline" @click="emit('cancel')">取消</button>
    </div>
  </form>
</template>

<style scoped>
.pet-form {
  padding: 8px 0;
}
.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}
</style>
