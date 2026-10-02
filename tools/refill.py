"""Add N new pins to queue.json (images rendered into images/).

Usage: python tools/refill.py [N]   (default 10)
Order: before/after for designs not yet used -> colored spotlights -> tip cards.
Seasonal designs are moved to the front in their season.
"""
import json, os, sys, datetime, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P

ROOT = P.ROOT
AMAZON = "https://www.amazon.com/dp/B0HLMN3TBJ"
BOARDS = ["Large Print Coloring Pages for Seniors", "Dementia Activities for Seniors",
          "Memory Care Activity Ideas", "Calm Activities for Caregivers", "Gifts for Grandma & Seniors"]
SEASON = {10: ["36_autumn_pumpkins"], 11: ["36_autumn_pumpkins", "30_fireplace"], 12: ["40_holiday_wreath", "37_snowy_cabin", "30_fireplace"],
          1: ["37_snowy_cabin", "30_fireplace"], 2: ["37_snowy_cabin"], 3: ["38_spring_blossoms", "18_tulip_bed"], 4: ["38_spring_blossoms", "18_tulip_bed"],
          5: ["17_rose_arch", "38_spring_blossoms"], 6: ["23_beach_chairs", "39_ice_cream_stand"], 7: ["39_ice_cream_stand", "10_lemonade"],
          8: ["08_picnic", "23_beach_chairs"], 9: ["36_autumn_pumpkins", "05_camper_lake"]}
TITLES = ["{n} Coloring Page for Seniors – Large Print, Bold Lines",
          "Easy {n} Coloring Page for Adults with Dementia",
          "{n}: Large Print Coloring Activity for the Elderly",
          "Calm {n} Coloring Page for Memory Care",
          "{n} – Simple Coloring Page for Grandma"]
SUBS = ["Large print coloring page for seniors", "Easy coloring page for adults with dementia",
        "Bold-line coloring for older hands and eyes", "Calm memory-care coloring activity", "Big spaces, thick lines, no fuss"]
DESCS = ["A calm, easy {nl} coloring page with thick lines and big spaces, made for older hands and eyes. From a 40-design large print coloring book for seniors, dementia and Alzheimer's care and memory care activities. Familiar, grown-up pictures, never childish. Single-sided pages with a cut line.",
         "Looking for a simple activity for a parent or grandparent with memory loss? This {nl} page is easy to color together: large print, bold lines and familiar everyday scenes. One of 40 designs in Easy Coloring Book for Seniors with Dementia and Alzheimer's.",
         "{n} coloring page for seniors. Large print and bold lines make it easy to see and color, a relaxing activity for the elderly, memory care residents and caregivers coloring side by side. 40 calm designs in the full book: tea time, gardens, pets, the seaside and the seasons."]
TIPS = [("6 Calm Activities for a Loved One with Dementia", ["Color a familiar picture together", "Sort buttons, socks or cutlery", "Listen to songs from their youth",
         "Water and care for a houseplant", "Fold towels or napkins", "Look through old photos"], "09_coffee"),
        ("Coloring with Grandma: 5 Easy Tips", ["Choose big, simple pictures", "Use chunky markers or crayons", "Offer only 3–4 colors",
         "Short sessions: 15–20 minutes", "Frame the finished page"], "16_sunflowers"),
        ("Memory Care Activity Ideas for This Week", ["Monday: tea-time coloring", "Tuesday: garden sorting game", "Wednesday: music and memories",
         "Thursday: color the seaside", "Friday: show-and-tell of finished pages"], "21_harbor"),
        ("Why Large Print Coloring Works for Seniors", ["Big spaces are easy to see", "Thick lines forgive shaky hands", "Familiar scenes spark conversation",
         "One page is one calm, finished task", "Single-sided pages, no bleed-through"], "31_sleeping_cat")]


def load():
    p = os.path.join(ROOT, "queue.json")
    return json.load(open(p)) if os.path.exists(p) else []


def main(n=10):
    q = load(); names = json.load(open(os.path.join(ROOT, "designs.json")))
    used = {(i.get("kind"), i.get("design")) for i in q}
    month = datetime.date.today().month
    order = SEASON.get(month, []) + [s for s in names if s not in SEASON.get(month, [])]
    cands = [("before_after", s) for s in order] + [("spotlight", s) for s in order] + [("tips", t[0]) for t in TIPS]
    cands = [c for c in cands if c not in used]
    rnd = random.Random(len(q)); added = 0
    for kind, key in cands:
        if added >= n: break
        k = len(q)
        if kind == "tips":
            title, lines, art = next(t for t in TIPS if t[0] == key)
            im = P.quote_card(art, lines, title); ptitle = title
            desc = title + ": " + "; ".join(lines) + ". Easy large print coloring pages for seniors make a calm, familiar activity. 40 designs in Easy Coloring Book for Seniors with Dementia and Alzheimer's."
            alt = f"Pin listing: {title.lower()}, with a small colored stained-glass design."
            board = BOARDS[3] if k % 2 else BOARDS[1]
        else:
            nm = names[key]; ptitle = TITLES[k % len(TITLES)].format(n=nm)
            sub = SUBS[(k * 2 + 1) % len(SUBS)]
            im = P.before_after(key, ptitle, sub, seed=k) if kind == "before_after" else P.spotlight(key, ptitle, sub, seed=k + 7)
            desc = DESCS[k % len(DESCS)].format(n=nm, nl=nm.lower())
            alt = (f"Large print stained-glass coloring page of {nm.lower()} for seniors, shown blank and colored in."
                   if kind == "before_after" else f"Colored-in large print coloring page of {nm.lower()}, stained-glass style, for seniors.")
            board = BOARDS[(k * 3 + 1) % len(BOARDS)]
        fname = f"images/{k + 1:03d}_{kind}_{key[:3].strip('_') if kind != 'tips' else 'tips'}_{rnd.randint(100, 999)}.jpg"
        P.save(im, os.path.join(ROOT, fname))
        q.append({"n": k + 1, "kind": kind, "design": key, "image": fname, "title": ptitle[:100], "description": desc[:500],
                  "alt": alt[:500], "board": board, "link": AMAZON, "status": "queued"})
        added += 1
    json.dump(q, open(os.path.join(ROOT, "queue.json"), "w"), indent=1)
    print(f"added {added}, queue now {len(q)} ({sum(i['status'] == 'queued' for i in q)} queued)")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
