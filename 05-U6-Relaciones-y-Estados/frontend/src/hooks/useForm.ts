import { useState } from 'react'

export const useForm = <T,>(initialValues: T) => {
  const [values, setValues] = useState<T>(initialValues)

  const updateField = <K extends keyof T>(field: K, value: T[K]) => {
    setValues((current) => ({ ...current, [field]: value }))
  }

  return { values, updateField }
}
