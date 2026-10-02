// Run in the Pinterest tab via javascript_tool after replacing the PIN object with the queue item's fields.
const PIN = { board_id: "BOARD_ID", image_url: "https://raw.githubusercontent.com/golden-hour-prints/pins/main/IMAGE",
  link: "https://www.amazon.com/dp/B0HLMN3TBJ", title: "TITLE", description: "DESCRIPTION", alt_text: "ALT" };
const csrf = document.cookie.split('; ').find(c => c.startsWith('csrftoken=')).split('=')[1];
const body = new URLSearchParams({ source_url: '/pin-creation-tool/', data: JSON.stringify({ options: { ...PIN, method: 'scraped', scrape_metric: { source: 'www_url_scrape' } }, context: {} }) });
const r = await fetch('/resource/PinResource/create/', { method: 'POST', credentials: 'include', body,
  headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest', 'X-Pinterest-AppState': 'active', 'Content-Type': 'application/x-www-form-urlencoded' } });
const j = await r.json().catch(() => null); const d = j && j.resource_response;
({ status: r.status, id: d && d.data && d.data.id, error: d && d.error && JSON.stringify(d.error).slice(0, 300) })
