import { useEffect } from 'react'
import { useNotificationStore } from '@/store/notificationStore'

export function Toast() {
  const message = useNotificationStore((state) => state.message)
  const visible = useNotificationStore((state) => state.visible)
  const hideNotification = useNotificationStore((state) => state.hideNotification)

  useEffect(() => {
    if (!visible) return
    const timer = window.setTimeout(hideNotification, 3000)
    return () => window.clearTimeout(timer)
  }, [visible, message, hideNotification])

  if (!visible) return null
  return (
    <div role="status" className="fixed bottom-5 right-5 z-[70] max-w-sm rounded-xl bg-slate-900 px-4 py-3 font-medium text-white shadow-2xl dark:bg-sky-700">
      {message}
    </div>
  )
}
