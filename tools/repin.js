// Run on a Pinterest search page via javascript_tool. Replace SAVES with [[pin_id, board_id], ...] (max 5).
const SAVES = [["PIN_ID", "BOARD_ID"]];
const csrf = document.cookie.split('; ').find(c => c.startsWith('csrftoken=')).split('=')[1];
const out = [];
for (const [pin_id, board_id] of SAVES) {
  const body = new URLSearchParams({ source_url: '/search/pins/', data: JSON.stringify({ options: { pin_id, board_id, description: '', is_buyable_pin: false, is_removable: false, carousel_slot_index: 0 }, context: {} }) });
  const r = await fetch('/resource/RepinResource/create/', { method: 'POST', credentials: 'include', body,
    headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest', 'X-Pinterest-AppState': 'active', 'Content-Type': 'application/x-www-form-urlencoded' } });
  out.push([pin_id, r.status]); if (r.status !== 200) break;
  await new Promise(res => setTimeout(res, 4000 + Math.random() * 3000));
}
out
// List candidate pins on a search page:
// [...new Map([...document.querySelectorAll('a[href*="/pin/"]')].map(a=>{const id=(a.href.match(/\/pin\/(\d+)/)||[])[1];const img=a.querySelector('img');return [id,{id,alt:(img&&img.alt||'').slice(0,80)}]}).filter(x=>x[0])).values()].slice(0,25)
