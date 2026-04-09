"""
Merge LLM-extracted parts data with raw_posts.json metadata to produce keyboards.json.

The EXTRACTIONS dict below was hand-built by Claude reading evidence.txt for each
post. Posts not in this dict are skipped (collection posts, joke posts, posts with
no parts info anywhere).
"""

import json

# Each entry: id -> {parts, inferred, notes}
# parts categories: case, pcb, plate, switches, keycaps, stabilizers, layout, mods, cable, deskmat
# inferred: sound_profile (thocky/clacky/creamy/poppy/marbley/null),
#           build_tier (budget/mid/high-end/endgame),
#           aesthetic (list of tags),
#           typing_feel (linear/tactile/clicky/silent-tactile/topre),
#           build_complexity (stock/light-mod/heavy-mod),
#           confidence (low/medium/high)

E = {
    "j8aqrn": {
        "parts": {
            "case": "PAW", "switches": "Sakurios (60g TX springs, lubed Hoppes 9 + Krytox 205g0, filmed)",
        },
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["minimal", "themed"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "medium"},
    },
    "l5goai": {
        "parts": {"case": "V4N4G0N r1", "plate": "polycarbonate", "switches": "Tangerines",
                  "keycaps": "GMK Olivia++ Dark Base + Olivia r1 extensions"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "mzde6e": {
        "parts": {"case": "Think 6.5 v2 (white top, polycarbonate bottom)",
                  "switches": "Gateron Black v2 (lubed Krytox 205g0)",
                  "keycaps": "ePBT BoW + Geekarc accents", "deskmat": "TKC Netizen"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["BoW", "minimal"],
                     "typing_feel": "linear", "build_complexity": "light-mod", "confidence": "high"},
    },
    "jl1nmb": {
        "parts": {"case": "Satisfaction 75", "plate": "FR4", "switches": "Alpacas (lubed/filmed)",
                  "keycaps": "GMK Minimal", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "marbley", "build_tier": "high-end", "aesthetic": ["BoW", "minimal", "gold"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "mqt9se": {
        "parts": {"case": "PC Iron165 SE Prototype (Smith and Rune)", "plate": "copper",
                  "switches": "Zykos (Zealios bottom + translucent panda top + halo stem + Sprit springs)",
                  "keycaps": "GMK Copper", "cable": "Keebstuff Cu Custom Lemo"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["copper", "warm"],
                     "typing_feel": "tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "j2qs8v": {
        "parts": {"case": "Satisfaction 75", "plate": "brass", "switches": "Alpacas (lubed/filmed)",
                  "keycaps": "GMK Minimal", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "clacky", "build_tier": "high-end", "aesthetic": ["BoW", "minimal", "gold"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "jdc6kw": {
        "parts": {"case": "custom clear acrylic (sandwich)", "pcb": "DZ60 Rev 3.0", "plate": "polished brass",
                  "switches": "Gateron Black Ink (Tribosys 3203)", "stabilizers": "GMK screw-in",
                  "keycaps": "Rama Heavy Industries"},
        "inferred": {"sound_profile": "thocky", "build_tier": "mid", "aesthetic": ["acrylic", "brass", "DIY"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "nek62r": {
        "parts": {"case": "HHKB Pro-3 Silenced", "keycaps": "Custom Topre Urushi Keycaps"},
        "inferred": {"sound_profile": "creamy", "build_tier": "endgame", "aesthetic": ["japanese", "luxury", "topre"],
                     "typing_feel": "topre-silent", "build_complexity": "stock", "confidence": "high"},
    },
    "hx0dgg": {
        "parts": {"case": "Rama U80-A (Milk E-white)", "keycaps": "GMK Peaches n Cream",
                  "switches": "Tacit (unlubed)", "stabilizers": "Durock (super lube)",
                  "cable": "freshcablez coiled aviator"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["peach", "cream", "white"],
                     "typing_feel": "linear", "build_complexity": "light-mod", "confidence": "high"},
    },
    "jwke5c": {
        "parts": {"case": "TX EO-87", "plate": "Chocobo brass",
                  "switches": "Alpacas (Krytox 205g0 + GPL 105 springs + Deskeys films, 63.5g Sprit Slow)",
                  "keycaps": "GMK Minimal", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["BoW", "minimal", "frosted"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "ihs3ca": {
        "parts": {"case": "Keycult No.2 Rev.1 (black + polished brass)",
                  "switches": "Gateron Black Inks (lubed)"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["black", "brass", "luxury"],
                     "typing_feel": "linear", "build_complexity": "light-mod", "confidence": "medium"},
    },
    "jhuwq2": {
        "parts": {"case": "Exclusive E6.5 (Mao)", "plate": "rose gold brass",
                  "switches": "Moyu Blacks (lubed Krytox 205g0)", "stabilizers": "Durock",
                  "keycaps": "GMK Olivia++", "cable": "loveme3000"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway", "rose gold"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "n8sq3z": {
        "parts": {"case": "7V (by gok101)", "plate": "PC + plate foam",
                  "switches": "Cherry Hyperglide MX Blacks (lubed 205g0, Deskeys films, Sprit 63.5g Slow springs)",
                  "keycaps": "GMK Shoko", "stabilizers": "Durock V2 (205g0 + XHT-BDZ on wires)",
                  "deskmat": "Kineticlabs Blue Horizons"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["blue", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "lruyn5": {
        "parts": {"case": "Space65 CV", "switches": "L&F 62g Tangerines",
                  "keycaps": "GMK Boba Fett", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["star wars", "earthy"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "oa0md2": {
        "parts": {"case": "Kara (Ramaworks)", "keycaps": "CRP C64 (hamm3rworks)"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["retro", "beige", "C64"],
                     "typing_feel": None, "build_complexity": "stock", "confidence": "medium"},
    },
    "l1eron": {
        "parts": {"case": "Sneakbox Prime_Elise", "plate": "polished brass",
                  "switches": "Holy Pandas (lubed)", "keycaps": "GMK Olivia++ + GMK B"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway", "alice"],
                     "typing_feel": "tactile", "build_complexity": "light-mod", "confidence": "high"},
    },
    "m4scy6": {
        "parts": {"case": "Noxary x60 (custom cerakote red)",
                  "switches": "Durock 62g (lubed 205g0, filmed)",
                  "stabilizers": "Cherry screw-in", "keycaps": "JTK Tripleshot"},
        "inferred": {"sound_profile": "clacky", "build_tier": "high-end", "aesthetic": ["red", "black"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "naov1t": {
        "parts": {"case": "Voice 65 eWhite", "plate": "aluminum",
                  "switches": "Original Aspiration", "stabilizers": "Durock V2",
                  "keycaps": "ePBT Kon Momo"},
        "inferred": {"sound_profile": "marbley", "build_tier": "high-end", "aesthetic": ["white", "pastel", "japanese"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "lf8fxl": {
        "parts": {"case": "KFE CE (royal purple)",
                  "switches": "CK Lavenders (lubed/filmed)",
                  "keycaps": "GMK Olivia++ Dark Base", "cable": "CruzCtrlCables"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["lilac", "purple", "olivia colorway"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "jnejp6": {
        "parts": {"case": "Mode Eighty Founder's Edition", "plate": "PVD rose gold brass",
                  "switches": "Cherry MX Hyperglide Blacks",
                  "keycaps": "GMK Olivia Light + Rama hihihi Enter"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway", "rose gold"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "o50iiq": {
        "parts": {"case": "Keycult No.2/65 (brass bottom)", "plate": "POM half plate",
                  "switches": "Gateron Inks (lubed Tribosys 3204 + 105 springs)",
                  "stabilizers": "Zeal", "keycaps": "GMK 8008 (implied)"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["brass", "patina", "warm"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "medium"},
    },
    "muqjn4": {
        "parts": {"case": "Tofu 60 Acrylic", "pcb": "1UP RGB PCB HSE", "plate": "polycarbonate",
                  "switches": "Gazzew Boba U4T 68g (lubed)", "stabilizers": "Durock V2",
                  "keycaps": "KAT Alpha", "mods": ["plate foam", "O-ring at standoffs"]},
        "inferred": {"sound_profile": "thocky", "build_tier": "mid", "aesthetic": ["acrylic", "RGB"],
                     "typing_feel": "silent-tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "l212dq": {
        "parts": {"case": "Eniigma Keyboards Infinitum (top mount)", "plate": "aluminum",
                  "switches": "Gateron Ink v2 (lubed 205g0, filmed)", "stabilizers": "Zeal v2 (lubed superlube)"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["polished", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "kishkb": {
        "parts": {"case": "Eniigma Keyboards Infinitum (top mount)", "plate": "aluminum",
                  "switches": "Gateron Ink v2 (lubed 205g0, filmed)", "stabilizers": "Zeal v2 (lubed superlube)",
                  "keycaps": "ePBT Sushi"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["sushi", "japanese", "colorful"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "iehhku": {
        "parts": {"case": "Keycult No.1/65 Black/Brass", "switches": "Retooled MX Blacks",
                  "keycaps": "GMK Olivia"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway", "brass", "black"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "ma1pzv": {
        "parts": {"case": "Rama U80-A Lake", "plate": "aluminum",
                  "switches": "Creampacas (lubed 205g0, 63.5g Sprit Slow, Deskeys films)",
                  "keycaps": "KAT Blanks"},
        "inferred": {"sound_profile": "creamy", "build_tier": "endgame", "aesthetic": ["blue", "white", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "k1kclm": {
        "parts": {"case": "Mode Eighty First Edition (Dark)", "plate": "Mode FR4",
                  "switches": "Creampacas (Krytox 205g0 + GPL 105 springs + Deskeys films)",
                  "keycaps": "GMK Oblivion", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["dark", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "l0k1la": {
        "parts": {"case": "Angry Miao Cyberboard (grey)", "plate": "aluminum",
                  "switches": "Gazzew Boba U4 (Tribosys 3203, lubed)", "keycaps": "GMK Dots"},
        "inferred": {"sound_profile": "creamy", "build_tier": "endgame", "aesthetic": ["futuristic", "RGB", "white"],
                     "typing_feel": "silent-tactile", "build_complexity": "light-mod", "confidence": "high"},
    },
    "mox6x2": {
        "parts": {"case": "ProjectKeyboard Sirius HHKB (POM)", "pcb": "WT60-D WEIRDFLEX",
                  "switches": "NK Creams (lubed 205g0)", "stabilizers": "Durock V2",
                  "keycaps": "GMK Botanical"},
        "inferred": {"sound_profile": "poppy", "build_tier": "endgame", "aesthetic": ["green", "POM", "translucent"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "lupcpb": {
        "parts": {"case": "TX-660C (txkeyboards) over FC660C", "switches": "Topre 55g domes (Tribosys 3204)",
                  "keycaps": "White POM alphas + pastel mods (mitchcapped) + thermochromic spacebar"},
        "inferred": {"sound_profile": "creamy", "build_tier": "endgame", "aesthetic": ["pastel", "marshmallow", "topre"],
                     "typing_feel": "topre", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "la1zk1": {
        "parts": {"case": "Doodboard Duckboard (acrylic)", "switches": "Gateron Ink Reds",
                  "stabilizers": "Durock v2", "keycaps": "DSA Vilebloom", "cable": "junk cable"},
        "inferred": {"sound_profile": "thocky", "build_tier": "mid", "aesthetic": ["floral", "acrylic", "ortho"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "g7azh6": {
        "parts": {"case": "Satisfaction 75 (CannonKeys)", "plate": "brass",
                  "switches": "Mauve (filmed TX, lubed 205g0)",
                  "stabilizers": "Durock (housing 205g0, wires dielectric grease)",
                  "keycaps": "GMK Oblivion V2 Git Base", "deskmat": "randomfrankp x NK"},
        "inferred": {"sound_profile": "clacky", "build_tier": "high-end", "aesthetic": ["dark", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "m354kl": {
        "parts": {"case": "ATXKB Moontower",
                  "switches": "NK Dry Yellow 63.5g (lubed 205g0, Deskeys films)",
                  "stabilizers": "C3 (lubed 205g0)", "keycaps": "CRP Peacock",
                  "deskmat": "GMK Bento R2 Waves"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["beige", "vintage"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "kz0civ": {
        "parts": {"case": "handwired 40% (acrylic)", "switches": "Gateron Milky Yellow (lubed Krytox 205g)",
                  "stabilizers": "Gateron (lubed Permatex)", "keycaps": "Tai-hao Dark Knight"},
        "inferred": {"sound_profile": "thocky", "build_tier": "budget", "aesthetic": ["DIY", "40%", "acrylic"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "l2pvu1": {
        "parts": {"case": "E-white E8.5 (pink badge/weight)", "switches": "Gazzew U4 Thocks (L&F)",
                  "stabilizers": "Durock screw-in (lubed)", "keycaps": "GMK 8008"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "white", "8008 colorway"],
                     "typing_feel": "silent-tactile", "build_complexity": "light-mod", "confidence": "high"},
    },
    "myhxfm": {
        "parts": {"case": "Think 6.5 V2", "switches": "Tangerine V2", "keycaps": "GMK Botanical"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["green", "botanical"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "medium"},
    },
    "qlwct7": {
        "parts": {"case": "RAMA x Ion Zenith", "switches": "Boba U4T Blacks",
                  "keycaps": "GMK WoB + GMK Stealth Rama artisans",
                  "cable": "Keebstuff Lemo Amboss x KAT Iron"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["BoW", "stealth", "minimal"],
                     "typing_feel": "tactile", "build_complexity": "stock", "confidence": "high"},
    },
    "mvj8ly": {
        "parts": {"case": "Night Owl Keyboards Gemini TKL", "plate": "brushed copper",
                  "switches": "Zykos (translucent panda top + zealios bottom + halo clear stem + 63.5g Sprit Slow)",
                  "keycaps": "GMK Copper", "stabilizers": "Durock v2"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["copper", "warm"],
                     "typing_feel": "tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "jzqwpb": {
        "parts": {"case": "45-ATS by Abec", "plate": "brass",
                  "switches": "T1s (lubed Tribosys 3204, TX films)", "keycaps": "GMK DMG",
                  "deskmat": "GMK DMG"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["gameboy", "retro", "grey"],
                     "typing_feel": "tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "nz44w2": {
        "parts": {"case": "MGA Standard", "plate": "hineybush 3/4 FR4",
                  "switches": "Cobalt POM Linears (Kinetic Labs Salmon Tactiles on spacebars)",
                  "keycaps": "ePBT Black Japanese", "deskmat": "Deep"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["dark", "japanese"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "liai9w": {
        "parts": {"case": "ai03 Vega (Blue)", "plate": "aluminum",
                  "switches": "Koalas 67g (L&F)", "keycaps": "GMK Voyage"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["blue", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "lzf9ie": {
        "parts": {"case": "TGR x Singa Unikorn R2.1 (PC)", "plate": "FR4",
                  "switches": "JWK Lavenders (lubed 205g0, Sprit 60g Slow Extreme II springs)",
                  "stabilizers": "Cherry clip-in (housings 205g0, wires XHT-BDZ)",
                  "keycaps": "GMK Shoko"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["blue", "translucent", "PC"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "jutlez": {
        "parts": {"case": "Duck TC-V3 (black anodized aluminum + brass weight)", "pcb": "TC-V3 (O2D)",
                  "plate": "full aluminum",
                  "switches": "Gateron Ink (UHMWPE stems, 70g springs, TX films, lubed 205g0)",
                  "stabilizers": "Cherry screw-in (lubed/clipped)", "keycaps": "GMK Alter"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["black", "premium"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "n45y3e": {
        "parts": {"case": "KBIC65 (custom designed, through-hole kit)", "pcb": "nice!nano (wireless, ZMK)",
                  "switches": "Gazzew Boba U4 silent tactile",
                  "keycaps": "ePBT 9009 + Win95 kit",
                  "mods": ["plate foam", "neoprene"]},
        "inferred": {"sound_profile": "creamy", "build_tier": "high-end", "aesthetic": ["DIY", "wireless", "retro"],
                     "typing_feel": "silent-tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "hxsbkh": {
        "parts": {"case": "Rama Koyu (Milk)",
                  "switches": "Gateron Black Ink (lubed 205g0, Thicc films)",
                  "keycaps": "ePBT x GOK BoW + KpRepublic PBT Muted",
                  "cable": "Melgeek Oblivion"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["white", "BoW", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "meftdn": {
        "parts": {"case": "Keycult No.2/65 (red bottom)", "plate": "POM half plate",
                  "switches": "Gateron Inks (lubed 205g0 + 105 springs)",
                  "stabilizers": "Zeal (dielectric plugs, 205g0, krytox BZT wires)",
                  "keycaps": "GMK Hennesey + BoW Micons"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["red", "warm"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "mnfzkf": {
        "parts": {"case": "ai03 Vega", "switches": "Lavenders", "keycaps": "GMK Umbra"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["dark", "purple"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "medium"},
    },
    "m85hj9": {
        "parts": {"case": "Space65 CyberVoyager EV-01",
                  "switches": "EV-01 JWK 63.5g linears",
                  "keycaps": "AliExpress Evangelion (until GMK Mecha-01)"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["evangelion", "anime", "purple"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "l4unur": {
        "parts": {"case": "Bauer", "switches": "Gateron Black Inks", "keycaps": "GMK Dual Shot"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["blue", "BoW"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "medium"},
    },
    "kv5012": {
        "parts": {"case": "Oceanographer Prototype", "pcb": "STM32 Diodeless",
                  "switches": "OG KBDfans T1 (smoke housing, teal stem; lubed Krytox 205g0 + 105)",
                  "stabilizers": "Durock Clear (gold wires)", "keycaps": "GMK Paperwork"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["blue", "ocean", "designer"],
                     "typing_feel": "tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "iyhm2a": {
        "parts": {"case": "Satisfaction 75", "plate": "brass", "switches": "Alpacas (lubed/filmed)",
                  "keycaps": "GMK Phosphorus + Infinikey BoW", "stabilizers": "Durock"},
        "inferred": {"sound_profile": "clacky", "build_tier": "high-end", "aesthetic": ["green", "BoW"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "kvudz6": {
        "parts": {"case": "IMK Corne (snow white cerakote)", "keycaps": "KAT Milkshake"},
        "inferred": {"sound_profile": "creamy", "build_tier": "high-end", "aesthetic": ["white", "minimal", "ergo split"],
                     "typing_feel": None, "build_complexity": "stock", "confidence": "medium"},
    },
    "1hkt3x8": {
        "parts": {"case": "IU by perry", "switches": "Cherry MX Brown",
                  "stabilizers": "TX AP", "keycaps": "GMK Analog Dreams"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["pastel", "kpop", "vaporwave"],
                     "typing_feel": "tactile", "build_complexity": "stock", "confidence": "high"},
    },
    "jqcrfm": {
        "parts": {"case": "acw88 (smoke polycarb prototype)", "plate": "polycarb half plate",
                  "pcb": "hineybush h88",
                  "switches": "Gateron Ink v2 (Tribosys 3204, films)", "stabilizers": "Durock",
                  "keycaps": "GMK WoB + icons + Cherry relegendables", "cable": "coaxius fixed Lemo"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["smoke", "BoW", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "mwt5i8": {
        "parts": {"case": "KBDFans Bella (ISO)",
                  "switches": "C3 Equalz x TKC Banana Split (lubed Krytox 205g0, Deskeys films)",
                  "keycaps": "GMK Laser", "cable": "Swiftcables Laser"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["pink", "laser", "vaporwave", "neon"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "o2n6lz": {
        "parts": {"case": "Geonworks F1", "switches": "Moss", "keycaps": "GMK Solarized Dark"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["dark", "blue", "solarized"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "medium"},
    },
    "ox67sn": {
        "parts": {"case": "Rama KARA (internal weight)",
                  "switches": "ThickThoc Shugoki Tactiles", "keycaps": "GMK Mitolet"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "warm"],
                     "typing_feel": "tactile", "build_complexity": "stock", "confidence": "high"},
    },
    "ii844i": {
        "parts": {"case": "Nibble 65% (through-hole)",
                  "switches": "Lilacs (lubed Tribosys 3204, TX filmed)",
                  "stabilizers": "Cherry screw-in (lubed Krytox 205g0)",
                  "keycaps": "GMK Metropolis"},
        "inferred": {"sound_profile": "thocky", "build_tier": "mid", "aesthetic": ["DIY", "pastel"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "mdoeks": {
        "parts": {"case": "Squid60 (grey, brass weight + brass plate, WKL)", "plate": "brass",
                  "pcb": "Instant60 Tsangan", "switches": "H1 (lubed 205g0)",
                  "stabilizers": "Zeal (lubed dielectric grease + 205g0)",
                  "keycaps": "GMK Oblivion"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["dark", "brass", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "nrrt1b": {
        "parts": {"case": "Keycult No.1/60 rev.1 (Midnight Rainbow patina)", "plate": "brass",
                  "switches": "Cobalts", "stabilizers": "Durock (lubed/plugged)",
                  "keycaps": "ePBT Black blanks"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["patina", "rainbow", "dark"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "ms8ngs": {
        "parts": {"case": "Boardsource PC Mark65", "switches": "Holy Boba",
                  "keycaps": "CustomMK Genesis", "deskmat": "Poly"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["white", "minimal", "split-space"],
                     "typing_feel": "tactile", "build_complexity": "stock", "confidence": "high"},
    },
    "pkhtb8": {
        "parts": {"case": "Aaru by HelixLab (purple/blue ano)",
                  "switches": "L&F Lavenders (TX springs)", "stabilizers": "C3",
                  "keycaps": "GMK VoC"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["purple", "eggplant"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "i3smx4": {
        "parts": {"case": "Iron165", "keycaps": "GMK WoB"},
        "inferred": {"sound_profile": None, "build_tier": "endgame", "aesthetic": ["BoW", "minimal"],
                     "typing_feel": None, "build_complexity": None, "confidence": "low"},
    },
    "m0mn7p": {
        "parts": {"case": "Graystudio Think 6.5 V2 (Stormtrooper colorway, gasket mount)",
                  "plate": "FR4",
                  "switches": "Alpaca V1 (lubed 205G0, Deskeys film)",
                  "stabilizers": "Smokey Durock V1 (205G0)",
                  "keycaps": "GMK Bleached"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["white", "stormtrooper", "minimal"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "m9571w": {
        "parts": {"case": "Pneuma Mk.1 (Cerakoted Armor Black)",
                  "plate": "carbon fiber full plate",
                  "switches": "Alpacas with 60g TX springs (lubed 205G0 + superlube PTFE oil)",
                  "keycaps": "GMK Olivia++"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["pink", "olivia colorway", "black"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "lwtbom": {
        "parts": {"case": "J02", "plate": "stainless steel (custom)",
                  "switches": "Amber ALPS (oiled springs Krytox 105)"},
        "inferred": {"sound_profile": "clacky", "build_tier": "high-end", "aesthetic": ["vintage", "alps"],
                     "typing_feel": "clicky", "build_complexity": "light-mod", "confidence": "high"},
    },
    "mq041o": {
        "parts": {"case": "V4N4G0N (r1 bottom/mid, r2 violet top)", "plate": "PC",
                  "switches": "Tangerines", "keycaps": "KAT Lich"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["purple", "dark", "halloween"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "owj3bw": {
        "parts": {"case": "Time80RE (black with gold/red accents)", "plate": "full red aluminum",
                  "switches": "L+F Marshmallow (lubed 205g0 + 105g0 springs, pink TX films)",
                  "stabilizers": "Durock v2 (lubed 205g0)",
                  "keycaps": "ePBT Gray on White Hiragana donor + GMK Higanbana",
                  "cable": "Mechcables", "deskmat": "Neko-Tomo"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["japanese", "anime", "red"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "ld6lwz": {
        "parts": {"case": "Bias", "plate": "FR4", "switches": "Gateron Inks", "keycaps": "GMK Darling"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["pink", "pastel"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "medium"},
    },
    "j9pdh4": {
        "parts": {"case": "Norbaforce MkII (VHS finish, donor Realforce R2 RGB)",
                  "keycaps": "GMK Minimal + GMK Coral mash"},
        "inferred": {"sound_profile": "topre", "build_tier": "endgame", "aesthetic": ["coral", "minimal", "topre"],
                     "typing_feel": "topre", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "iqxc1x": {
        "parts": {"case": "Dixie Mech Bauer (grey cerakote top, cyan bottom)", "pcb": "wilba.tech WT65-B",
                  "plate": "full POM",
                  "switches": "Gateron Ink (63.5g Sprit, TX films, lubed 205g0)",
                  "stabilizers": "Durock screw-in (lubed)", "keycaps": "GMK Modern Dolch R1"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["grey", "cyan", "modern dolch"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "igh12d": {
        "parts": {"case": "Klippe T R4 Ultramarine", "pcb": "Instant60", "plate": "polycarb",
                  "switches": "Gateron Black Ink (TX films, lubed Krytox 205g0)",
                  "stabilizers": "Everglide", "keycaps": "cheap BoW from AliExpress",
                  "cable": "Mechcables"},
        "inferred": {"sound_profile": "thocky", "build_tier": "mid", "aesthetic": ["blue", "BoW"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "k3azep": {
        "parts": {"case": "Space65 Cyber Voyager R2 (Robocop)",
                  "switches": "Holy Boba", "stabilizers": "Durock", "keycaps": "GMK Ascii"},
        "inferred": {"sound_profile": "thocky", "build_tier": "high-end", "aesthetic": ["dark", "monochrome"],
                     "typing_feel": "tactile", "build_complexity": "stock", "confidence": "high"},
    },
    "ltoep6": {
        "parts": {"case": "Keycult No.1 Rev.1", "plate": "polycarb",
                  "switches": "Alpacas (lubed/filmed)", "stabilizers": "Durock smokey",
                  "keycaps": "GMK Striker + Mt Fuji + Japan Flag artisans"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["red", "japanese", "blue"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "kjigfd": {
        "parts": {"case": "Keycult 1/60 OG (Battleship Grey)",
                  "switches": "63.5g Silks (Boba tops + Cherry stems, lubed 205g0)",
                  "stabilizers": "Durock (lubed 205g0 + dielectric)",
                  "keycaps": "GMK Botanical + Rama cap"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["green", "grey", "botanical"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "j35spn": {
        "parts": {"case": "E-White Hello m0110", "plate": "custom-cut PC",
                  "switches": "NK Creams (broken in, lubed 205g0)", "keycaps": "GMK Cafe"},
        "inferred": {"sound_profile": "marbley", "build_tier": "endgame", "aesthetic": ["beige", "brown", "vintage"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "kpxax9": {
        "parts": {"case": "ai03 Vega (Black)", "plate": "PC", "switches": "NK Creams",
                  "keycaps": "GMK Umbra"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["dark", "purple"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "nf6xo3": {
        "parts": {"case": "Gok 7V (black)", "plate": "PC",
                  "switches": "Lilac Lavenders (lubed 205g0, TX films)",
                  "stabilizers": "Durock V2 (205g0 + dielectric)",
                  "keycaps": "GMK Taro R2"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["purple", "pastel"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "nysyvl": {
        "parts": {"case": "Keycult 2/65 Black/Red", "plate": "brass",
                  "switches": "Random 150g unlubed MX Blues + Browns (joke build)",
                  "stabilizers": "Cherry clip-in (unlubed)",
                  "keycaps": "ahegao set from Amazon + EPBT BoW mods"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["meme", "joke", "anime"],
                     "typing_feel": "clicky", "build_complexity": "stock", "confidence": "high"},
    },
    "mly5u8": {
        "parts": {"case": "Gaff60 (blue)", "switches": "Ultramarine",
                  "stabilizers": "Ultramarine", "keycaps": "GMK Nautilus R2",
                  "cable": "Swiftcables Nautilus", "deskmat": "GMK Nautilus"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["blue", "nautical"],
                     "typing_feel": "linear", "build_complexity": "stock", "confidence": "high"},
    },
    "lsg5iz": {
        "parts": {"case": "PC Iron165 SE Prototype",
                  "switches": "Zykos (Halo Clear stem + Translucent Panda top + Zealios v2 bottom + 67g springs)",
                  "stabilizers": "Durock V2", "keycaps": "Kitty KAT"},
        "inferred": {"sound_profile": "clacky", "build_tier": "endgame", "aesthetic": ["pink", "cute"],
                     "typing_feel": "tactile", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "o5l8mh": {
        "parts": {"case": "Rama U80-A (Milk)",
                  "switches": "L+F Tealios v2",
                  "stabilizers": "Durock v2 (lubed 205g0, DG on wire)",
                  "keycaps": "ePBT Kuro/Shiro"},
        "inferred": {"sound_profile": "thocky", "build_tier": "endgame", "aesthetic": ["white", "BoW", "panda"],
                     "typing_feel": "linear", "build_complexity": "heavy-mod", "confidence": "high"},
    },
    "hdtj9x": {
        "parts": {"case": "Satisfaction 75", "keycaps": "GMK Oblivion"},
        "inferred": {"sound_profile": None, "build_tier": "high-end", "aesthetic": ["dark"],
                     "typing_feel": None, "build_complexity": None, "confidence": "low"},
    },
}


def find_parts_source_text(post):
    """Return the text we extracted parts from: OP comment(s) joined, or title if no OP."""
    op = [c["body"] for c in post["top_comments"] if c["is_op"]]
    if op:
        return "\n\n".join(op)
    return post["title"]


def main():
    raw = json.load(open("raw_posts.json"))
    out = []
    skipped = []

    for post in raw:
        pid = post["id"]
        if pid not in E:
            skipped.append(pid)
            continue
        ext = E[pid]
        # Fill in nulls for any unspecified part categories so the schema is consistent
        parts_full = {
            "case": None, "pcb": None, "plate": None, "switches": None,
            "keycaps": None, "stabilizers": None, "layout": None,
            "mods": None, "cable": None, "deskmat": None,
        }
        parts_full.update(ext["parts"])

        out.append({
            "id": pid,
            "title": post["title"],
            "author": post["author"],
            "permalink": post["permalink"],
            "created_utc": post["created_utc"],
            "score": post["score"],
            "image_urls": post["image_urls"],
            "parts": parts_full,
            "inferred": ext["inferred"],
            "raw": {
                "selftext": post["selftext"],
                "parts_source_text": find_parts_source_text(post),
            },
        })

    with open("keyboards.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"wrote {len(out)} entries to keyboards.json")
    print(f"skipped {len(skipped)} posts (collection/empty/joke): {skipped}")


if __name__ == "__main__":
    main()
