import { useStore } from '../store';

export default function Toaster() {
  const toasts = useStore((s) => s.toasts);
  if (!toasts.length) return null;

  return (
    <div className="toaster">
      {toasts.map((t) => (
        <div key={t.id} className={`toast ${t.type}`}>
          {t.msg}
        </div>
      ))}
    </div>
  );
}
