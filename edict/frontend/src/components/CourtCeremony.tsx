import { useEffect, useState } from 'react';
import { useStore, isEdict } from '../store';

export default function CourtCeremony() {
  const liveStatus = useStore((s) => s.liveStatus);
  const [show, setShow] = useState(false);
  const [out, setOut] = useState(false);

  useEffect(() => {
    const lastOpen = localStorage.getItem('openclaw_court_date');
    const today = new Date().toISOString().substring(0, 10);
    const pref = JSON.parse(localStorage.getItem('openclaw_court_pref') || '{"enabled":true}');
    if (!pref.enabled || lastOpen === today) return;
    localStorage.setItem('openclaw_court_date', today);
    setShow(true);
    const timer = setTimeout(() => skip(), 3500);
    return () => clearTimeout(timer);
  }, []);

  const skip = () => {
    setOut(true);
    setTimeout(() => setShow(false), 500);
  };

  if (!show) return null;

  const tasks = liveStatus?.tasks || [];
  const jjc = tasks.filter(isEdict);
  const pending = jjc.filter((t) => !['Done', 'Cancelled'].includes(t.state)).length;
  const done = jjc.filter((t) => t.state === 'Done').length;
  const overdue = jjc.filter(
    (t) => t.state !== 'Done' && t.state !== 'Cancelled' && t.eta && new Date(t.eta.replace(' ', 'T')) < new Date()
  ).length;

  const d = new Date();
  const days = ['日', '一', '二', '三', '四', '五', '六'];
  const dateStr = `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 · ${days[d.getDay()]}曜日`;

  return (
    <div className={`ceremony-bg${out ? ' out' : ''}`} onClick={skip}>
      <div className="crm-glow" />
      <div className="crm-line1 in">🏛 早朝开始</div>
      <div className="crm-line2 in">有事启奏，无事退朝</div>
      <div className="crm-line3 in">
        待办 {pending} 件 · 已完成 {done} 件{overdue > 0 && ` · ⚠ 超期 ${overdue} 件`}
      </div>
      <div className="crm-date in">{dateStr}</div>
      <div className="crm-skip">点击任意处跳过</div>
    </div>
  );
}
