import React, { useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const sessions = [
  { id: 'P01', name: 'Khởi đầu sự nghiệp công nghệ', time: '08:30 – 09:30', category: 'Định hướng', text: 'Khám phá lộ trình nghề nghiệp và những kỹ năng cần có để bước vào ngành công nghệ.' },
  { id: 'P02', name: 'CV nổi bật & phỏng vấn tự tin', time: '09:45 – 10:45', category: 'Kỹ năng', text: 'Chuẩn bị hồ sơ, kể câu chuyện của bạn và luyện tập cùng nhà tuyển dụng.' },
  { id: 'P03', name: 'Kết nối cùng doanh nghiệp', time: '11:00 – 12:00', category: 'Kết nối', text: 'Gặp gỡ doanh nghiệp, tìm hiểu vị trí thực tập và cơ hội dành cho sinh viên.' },
];

function App() {
  const [maSv, setMaSv] = useState('');
  const [selected, setSelected] = useState('P01');
  const [result, setResult] = useState({ type: 'idle' });
  const [loading, setLoading] = useState(false);
  const inFlight = useRef(false);
  const session = sessions.find(item => item.id === selected);
  function change(action) { action(); setResult({ type: 'idle' }); }

  async function register(event) {
    event.preventDefault();
    if (inFlight.current) return;
    inFlight.current = true;
    setLoading(true);
    setResult({ type: 'idle' });
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch('http://localhost:8000/api/dang-ky', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ma_sv: maSv.trim(), ma_phien: selected }),
        signal: controller.signal,
      });
      if (response.status === 201) setResult({ type: 'success', message: `Bạn đã đăng ký phiên ${selected}. Hẹn gặp bạn tại Ngày hội việc làm!` });
      else if (response.status === 409) setResult({ type: 'duplicate', message: `Mã sinh viên ${maSv.trim()} đã đăng ký phiên ${selected}. Bạn có thể chọn một phiên khác.` });
      else if (response.status === 422) setResult({ type: 'error', message: 'Dữ liệu chưa hợp lệ. Hãy kiểm tra mã sinh viên và phiên đã chọn.' });
      else setResult({ type: 'error', message: 'Máy chủ chưa xử lý được yêu cầu. Vui lòng thử lại.' });
    } catch (error) {
      setResult({ type: 'error', message: error.name === 'AbortError' ? 'Kết nối quá thời gian chờ. Vui lòng thử lại.' : 'Không kết nối được máy chủ. Vui lòng thử lại sau.' });
    } finally {
      clearTimeout(timeout); inFlight.current = false; setLoading(false);
    }
  }

  return <>
    <header><a className="brand" href="#"><span className="brand-icon">N</span><span>NGÀY HỘI<span className="brand-sub">VIỆC LÀM</span></span></a><span className="header-note">Kết nối hôm nay. Khởi đầu ngày mai.</span><a className="header-link" href="#register">Đăng ký tham gia <span>↗</span></a></header>
    <main>
      <section className="hero"><div className="eyebrow"><span className="dot"/> CỔNG ĐĂNG KÝ DÀNH CHO SINH VIÊN</div><h1>Cơ hội mới.<br/><span>Hành trình của bạn.</span></h1><p>Gặp gỡ doanh nghiệp, mở rộng kết nối và sẵn sàng cho bước tiếp theo trong sự nghiệp.</p><div className="hero-facts"><span>↗ &nbsp; 03 phiên trải nghiệm</span><span>◷ &nbsp; Tham gia miễn phí</span></div><div className="hero-art" aria-hidden="true"><div className="art-circle"/><div className="art-arrow">↗</div><div className="art-caption">YOUR NEXT<br/>CHAPTER.</div></div></section>
      <section className="workspace" id="register">
        <div className="session-list"><div className="section-heading"><div><div className="eyebrow muted">KHÁM PHÁ CHƯƠNG TRÌNH</div><h2>Chọn phiên của bạn</h2></div><span className="count">01 — 03</span></div><p className="section-intro">Mỗi phiên là một bước tiến gần hơn đến công việc bạn muốn.</p>
          <div className="cards">{sessions.map((item, index) => <button type="button" className={`session-card ${selected === item.id ? 'selected' : ''}`} key={item.id} aria-pressed={selected === item.id} disabled={loading} onClick={() => change(() => setSelected(item.id))}><span className="card-number">0{index + 1}</span><div className="card-content"><div className="card-meta"><span>{item.category}</span><span>{item.time}</span></div><h3>{item.name}</h3><p>{item.text}</p><span className="session-code">Phiên {item.id}</span></div><span className="radio" aria-hidden="true">{selected === item.id ? '✓' : ''}</span></button>)}</div>
        </div>
        <aside className="registration"><div className="eyebrow muted">SẴN SÀNG CHO BƯỚC TIẾP THEO?</div><h2>Giữ chỗ của bạn</h2><p className="form-intro">Chọn một phiên và nhập mã sinh viên để đăng ký tham gia.</p><form onSubmit={register}><label htmlFor="ma-sv">Mã sinh viên <span>*</span></label><input id="ma-sv" autoComplete="off" required maxLength={30} pattern="[A-Za-z0-9_-]+" placeholder="Ví dụ: 23110198" value={maSv} disabled={loading} onChange={event => change(() => setMaSv(event.target.value))}/><p className="input-help">Dùng mã sinh viên do trường cấp.</p><label htmlFor="ma-phien">Phiên tham gia <span>*</span></label><select id="ma-phien" value={selected} disabled={loading} onChange={event => change(() => setSelected(event.target.value))}>{sessions.map(item => <option key={item.id} value={item.id}>{item.id} — {item.name}</option>)}</select><div className="selection-summary"><span className="summary-icon">◷</span><div><strong>{session.time}</strong><span>{session.name}</span></div></div><button className="submit" disabled={loading} type="submit">{loading ? 'Đang đăng ký…' : 'Đăng ký tham gia'}<span aria-hidden="true">↗</span></button>
          <div className={`feedback ${result.type}`} role="status" aria-live="polite" aria-atomic="true">{result.type === 'idle' ? <><span className="feedback-icon">ⓘ</span><div><strong>{loading ? 'Đang gửi yêu cầu' : 'Mỗi phiên, một lượt đăng ký'}</strong><p>{loading ? 'Vui lòng chờ trong giây lát.' : 'Bạn có thể đăng ký nhiều phiên khác nhau. Mỗi phiên chỉ cần đăng ký một lần.'}</p></div></> : <><span className="feedback-icon">{result.type === 'success' ? '✓' : '!'}</span><div><strong>{result.type === 'success' ? 'Đăng ký thành công' : result.type === 'duplicate' ? 'Bạn đã đăng ký phiên này' : 'Chưa thể đăng ký'}</strong><p>{result.message}</p></div></>}</div></form><div className="form-footer">Thông tin được dùng để ghi nhận lượt đăng ký.</div></aside>
      </section><div className="bottom-note"><span>CHUẨN BỊ CHO NGÀY HỘI</span><p>Mang theo CV, sự tò mò và tinh thần sẵn sàng học hỏi.</p><span aria-hidden="true">↗</span></div>
    </main><footer><span>Ngày hội việc làm · Cổng đăng ký sinh viên</span><span>Ứng dụng thực hành CSE3051 · Buổi 3</span></footer>
  </>;
}

createRoot(document.getElementById('root')).render(<App/>);
