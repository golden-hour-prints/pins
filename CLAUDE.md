# Golden Hour Prints — Pinterest media manager runbook

This repo runs the daily Pinterest routine for **Golden Hour Prints** (owner: Souhaib).
Product: *Easy Coloring Book for Seniors with Dementia and Alzheimer's* — https://www.amazon.com/dp/B0HLMN3TBJ
Pinterest account: `garaaouchsouhaib` (display name Golden Hour Prints), signed in inside the built-in browser pane of Souhaib's Claude desktop app.

Souhaib approved this routine in chat on 2026-10-02 (posting automatically, no per-pin confirmation): one pin per day from `queue.json`, saving 3–5 relevant pins per day to his boards, and a weekly report. Do nothing outside this list.

## Daily run (target: under 15 minutes)

1. **Reach the browser.** Load the built-in browser tools (`mcp__remote-devices__Claude_Browser__*`, one ToolSearch call). Open https://www.pinterest.com/ with `preview_start`. If the computer is unreachable or Pinterest shows a login page, stop and send Souhaib a short message: "Pinterest run skipped: <reason>". Never type passwords.
2. **Pick the next pin.** Take the first item in `queue.json` with `"status": "queued"`. Its image URL is `https://raw.githubusercontent.com/golden-hour-prints/pins/main/<image>`. Board ids are in `boards.json`.
3. **Post it.** Run `tools/post_pin.js` with the browser's `javascript_tool`, filling in the item's fields. The result is `{status, id}`. On success, set the item's `status` to `"posted"`, `posted_at` to today's date and `pin_id` to the id. On failure, record `"last_error"`, leave it queued and continue. Never post more than **one** pin per run.
4. **Save 3–5 pins from others.** Search Pinterest for one rotating topic, for example "dementia activities for seniors", "memory care activities", "gift ideas for nursing home residents", "caregiver tips dementia" or "large print activities for seniors". Pick helpful idea pins (activities, tips, free printables). Do **not** save other sellers' coloring books for sale. Use `tools/repin.js`, wait 4–7 s between saves, and put each pin on the matching board. Log the ids in `logs/saves.csv` and never save the same pin twice.
5. **Keep the queue full.** If fewer than 7 pins are queued, run `pip install -q opencv-python-headless pillow numpy` if needed, then `python tools/refill.py 14`.
6. **Commit and push**, with message `daily: pin <n> + <k> saves`.

## Every Monday (add to the daily run)

- Open https://analytics.pinterest.com/ (last 30 days). Read impressions, saves, outbound clicks, follower count and the top 5 pins.
- Append one row to `logs/weekly.csv`: date, impressions, engagements, outbound_clicks, saves, followers.
- Send Souhaib a short report: the numbers, the top pin and one change you'll make. Example: "before/after pins get 3× the clicks, so the next refill will be all before/after." Apply that change by editing the order in `tools/refill.py` and say what you changed.

## Hard rules (account safety, Pinterest guidelines)

- Never follow or unfollow accounts in bulk, comment, send messages, or join group boards.
- Never change account settings, the profile, passwords or payment details, and never turn on ads.
- Never delete pins or boards.
- Never claim the book treats, slows or improves dementia or memory.
- At most 1 own pin and 5 saves per day. If Pinterest shows any warning, captcha, "unusual activity" or a 403/429 error, stop at once and tell Souhaib.
- Our art is AI-made. If you ever use the pin builder UI instead of `post_pin.js`, switch on "Mark as AI-Modified".
