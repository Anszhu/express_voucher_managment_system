import { useEffect, useState, type ReactNode } from 'react';

/* ============================================================
   StatusBadge — Reusable status chip component
   ============================================================ */
export function StatusBadge({ status }: { status: string }) {
  const colorMap: Record<string, string> = {
    DRAFT: 'amber',
    PENDING_APPROVAL: 'violet',
    APPROVED: 'green',
    REJECTED: 'red',
  };
  const color = colorMap[status] || 'blue';
  const label = status.replaceAll('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  return <span className={`status ${color}`}>{label}</span>;
}

/* ============================================================
   Toast — Notification toast with auto-dismiss
   ============================================================ */
type ToastType = 'success' | 'error' | 'info' | 'warning';
type ToastItem = { id: string; type: ToastType; message: string };

let toastId = 0;
let addToastFn: ((t: ToastItem) => void) | null = null;

export function showToast(message: string, type: ToastType = 'info') {
  if (addToastFn) {
    addToastFn({ id: String(++toastId), type, message });
  }
}

export function ToastContainer() {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  useEffect(() => {
    addToastFn = (t: ToastItem) => {
      setToasts((prev) => [...prev, t]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((item) => item.id !== t.id));
      }, 4000);
    };
    return () => { addToastFn = null; };
  }, []);

  const remove = (id: string) => setToasts((prev) => prev.filter((t) => t.id !== id));

  const icons: Record<ToastType, string> = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  return (
    <div className="toast-container">
      {toasts.map((t) => (
        <div key={t.id} className={`toast ${t.type}`}>
          <span>{icons[t.type]}</span>
          <span>{t.message}</span>
          <button onClick={() => remove(t.id)}>×</button>
        </div>
      ))}
    </div>
  );
}

/* ============================================================
   ConfirmDialog — Confirmation modal with actions
   ============================================================ */
export function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
  danger = false,
}: {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  danger?: boolean;
}) {
  if (!open) return null;
  return (
    <div className="confirm-overlay" onClick={onCancel}>
      <div className="confirm-dialog" onClick={(e) => e.stopPropagation()}>
        <h3>{title}</h3>
        <p>{message}</p>
        <div className="confirm-actions">
          <button className="secondary" onClick={onCancel}>
            {cancelLabel}
          </button>
          <button className={danger ? 'danger' : 'primary'} onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
