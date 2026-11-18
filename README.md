# The World in a Day — Wednesday 18 November 2026

One image summing up the world news of Wednesday 18 November 2026, made for
the make.fun bounty [news-image-20261118](https://make.fun/bounty/news-image-20261118).

The front page (`entry.png`, 1024×1024) carries six stories in a 2×3 grid,
each with a short factual caption. The panels were generated as one text-free
collage and laid out with `composite.py` (Pillow); `main.py` simply copies
`entry.png` to the output directory.

## The six stories

1. **Kerch Bridge road arch collapses; Russia hits Kyiv bridges** — Ukraine
   struck the Kerch Bridge for a second day; President Zelenskiy said its main
   road arch had collapsed into the strait. Overnight Russia hit Kyiv's two
   main Dnipro bridges, the North and South crossings.
   Source: AP via Montana Public Radio,
   https://www.mtpr.org/2026-11-17/ukraine-strikes-major-russian-bridge-with-drones-and-missiles-as-aerial-attacks-escalate
2. **Iran drones hit US radar base in Bahrain, third attack in days** — Iran
   fired drones at a US military radar facility in Bahrain on 17 November, its
   third attack in days on US targets there; Bahrain said its air defences
   intercepted the attack and the US reported no damage or injuries.
   Source: Associated Press via Military.com,
   https://www.military.com/a-2-month-lull-ends-with-irans-third-strike-on-us-targets-in-bahrain
3. **Tanker MT TARA GAS hit twice in Hormuz; one seafarer missing** — The
   Panama-flagged LPG carrier was attacked twice in the Strait of Hormuz,
   forcing the crew to abandon ship; 21 of 24 Indian nationals were evacuated
   ashore at Khasab, two were hospitalised, and one seafarer remained missing.
   Source: Seatrade Maritime,
   https://www.seatrade-maritime.com/security/lpg-tanker-suffers-engine-room-fire-following-hormuz-attack
4. **Nvidia posts $115.8B quarter; board says Huang will not return** — Nvidia
   reported fiscal Q3 revenue of $115.8 billion, up 103% year on year, in its
   first earnings report since co-founder Jensen Huang resigned as CEO; the
   board said it does not intend to reinstate him.
   Source: Gizmodo,
   https://gizmodo.com/nvidias-ai-money-machine-keeps-churning-without-jensen-huang-2000841301
5. **APEC opens in Shenzhen; first Trump–Xi–Putin meeting Thursday** — The
   33rd APEC Economic Leaders' Meeting opened in Shenzhen on 18 November; a
   trilateral between Xi Jinping, Donald Trump and Vladimir Putin is scheduled
   for Thursday 19 November, the first ever between the three leaders.
   Source: Le Monde,
   https://www.lemonde.fr/en/international/article/2026/11/18/with-trump-and-putin-at-his-side-xi-puts-himself-front-and-center-on-world-stage_6782965_4.html
6. **Cyclone Akvan forecast to hit India's east coast Friday** — Cyclonic
   Storm Akvan in the Bay of Bengal was forecast by the India Meteorological
   Department to cross the Andhra Pradesh and Yanam coasts around noon on
   Friday 20 November as a very severe cyclonic storm.
   Source: India Meteorological Department, National Bulletin No. 14,
   https://mausam.imd.gov.in/Forecast/marquee_data/14.%20National%20Bulletin%20No%2014-17Nov2026_0830IST.pdf

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` — byte-identical on every run. To rebuild the
front page from the six-panel collage, run `python3 composite.py`.

## License

MIT — see `LICENSE`.
