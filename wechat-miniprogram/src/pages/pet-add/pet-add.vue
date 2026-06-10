<template>
  <view class="page">
    <view class="form">
      <view class="field">
        <text class="label">宠物名称 <text class="required">*</text></text>
        <input class="input" v-model="form.name" placeholder="如：旺财" />
      </view>
      <view class="field">
        <text class="label">种类 <text class="required">*</text></text>
        <picker class="picker" :value="speciesIndex" :range="speciesList" @change="onSpeciesChange">
          <text>{{ speciesList[speciesIndex] }}</text>
        </picker>
      </view>
      <view class="field">
        <text class="label">性别 <text class="required">*</text></text>
        <picker class="picker" :value="genderIndex" :range="genderList" @change="onGenderChange">
          <text>{{ genderList[genderIndex] }}</text>
        </picker>
      </view>
      <view class="field">
        <text class="label">年龄（岁） <text class="required">*</text></text>
        <picker class="picker" :value="ageIndex" :range="ageList" @change="onAgeChange">
          <text>{{ ageList[ageIndex] }}</text>
        </picker>
      </view>
      <view class="field">
        <text class="label">地址（可选）</text>
        <input class="input" v-model="form.address" placeholder="如：北京市朝阳区" />
      </view>
      <view class="field">
        <text class="label">生日（可选）</text>
        <picker class="picker" mode="date" :value="form.birthday" @change="onBirthdayChange">
          <text>{{ form.birthday || '选择日期' }}</text>
        </picker>
      </view>
      <view class="field">
        <text class="label">个性签名（可选）</text>
        <textarea class="textarea" v-model="form.bio" placeholder="一只快乐的小狗" />
      </view>
      <button class="submit-btn" :disabled="submitting" @click="onSubmit">
        {{ submitting ? '提交中...' : '添加宠物' }}
      </button>
    </view>
  </view>
</template>

<script>
import { createPet } from '../../api/pet'

export default {
  data() {
    return {
      speciesList: ['狗', '猫', '兔子', '仓鼠', '鸟', '其他'],
      genderList: ['公', '母'],
      ageList: Array.from({ length: 30 }, (_, i) => `${i + 1} 岁`),
      form: {
        name: '',
        species: '狗',
        gender: '公',
        age: 1,
        address: '',
        birthday: '',
        bio: '',
      },
      speciesIndex: 0,
      genderIndex: 0,
      ageIndex: 0,
      submitting: false,
    }
  },
  methods: {
    onSpeciesChange(e) {
      this.speciesIndex = e.detail.value
      this.form.species = this.speciesList[e.detail.value]
    },
    onGenderChange(e) {
      this.genderIndex = e.detail.value
      this.form.gender = this.genderList[e.detail.value]
    },
    onAgeChange(e) {
      this.ageIndex = e.detail.value
      this.form.age = e.detail.value + 1
    },
    onBirthdayChange(e) {
      this.form.birthday = e.detail.value
    },
    async onSubmit() {
      if (!this.form.name.trim()) {
        uni.showToast({ title: '请输入宠物名称', icon: 'none' })
        return
      }
      this.submitting = true
      try {
        const data = { ...this.form }
        if (!data.birthday) delete data.birthday
        if (!data.address) delete data.address
        if (!data.bio) delete data.bio
        await createPet({ name: data.name, species: this.speciesMap[this.form.species], gender: data.gender, age: data.age, address: data.address || undefined, birthday: data.birthday || undefined, bio: data.bio || undefined })
        uni.showToast({ title: '添加成功', icon: 'success' })
        setTimeout(() => uni.navigateBack(), 1000)
      } catch (e) {
        uni.showToast({ title: e.message || '添加失败', icon: 'none' })
      } finally {
        this.submitting = false
      }
    },
  },
  computed: {
    speciesMap() {
      return { '狗': 'dog', '猫': 'cat', '兔子': 'rabbit', '仓鼠': 'hamster', '鸟': 'bird', '其他': 'other' }
    },
  },
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 16px;
}
.form {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
}
.field {
  margin-bottom: 16px;
}
.label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 6px;
  font-weight: 500;
}
.required {
  color: #ef4444;
}
.input {
  width: 100%;
  height: 40px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 14px;
  box-sizing: border-box;
}
.picker {
  width: 100%;
  height: 40px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 14px;
  line-height: 40px;
  color: #333;
  box-sizing: border-box;
}
.textarea {
  width: 100%;
  height: 80px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  box-sizing: border-box;
}
.submit-btn {
  width: 100%;
  height: 44px;
  background: #07c160;
  color: #fff;
  font-size: 16px;
  border-radius: 22px;
  margin-top: 8px;
  line-height: 44px;
}
.submit-btn[disabled] {
  background: #ccc;
}
</style>
