export function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

export function formatDate(iso) {
  if (!iso) return ''
  return iso.slice(0, 16).replace('T', ' ')
}

export function formatAge(years) {
  if (years < 1) return `${Math.round(years * 12)}个月`
  return `${years}岁`
}
