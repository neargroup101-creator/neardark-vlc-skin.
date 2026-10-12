#!/usr/bin/env python3
"""Build the NearDark VLC skin (skins2). Usage: python3 build.py [scale]. Output: out/NearDark.vlt"""
import os
import os, shutil, tarfile, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = 10
K = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
def S(v): return int(round(v * K))
def SC(v): return int(math.ceil(v * K - 1e-9))
from PIL import Image, ImageDraw
import io, re, math, cairosvg, sys

OUT = os.path.join(HERE, 'out')
SKIN = os.path.join(OUT, 'skin')
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(SKIN)
shutil.copy(os.path.join(HERE, 'src', 'roboto.ttf'), SKIN)

BG = (20, 21, 24, 255)
SURF = (32, 34, 40, 255)
VID = (11, 11, 12, 255)
TXT = (236, 236, 238, 255)
MUT = (139, 143, 152, 255)
ACC = (61, 139, 255, 255)      # #3D8BFF blue
REC = (235, 64, 64, 255)
TRK = (48, 50, 57, 255)
MAG = (255, 0, 255, 255)
CLEAR = (0, 0, 0, 0)
SS = 4
def hexc(c): return '#%02X%02X%02X' % c[:3]

LUC = {'close':'x','min':'minus','max':'square','restore':'copy','fs':'maximize','fsoff':'minimize',
       'pin':'pin','pinon':'pin','list':'list-video','add':'plus','vol':'volume-2','mute':'volume-x',
       'open':'settings','save':'save','shot':'camera','info':'info','mini':'picture-in-picture-2',
       'loop':'repeat','loop1':'repeat-1','shuffle':'shuffle','menu':'ellipsis','chevd':'chevron-down',
       'chevu':'chevron-up','wide':'move-horizontal','narrow':'fold-horizontal','prev':'skip-back',
       'next':'skip-forward','play':'play','pause':'pause','stop':'square'}
FILLED = {'prev','next','play','pause','stop'}
LSCALE = {'play':.56,'pause':.56,'prev':.5,'next':.5,'stop':.42}
def icon(name, size, color):
    if name in LUC:
        svg = open(os.path.join(HERE, 'src', 'lucide', LUC[name] + '.svg')).read()
        svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S).replace('currentColor', hexc(color))
        if name in FILLED:
            svg = svg.replace('fill="none"', f'fill="{hexc(color)}"')
        if name == 'pinon':
            svg = svg.replace('stroke-width="2"', 'stroke-width="2.6"')
        px = max(8, round(size * LSCALE.get(name, .5)))
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
        ic = Image.open(io.BytesIO(png)).convert('RGBA')
        if color[3] < 255:
            pass
        out = Image.new('RGBA', (size, size), CLEAR)
        out.alpha_composite(ic, ((size - px) // 2, (size - px) // 2))
        return out
    S = size * SS
    im = Image.new('RGBA', (S, S), CLEAR)
    d = ImageDraw.Draw(im)
    def P(x, y): return (x * S, y * S)
    w = max(2, int(S * 0.075))
    if name == 'play':
        d.polygon([P(.34, .24), P(.34, .76), P(.78, .5)], fill=color)
    elif name == 'pause':
        d.rounded_rectangle([P(.30, .24), P(.43, .76)], radius=S*.03, fill=color)
        d.rounded_rectangle([P(.57, .24), P(.70, .76)], radius=S*.03, fill=color)
    elif name == 'next':
        d.polygon([P(.28, .28), P(.28, .72), P(.62, .5)], fill=color)
        d.rounded_rectangle([P(.64, .28), P(.72, .72)], radius=S*.02, fill=color)
    elif name == 'prev':
        d.polygon([P(.72, .28), P(.72, .72), P(.38, .5)], fill=color)
        d.rounded_rectangle([P(.28, .28), P(.36, .72)], radius=S*.02, fill=color)
    elif name == 'close':
        d.line([P(.34, .34), P(.66, .66)], fill=color, width=w)
        d.line([P(.66, .34), P(.34, .66)], fill=color, width=w)
    elif name == 'min':
        d.line([P(.32, .55), P(.68, .55)], fill=color, width=w)
    elif name == 'max':
        d.rounded_rectangle([P(.33, .33), P(.67, .67)], radius=S*.04, outline=color, width=w)
    elif name == 'restore':
        d.rounded_rectangle([P(.40, .30), P(.70, .60)], radius=S*.03, outline=color, width=w)
        d.rectangle([P(.30, .40), P(.60, .70)], fill=CLEAR)
        d.rounded_rectangle([P(.30, .40), P(.60, .70)], radius=S*.03, outline=color, width=w)
    elif name in ('fs', 'fsoff'):
        for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            X = lambda v: v if sx == 0 else 1 - v
            Y = lambda v: v if sy == 0 else 1 - v
            if name == 'fs':
                d.line([P(X(.30), Y(.43)), P(X(.30), Y(.30)), P(X(.43), Y(.30))], fill=color, width=w, joint='curve')
            else:
                d.line([P(X(.30), Y(.42)), P(X(.42), Y(.42)), P(X(.42), Y(.30))], fill=color, width=w, joint='curve')
    elif name in ('pin', 'pinon'):
        if name == 'pinon':
            d.ellipse([P(.38, .22), P(.62, .46)], fill=color)
        else:
            d.ellipse([P(.38, .22), P(.62, .46)], outline=color, width=w)
        d.line([P(.5, .46), P(.5, .78)], fill=color, width=w)
    elif name == 'list':
        for y in (.33, .5, .67):
            d.line([P(.40, y), P(.72, y)], fill=color, width=w)
            d.ellipse([P(.27, y - .035), P(.34, y + .035)], fill=color)
    elif name == 'add':
        d.line([P(.5, .3), P(.5, .7)], fill=color, width=w)
        d.line([P(.3, .5), P(.7, .5)], fill=color, width=w)
    elif name in ('vol', 'mute'):
        d.polygon([P(.22, .42), P(.32, .42), P(.46, .28), P(.46, .72), P(.32, .58), P(.22, .58)], fill=color)
        if name == 'vol':
            d.arc([P(.40, .36), P(.62, .64)], -55, 55, fill=color, width=w)
            d.arc([P(.40, .26), P(.76, .74)], -55, 55, fill=color, width=w)
        else:
            d.line([P(.56, .40), P(.76, .60)], fill=color, width=w)
            d.line([P(.76, .40), P(.56, .60)], fill=color, width=w)
    elif name == 'open':   # folder
        d.line([P(.24, .70), P(.24, .32), P(.42, .32), P(.48, .38), P(.76, .38), P(.76, .70), P(.24, .70)], fill=color, width=w, joint='curve')
    elif name == 'save':   # download into tray
        d.line([P(.5, .26), P(.5, .58)], fill=color, width=w)
        d.line([P(.37, .46), P(.5, .59), P(.63, .46)], fill=color, width=w, joint='curve')
        d.line([P(.26, .58), P(.26, .74), P(.74, .74), P(.74, .58)], fill=color, width=w, joint='curve')
    elif name == 'shot':   # camera
        d.rounded_rectangle([P(.22, .36), P(.78, .72)], radius=S*.06, outline=color, width=w)
        d.line([P(.40, .36), P(.44, .28), P(.56, .28), P(.60, .36)], fill=color, width=w, joint='curve')
        d.ellipse([P(.41, .43), P(.59, .61)], outline=color, width=w)
    elif name in ('rec', 'recon'):
        if name == 'recon':
            d.ellipse([P(.32, .32), P(.68, .68)], fill=REC)
        else:
            d.ellipse([P(.30, .30), P(.70, .70)], outline=color, width=w)
            d.ellipse([P(.42, .42), P(.58, .58)], fill=color)
    elif name == 'info':
        d.ellipse([P(.26, .26), P(.74, .74)], outline=color, width=w)
        d.line([P(.5, .46), P(.5, .62)], fill=color, width=w)
        d.ellipse([P(.47, .34), P(.53, .40)], fill=color)
    elif name == 'mini':
        d.rounded_rectangle([P(.24, .30), P(.76, .70)], radius=S*.04, outline=color, width=w)
        d.rounded_rectangle([P(.48, .50), P(.70, .64)], radius=S*.02, fill=color)
    elif name in ('loop', 'loop1'):
        d.line([P(.30, .56), P(.30, .40), P(.68, .40)], fill=color, width=w, joint='curve')
        d.polygon([P(.64, .32), P(.74, .40), P(.64, .48)], fill=color)
        d.line([P(.70, .44), P(.70, .60), P(.32, .60)], fill=color, width=w, joint='curve')
        d.polygon([P(.36, .52), P(.26, .60), P(.36, .68)], fill=color)
        if name == 'loop1':
            d.ellipse([P(.60, .58), P(.80, .78)], fill=color)
            d.line([P(.70, .63), P(.70, .73)], fill=BG, width=max(1, w // 2))
    elif name == 'shuffle':
        d.line([P(.24, .36), P(.36, .36), P(.60, .64), P(.70, .64)], fill=color, width=w, joint='curve')
        d.line([P(.24, .64), P(.36, .64), P(.60, .36), P(.70, .36)], fill=color, width=w, joint='curve')
        d.polygon([P(.68, .28), P(.78, .36), P(.68, .44)], fill=color)
        d.polygon([P(.68, .56), P(.78, .64), P(.68, .72)], fill=color)
    elif name == 'menu':
        for x in (.32, .5, .68):
            d.ellipse([P(x-.045, .455), P(x+.045, .545)], fill=color)
    elif name in ('wide', 'narrow'):
        d.line([P(.20, .30), P(.20, .70)], fill=color, width=w)
        d.line([P(.80, .30), P(.80, .70)], fill=color, width=w)
        if name == 'wide':
            d.line([P(.30, .5), P(.70, .5)], fill=color, width=w)
            d.polygon([P(.28, .5), P(.38, .40), P(.38, .60)], fill=color)
            d.polygon([P(.72, .5), P(.62, .40), P(.62, .60)], fill=color)
        else:
            d.line([P(.28, .5), P(.42, .5)], fill=color, width=w)
            d.line([P(.58, .5), P(.72, .5)], fill=color, width=w)
            d.polygon([P(.46, .5), P(.36, .40), P(.36, .60)], fill=color)
            d.polygon([P(.54, .5), P(.64, .40), P(.64, .60)], fill=color)
    elif name in ('chevd', 'chevu'):
        a, b = (.40, .60) if name == 'chevd' else (.60, .40)
        d.line([P(.32, a), P(.5, b), P(.68, a)], fill=color, width=w, joint='curve')
    elif name == 'stop':
        d.rounded_rectangle([P(.32, .32), P(.68, .68)], radius=S*.04, fill=color)
    return im.resize((size, size), Image.LANCZOS)

def pill(wh, color, radius):
    W, H = wh
    im = Image.new('RGBA', (W*SS, H*SS), CLEAR)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, W*SS-1, H*SS-1], radius=radius*SS, fill=color)
    return im.resize((W, H), Image.LANCZOS)

# states: up / over / down. Names ending in 'on' (active toggle) render in accent.
ACTIVE = {'pinon', 'loop1on', 'loopon', 'shuffleon', 'recon'}
def button_sheet(names, w, h, iconsz, circle=False, filled_play=False):
    w, h, iconsz = S(w), S(h), S(iconsz)
    sheet = Image.new('RGBA', (w * len(names), h * 3), CLEAR)
    for i, n in enumerate(names):
        base = n[:-2] if n in ('loopon', 'loop1on', 'shuffleon') else n
        for row in range(3):
            cell = Image.new('RGBA', (w, h), BG)  # opaque bg: VLC renders semi-transparent PNG edges badly
            if filled_play:
                bgc = [TXT, (255, 255, 255, 255), ACC][row]
                cell.alpha_composite(pill((w, h), bgc, min(w, h) // 2))
                fgc = BG if row < 2 else (255, 255, 255, 255)
            else:
                active = n in ACTIVE
                fgc = [ACC if active else (178, 182, 190, 255), ACC if active else TXT, ACC][row]
                if row > 0:
                    cell.alpha_composite(pill((w, h), SURF, min(w, h) // 2 if circle else S(7)))
                if n == 'close' and row > 0:
                    cell = Image.new('RGBA', (w, h), BG)
                    cell.alpha_composite(pill((w, h), (232, 17, 35, 255), S(7)))
                    fgc = (255, 255, 255, 255)
            ic = icon(base, iconsz, fgc)
            cell.alpha_composite(ic, ((w - iconsz) // 2, (h - iconsz) // 2))
            sheet.alpha_composite(cell, (i * w, row * h))
    return sheet

bitmaps = []
def save(img, fname, native=False):
    if not native:
        img = img.resize((SC(img.width), SC(img.height)), Image.NEAREST)
    img.save(os.path.join(SKIN, fname))

def add_sheet(bid, fname, names, w, h, iconsz, **kw):
    save(button_sheet(names, w, h, iconsz, **kw), fname, native=True)
    subs = []
    for i, n in enumerate(names):
        for row, suf in enumerate(['', 'H', 'A']):
            subs.append(f'    <SubBitmap id="{bid}_{n}{suf}" x="@{i*S(w)}" y="@{row*S(h)}" width="@{S(w)}" height="@{S(h)}"/>')
    bitmaps.append(f'  <Bitmap id="{bid}" file="{fname}" alphacolor="#FF00FF">\n' + '\n'.join(subs) + '\n  </Bitmap>')

TOPN = ['close', 'min', 'max', 'restore', 'fs', 'pin', 'pinon', 'list', 'add', 'vol', 'mute', 'fsoff',
        'open', 'save', 'shot', 'rec', 'recon', 'info', 'mini', 'loop', 'loopon', 'loop1on', 'shuffle', 'shuffleon', 'stop', 'menu', 'chevd', 'chevu']
add_sheet('t', 'top.png', TOPN, 34, 28, 30)
add_sheet('m', 'media.png', ['prev', 'next', 'stop'], 38, 38, 30, circle=True)
add_sheet('p', 'play.png', ['play', 'pause'], 44, 44, 26, filled_play=True)
add_sheet('ft', 'fstop.png', ['vol', 'mute', 'fsoff', 'shot', 'loop', 'loopon', 'loop1on', 'shuffle', 'shuffleon', 'list', 'menu', 'wide', 'narrow'], 40, 36, 38)
add_sheet('fm', 'fsmedia.png', ['prev', 'next', 'stop'], 46, 46, 36, circle=True)
add_sheet('s', 'tiny.png', ['chevd', 'close', 'max', 'wide', 'narrow'], 20, 14, 20)
add_sheet('sw', 'switch.png', ['wide', 'narrow'], 28, 24, 34)
add_sheet('fp', 'fsplay.png', ['play', 'pause'], 56, 56, 32, filled_play=True)

# transparent 1px (for overlay checkbox trick)
save(Image.new('RGBA', (1, 1), MAG), 'tp.png')
bitmaps.append('  <Bitmap id="tp" file="tp.png" alphacolor="#FF00FF"/>')

R = 12
def corners(bid, color, r):
    rr = S(r); Z = rr * 2
    im = Image.new('RGBA', (Z * SS, Z * SS), MAG)
    ImageDraw.Draw(im).ellipse([0, 0, Z * SS - 1, Z * SS - 1], fill=color)
    im = im.resize((Z, Z), Image.LANCZOS)
    # hard alpha for alphacolor keying: blend edge into bg-ish, keep magenta outside
    px = im.load()
    for yy in range(Z):
        for xx in range(Z):
            r_, g_, b_, a_ = px[xx, yy]
            px[xx, yy] = MAG if (r_ > 120 and b_ > 120 and g_ < 100) else color
    save(im, f'{bid}.png', native=True)
    bitmaps.append(
        f'  <Bitmap id="{bid}" file="{bid}.png" alphacolor="#FF00FF">\n'
        f'    <SubBitmap id="{bid}_tl" x="@0" y="@0" width="@{rr}" height="@{rr}"/>\n'
        f'    <SubBitmap id="{bid}_tr" x="@{rr}" y="@0" width="@{rr}" height="@{rr}"/>\n'
        f'    <SubBitmap id="{bid}_bl" x="@0" y="@{rr}" width="@{rr}" height="@{rr}"/>\n'
        f'    <SubBitmap id="{bid}_br" x="@{rr}" y="@{rr}" width="@{rr}" height="@{rr}"/>\n  </Bitmap>')
corners('cor', BG, R)

g = Image.new('RGBA', (16, 16), BG)
gd = ImageDraw.Draw(g)
for (x, y) in [(11, 5), (8, 8), (11, 8), (5, 11), (8, 11), (11, 11)]:
    gd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(80, 83, 92, 255))
save(g, 'grip.png')
bitmaps.append('  <Bitmap id="grip" file="grip.png" alphacolor="#FF00FF"/>')

def thumbs(bid, d0):
    d = S(d0)
    sheet = Image.new('RGBA', (d * 3, d), CLEAR)
    for i, (dd, col) in enumerate([(d - S(4), TXT), (d, (255, 255, 255, 255)), (d, ACC)]):
        c = Image.new('RGBA', (d * SS, d * SS), CLEAR)
        o = (d - dd) * SS // 2
        ImageDraw.Draw(c).ellipse([o, o, d * SS - o - 1, d * SS - o - 1], fill=col)
        sheet.alpha_composite(c.resize((d, d), Image.LANCZOS), (i * d, 0))
    save(sheet, f'{bid}.png', native=True)
    bitmaps.append(
        f'  <Bitmap id="{bid}" file="{bid}.png" alphacolor="#FF00FF">\n'
        f'    <SubBitmap id="{bid}_u" x="@0" y="@0" width="@{d}" height="@{d}"/>\n'
        f'    <SubBitmap id="{bid}_o" x="@{d}" y="@0" width="@{d}" height="@{d}"/>\n'
        f'    <SubBitmap id="{bid}_d" x="@{2*d}" y="@0" width="@{d}" height="@{d}"/>\n  </Bitmap>')
thumbs('th', 14)
thumbs('thf', 20)

v6, v40 = S(6), S(40)
vs = Image.new('RGBA', (3 * v6, v40), CLEAR)
for i, col in enumerate([(70, 73, 82, 255), (110, 114, 124, 255), ACC]):
    vs.alpha_composite(pill((v6, v40), col, max(1, v6 // 2)), (i * v6, 0))
save(vs, 'vthumb.png', native=True)
bitmaps.append('  <Bitmap id="vthumb" file="vthumb.png" alphacolor="#FF00FF">\n'
               f'    <SubBitmap id="vthumb_u" x="@0" y="@0" width="@{v6}" height="@{v40}"/>\n'
               f'    <SubBitmap id="vthumb_o" x="@{v6}" y="@0" width="@{v6}" height="@{v40}"/>\n'
               f'    <SubBitmap id="vthumb_d" x="@{2*v6}" y="@0" width="@{v6}" height="@{v40}"/>\n  </Bitmap>')

def progress(bid, W, H, bh, N, fillc=ACC, bgc=BG):
    W, H, bh = S(W), S(H), max(1, S(bh))
    im = Image.new('RGBA', (W, H * N), bgc)
    d = ImageDraw.Draw(im)
    y0 = (H - bh) // 2
    for i in range(N):
        top = i * H + y0
        d.rectangle([0, top, W - 1, top + bh - 1], fill=TRK)
        fw = round(W * i / (N - 1))
        if fw > 0:
            d.rectangle([0, top, fw - 1, top + bh - 1], fill=fillc)
    save(im, f'{bid}.png', native=True)
    bitmaps.append(f'  <Bitmap id="{bid}" file="{bid}.png" alphacolor="#FF00FF"/>')
    return N

fills = {}
def fill(color_id, color, w, h):
    key = (color_id, w, h)
    if key not in fills:
        bid = f'{color_id}_{w}x{h}'
        save(Image.new('RGBA', (w, h), color), f'{bid}.png')
        bitmaps.append(f'  <Bitmap id="{bid}" file="{bid}.png" alphacolor="#FF00FF"/>')
        fills[key] = bid
    return fills[key]

def frame2(prefix, w, h, r=R, resizable=True):
    c = fill('bg', BG, w, h - 2 * r)
    t = fill('bg', BG, w - 2 * r, r)
    br_action = ' action="resizeSE"' if resizable else ' action="move"'
    return f'''
      <Image id="{prefix}.bgC" x="0" y="{r}" image="{c}" action="move" resize="scale" lefttop="lefttop" rightbottom="rightbottom"/>
      <Image id="{prefix}.bgT" x="{r}" y="0" image="{t}" action="move" resize="scale" lefttop="lefttop" rightbottom="righttop"/>
      <Image id="{prefix}.bgB" x="{r}" y="{h-r}" image="{t}" action="move" resize="scale" lefttop="leftbottom" rightbottom="rightbottom"/>
      <Image id="{prefix}.cTL" x="0" y="0" image="cor_tl" action="move"/>
      <Image id="{prefix}.cTR" x="{w-r}" y="0" image="cor_tr" action="move" lefttop="righttop" rightbottom="righttop"/>
      <Image id="{prefix}.cBL" x="0" y="{h-r}" image="cor_bl" action="move" lefttop="leftbottom" rightbottom="leftbottom"/>
      <Image id="{prefix}.cBR" x="{w-r}" y="{h-r}" image="cor_br"{br_action} lefttop="rightbottom" rightbottom="rightbottom"/>'''

PAD = 6
def resize_handles(prefix, w, h, top):
    e = fill('bg', BG, PAD, h - top - 16)
    s = fill('bg', BG, w - 16 - R, PAD)
    return f'''
      <Image id="{prefix}.rE" x="{w-PAD}" y="{top}" image="{e}" action="resizeE" resize="scale" lefttop="righttop" rightbottom="rightbottom"/>
      <Image id="{prefix}.rS" x="{R}" y="{h-PAD}" image="{s}" action="resizeS" resize="scale" lefttop="leftbottom" rightbottom="rightbottom"/>
      <Image id="{prefix}.rSE" x="{w-16}" y="{h-16}" image="grip" action="resizeSE" lefttop="rightbottom" rightbottom="rightbottom"/>'''

RT = 'lefttop="righttop" rightbottom="righttop"'

def repeat_shuffle(p, sheet, x, y, step, anchors=''):
    """loop-all / loop-one (overlay) / shuffle, same logic as VeLoCity"""
    return f'''
      <Checkbox id="{p}.loop" x="{x}" y="{y}" state="playlist.isLoop" up1="{sheet}_loop" over1="{sheet}_loopH" down1="{sheet}_loopA" up2="{sheet}_loopon" over2="{sheet}_looponH" down2="{sheet}_looponA" action1="playlist.setLoop(true)" action2="playlist.setLoop(false);playlist.setRepeat(true)" tooltiptext1="Répéter : non" tooltiptext2="Répéter : tout" {anchors}/>
      <Checkbox id="{p}.loop1" x="{x}" y="{y}" state="playlist.isRepeat" up1="tp" up2="{sheet}_loop1on" over2="{sheet}_loop1onH" down2="{sheet}_loop1onA" action1="playlist.setRepeat(true)" action2="playlist.setRepeat(false);playlist.setLoop(false)" tooltiptext2="Répéter : ce fichier" {anchors}/>
      <Checkbox id="{p}.rand" x="{x+step}" y="{y}" state="playlist.isRandom" up1="{sheet}_shuffle" over1="{sheet}_shuffleH" down1="{sheet}_shuffleA" up2="{sheet}_shuffleon" over2="{sheet}_shuffleonH" down2="{sheet}_shuffleonA" action1="playlist.setRandom(true)" action2="playlist.setRandom(false)" tooltiptext1="Aléatoire : non" tooltiptext2="Aléatoire : oui" {anchors}/>'''

# ---------------- MAIN WINDOW ----------------
W, H = 960, 600
TOP, BOT = 40, 88
VW, VH = W - 2 * PAD, H - TOP - BOT
TS_X, TS_W = 74, W - 74 - 86
NT = progress('prog', TS_W, 24, 4, 240)
progress('vprog', 90, 24, 4, 50, fillc=TXT)
vidbg = fill('vid', VID, VW, VH)
bx = lambda i: W - 8 - 34 * (i + 1)   # right-aligned top buttons
lx = lambda i: 8 + 34 * i             # left-aligned top buttons
CW = 38 + 8 + 38 + 8 + 44 + 8 + 38    # stop prev play next
main_layout = f'''
    <Layout id="mainL" width="{W}" height="{H}" minwidth="640" maxwidth="99999" minheight="340" maxheight="99999">{frame2('m', W, H)}
      <Button id="m.open" x="{lx(0)}" y="6" up="t_open" over="t_openH" down="t_openA" action="dialogs.prefs()" tooltiptext="Paramètres"/>
      <Button id="m.save" x="{lx(1)}" y="6" up="t_save" over="t_saveH" down="t_saveA" action="playlist.save()" tooltiptext="Enregistrer la playlist"/>
      <Button id="m.shot" x="{lx(2)}" y="6" up="t_shot" over="t_shotH" down="t_shotA" action="vlc.snapshot()" tooltiptext="Capture d'écran" visible="vlc.hasVout"/>
      <Checkbox id="m.rec" x="{lx(3)}" y="6" state="vlc.isRecording" up1="t_rec" over1="t_recH" down1="t_recA" up2="t_recon" over2="t_reconH" down2="t_reconA" action1="vlc.toggleRecord()" action2="vlc.toggleRecord()" tooltiptext1="Enregistrer (record)" tooltiptext2="Arrêter l'enregistrement" visible="vlc.isPlaying or vlc.isPaused"/>
      <Button id="m.info" x="{lx(4)}" y="6" up="t_info" over="t_infoH" down="t_infoA" action="dialogs.fileInfo()" tooltiptext="Infos sur le média" visible="vlc.isPlaying or vlc.isPaused"/>

      <Checkbox id="m.pin" x="{bx(5)}" y="6" state="vlc.isOnTop" up1="t_pin" over1="t_pinH" down1="t_pinA" up2="t_pinon" over2="t_pinonH" down2="t_pinonA" action1="vlc.onTop()" action2="vlc.onTop()" tooltiptext1="Toujours au premier plan" tooltiptext2="Désactiver premier plan" {RT}/>
      <Button id="m.mini" x="{bx(4)}" y="6" up="t_mini" over="t_miniH" down="t_miniA" action="player.hide();mini.setLayout(miniV);mini.show();vlc.onTop()" tooltiptext="Mini lecteur (épinglé)" {RT}/>
      <Button id="m.min" x="{bx(3)}" y="6" up="t_min" over="t_minH" down="t_minA" action="vlc.minimize()" tooltiptext="Réduire" {RT}/>
      <Checkbox id="m.max" x="{bx(2)}" y="6" state="player.isMaximized" up1="t_max" over1="t_maxH" down1="t_maxA" up2="t_restore" over2="t_restoreH" down2="t_restoreA" action1="player.maximize()" action2="player.unmaximize()" tooltiptext1="Agrandir" tooltiptext2="Restaurer" {RT}/>
      <Button id="m.fs" x="{bx(1)}" y="6" up="t_fs" over="t_fsH" down="t_fsA" action="vlc.fullscreen()" tooltiptext="Plein écran (F)" {RT}/>
      <Button id="m.close" x="{bx(0)}" y="6" up="t_close" over="t_closeH" down="t_closeA" action="vlc.quit()" tooltiptext="Quitter" {RT}/>

      <Image id="m.vbg" x="{PAD}" y="{TOP}" image="{vidbg}" resize="scale" lefttop="lefttop" rightbottom="rightbottom"/>
      <Text id="m.audio" x="{PAD+20}" y="{TOP+VH//2-12}" width="{VW-40}" text="$N" font="f18" color="{hexc(MUT)}" alignment="center" scrolling="none" lefttop="lefttop" rightbottom="rightbottom" visible="not vlc.hasVout"/>
      <Video id="m.video" x="{PAD}" y="{TOP}" width="{VW}" height="{VH}" autoresize="false" lefttop="lefttop" rightbottom="rightbottom"/>

      <Panel id="m.bottom" x="0" y="{H-BOT}" width="{W}" height="{BOT}" lefttop="leftbottom" rightbottom="rightbottom">
        <Text id="m.tcur" x="12" y="10" width="54" text="$T" font="f12" color="{hexc(TXT)}" alignment="right"/>
        <Slider id="m.time" x="{TS_X}" y="6" points="(0,12),({TS_W},12)" thickness="12" value="time" up="th_u" over="th_o" down="th_d" tooltiptext="$T / $D" lefttop="lefttop" rightbottom="righttop">
          <SliderBackground id="m.timeBG" image="prog" nbvert="{NT}"/>
        </Slider>
        <Text id="m.tleft" x="{W-80}" y="10" width="70" text="-$L" font="f12" color="{hexc(TXT)}" {RT}/>
        <Text id="m.tdur" x="20" y="44" width="150" text="Durée  $D" font="f12" color="{hexc(MUT)}"/>
        <Text id="m.title" x="20" y="62" width="300" text="$N" font="f11" color="{hexc(MUT)}" scrolling="none"/>
        <Panel id="m.ctr" x="{(W-CW)//2}" y="34" width="{CW}" height="44" rightbottom="righttop">
          <Panel id="m.ctr2" width="{CW}" height="44" rightbottom="righttop" xkeepratio="true">
            <Button id="m.stop" x="0" y="3" up="m_stop" over="m_stopH" down="m_stopA" action="vlc.stop()" tooltiptext="Stop"/>
            <Button id="m.prev" x="46" y="3" up="m_prev" over="m_prevH" down="m_prevA" action="playlist.previous()" tooltiptext="Précédent"/>
            <Checkbox id="m.play" x="92" y="0" state="vlc.isPlaying" up1="p_play" over1="p_playH" down1="p_playA" up2="p_pause" over2="p_pauseH" down2="p_pauseA" action1="vlc.play()" action2="vlc.pause()" tooltiptext1="Lecture (Espace)" tooltiptext2="Pause (Espace)"/>
            <Button id="m.next" x="144" y="3" up="m_next" over="m_nextH" down="m_nextA" action="playlist.next()" tooltiptext="Suivant"/>
          </Panel>
        </Panel>
        <Panel id="m.right" x="{W-20-90-8-34*4}" y="42" width="{90+8+34*4}" height="30" lefttop="righttop" rightbottom="righttop">{repeat_shuffle('m', 't', 0, 0, 34)}
          <Checkbox id="m.pl" x="68" y="0" state="plWin.isVisible" up1="t_list" over1="t_listH" down1="t_listA" up2="t_listA" over2="t_listH" down2="t_list" action1="plWin.show()" action2="plWin.hide()" tooltiptext1="Afficher la playlist" tooltiptext2="Masquer la playlist"/>
          <Checkbox id="m.mute" x="102" y="0" state="vlc.isMute" up1="t_vol" over1="t_volH" down1="t_volA" up2="t_mute" over2="t_muteH" down2="t_muteA" action1="vlc.mute()" action2="vlc.mute()" tooltiptext1="Couper le son" tooltiptext2="Rétablir le son"/>
          <Slider id="m.vol" x="144" y="2" points="(0,12),(90,12)" thickness="10" value="volume" up="th_u" over="th_o" down="th_d" tooltiptext="Volume $V%">
            <SliderBackground id="m.volBG" image="vprog" nbvert="50"/>
          </Slider>
        </Panel>
      </Panel>{resize_handles('m', W, H, TOP)}
    </Layout>'''

# ---------------- MINI PLAYER (video, 2 layouts) ----------------
MW, MH = 480, 300
def flat_bg(prefix, w, h):
    c = fill('bg', BG, w, h)
    return f"""
      <Image id="{prefix}.bg" x="0" y="0" image="{c}" action="move" resize="scale" lefttop="lefttop" rightbottom="rightbottom"/>"""
def mini_resize(prefix, w, h, top):
    e = fill('bg', BG, PAD, h - top - 16)
    s = fill('bg', BG, w - 16, PAD)
    return f"""
      <Image id="{prefix}.rE" x="{w-PAD}" y="{top}" image="{e}" action="resizeE" resize="scale" lefttop="righttop" rightbottom="rightbottom"/>
      <Image id="{prefix}.rS" x="0" y="{h-PAD}" image="{s}" action="resizeS" resize="scale" lefttop="leftbottom" rightbottom="rightbottom"/>
      <Image id="{prefix}.rSE" x="{w-16}" y="{h-16}" image="grip" action="resizeSE" lefttop="rightbottom" rightbottom="rightbottom"/>"""

# layout A: video only (default). 16px top strip: drag, double-click = show controls
VS = 16
mv_vid = fill('vid', VID, MW - 2*PAD, MH - VS - PAD)
gl = Image.new('RGBA', (40, VS), BG); ImageDraw.Draw(gl).rounded_rectangle([0, 6, 39, 9], radius=2, fill=(70, 73, 82, 255))
save(gl, 'handle.png'); bitmaps.append('  <Bitmap id="handle" file="handle.png" alphacolor="#FF00FF"/>')
miniV = f"""
    <Layout id="miniV" width="{MW}" height="{MH}" minwidth="200" maxwidth="99999" minheight="120" maxheight="99999">{flat_bg('mv', MW, MH)}
      <Image id="mv.handle" x="{(MW-40)//2}" y="0" image="handle" action="move" action2="mini.setLayout(miniL)" lefttop="lefttop" rightbottom="righttop" xkeepratio="true"/>
      <Button id="mv.show" x="4" y="1" up="s_chevd" over="s_chevdH" down="s_chevdA" action="mini.setLayout(miniL)" tooltiptext="Afficher les contrôles (ou double-clic sur la barre)"/>
      <Button id="mv.back" x="{MW-48}" y="1" up="s_max" over="s_maxH" down="s_maxA" action="mini.hide();player.show();vlc.onTop()" tooltiptext="Lecteur complet" {RT}/>
      <Button id="mv.close" x="{MW-24}" y="1" up="s_close" over="s_closeH" down="s_closeA" action="vlc.quit()" tooltiptext="Quitter" {RT}/>
      <Image id="mv.vbg" x="{PAD}" y="{VS}" image="{mv_vid}" resize="scale" lefttop="lefttop" rightbottom="rightbottom"/>
      <Text id="mv.audio" x="{PAD+10}" y="{VS+(MH-VS)//2-10}" width="{MW-2*PAD-20}" text="$N" font="f13" color="{hexc(MUT)}" alignment="center" scrolling="none" lefttop="lefttop" rightbottom="rightbottom" visible="not vlc.hasVout"/>
      <Video id="mv.video" x="{PAD}" y="{VS}" width="{MW-2*PAD}" height="{MH-VS-PAD}" autoresize="false" lefttop="lefttop" rightbottom="rightbottom"/>{mini_resize('mv', MW, MH, VS)}
    </Layout>"""

# layout B: video + controls
MT, MB = 32, 80
ml_vid = fill('vid', VID, MW - 2*PAD, MH - MT - MB)
MS_X, MS_W = 64, MW - 64 - 70
progress('mprog', MS_W, 20, 4, 200)
MCW = 38 + 6 + 44 + 6 + 38
miniL = f"""
    <Layout id="miniL" width="{MW}" height="{MH + 0}" minwidth="360" maxwidth="99999" minheight="200" maxheight="99999">{flat_bg('ml', MW, MH)}
      <Button id="ml.hide" x="4" y="2" up="t_chevu" over="t_chevuH" down="t_chevuA" action="mini.setLayout(miniV)" tooltiptext="Masquer les contrôles"/>
      <Checkbox id="ml.pin" x="{MW-4-34*3}" y="2" state="vlc.isOnTop" up1="t_pin" over1="t_pinH" down1="t_pinA" up2="t_pinon" over2="t_pinonH" down2="t_pinonA" action1="vlc.onTop()" action2="vlc.onTop()" tooltiptext1="Épingler" tooltiptext2="Désépingler" {RT}/>
      <Button id="ml.back" x="{MW-4-34*2}" y="2" up="t_max" over="t_maxH" down="t_maxA" action="mini.hide();player.show();vlc.onTop()" tooltiptext="Lecteur complet" {RT}/>
      <Button id="ml.close" x="{MW-4-34}" y="2" up="t_close" over="t_closeH" down="t_closeA" action="vlc.quit()" tooltiptext="Quitter" {RT}/>
      <Image id="ml.vbg" x="{PAD}" y="{MT}" image="{ml_vid}" resize="scale" lefttop="lefttop" rightbottom="rightbottom"/>
      <Text id="ml.audio" x="{PAD+10}" y="{MT+(MH-MT-MB)//2-10}" width="{MW-2*PAD-20}" text="$N" font="f13" color="{hexc(MUT)}" alignment="center" scrolling="none" lefttop="lefttop" rightbottom="rightbottom" visible="not vlc.hasVout"/>
      <Video id="ml.video" x="{PAD}" y="{MT}" width="{MW-2*PAD}" height="{MH-MT-MB}" autoresize="false" lefttop="lefttop" rightbottom="rightbottom"/>
      <Panel id="ml.bottom" x="0" y="{MH-MB}" width="{MW}" height="{MB}" lefttop="leftbottom" rightbottom="rightbottom">
        <Text id="ml.tcur" x="4" y="8" width="56" text="$T" font="f11" color="{hexc(TXT)}" alignment="right"/>
        <Slider id="ml.time" x="{MS_X}" y="4" points="(0,10),({MS_W},10)" thickness="10" value="time" up="th_u" over="th_o" down="th_d" tooltiptext="$T / $D" lefttop="lefttop" rightbottom="righttop">
          <SliderBackground id="ml.timeBG" image="mprog" nbvert="200"/>
        </Slider>
        <Text id="ml.tleft" x="{MW-66}" y="8" width="62" text="-$L" font="f11" color="{hexc(TXT)}" {RT}/>
        <Panel id="ml.ctr" x="{(MW-MCW)//2}" y="28" width="{MCW}" height="44" rightbottom="righttop">
          <Panel id="ml.ctr2" width="{MCW}" height="44" rightbottom="righttop" xkeepratio="true">
            <Button id="ml.prev" x="0" y="3" up="m_prev" over="m_prevH" down="m_prevA" action="playlist.previous()" tooltiptext="Précédent"/>
            <Checkbox id="ml.play" x="44" y="0" state="vlc.isPlaying" up1="p_play" over1="p_playH" down1="p_playA" up2="p_pause" over2="p_pauseH" down2="p_pauseA" action1="vlc.play()" action2="vlc.pause()" tooltiptext1="Lecture" tooltiptext2="Pause"/>
            <Button id="ml.next" x="94" y="3" up="m_next" over="m_nextH" down="m_nextA" action="playlist.next()" tooltiptext="Suivant"/>
          </Panel>
        </Panel>
        <Checkbox id="ml.mute" x="{MW-20-34}" y="36" state="vlc.isMute" up1="t_vol" over1="t_volH" down1="t_volA" up2="t_mute" over2="t_muteH" down2="t_muteA" action1="vlc.mute()" action2="vlc.mute()" tooltiptext1="Couper le son" tooltiptext2="Rétablir le son" {RT}/>
        {repeat_shuffle('ml', 't', 10, 36, 34)}
      </Panel>{mini_resize('ml', MW, MH, MT)}
    </Layout>"""
mini_layout = miniV + miniL

# ---------------- PLAYLIST ----------------
PW, PH = 380, 560
pl_layout = f'''
    <Layout id="plL" width="{PW}" height="{PH}" minwidth="280" maxwidth="99999" minheight="240" maxheight="99999">{frame2('pl', PW, PH)}
      <Text id="pl.title" x="18" y="12" width="150" text="Playlist" font="f13" color="{hexc(TXT)}"/>
      <Button id="pl.add" x="{PW-8-34*3}" y="6" up="t_add" over="t_addH" down="t_addA" action="playlist.add()" tooltiptext="Ajouter des fichiers" {RT}/>
      <Button id="pl.save" x="{PW-8-34*2}" y="6" up="t_save" over="t_saveH" down="t_saveA" action="playlist.save()" tooltiptext="Enregistrer la playlist" {RT}/>
      <Button id="pl.close" x="{PW-8-34}" y="6" up="t_close" over="t_closeH" down="t_closeA" action="plWin.hide()" tooltiptext="Fermer" {RT}/>
      <Playtree id="pl.tree" x="12" y="44" width="{PW-36}" height="{PH-44-18}" font="f12" flat="true" bgcolor1="{hexc(BG)}" bgcolor2="#181A1D" fgcolor="{hexc(MUT)}" selcolor="#2A2C33" playcolor="{hexc(ACC)}" lefttop="lefttop" rightbottom="rightbottom">
        <Slider id="pl.scroll" x="{PW-20}" y="48" points="(3,{PH-44-18-48}),(3,0)" thickness="6" up="vthumb_u" over="vthumb_o" down="vthumb_d" lefttop="righttop" rightbottom="rightbottom"/>
      </Playtree>{resize_handles('pl', PW, PH, 40)}
    </Layout>'''

# ---------------- FULLSCREEN CONTROLLER (card + full-width bar pinned bottom) ----------------
FS_H = 116
TO_W = 'fullscreenController.setLayout(fcW);fullscreenController.maximize()'
TO_L = 'fullscreenController.unmaximize();fullscreenController.setLayout(fcL)'
def fs_bar(p, FS_W, wide):
    FTS_X, FTS_W = 116, FS_W - 116 - 124
    nft = progress(f'{p}prog', FTS_W, 30, 6, 300)
    progress(f'{p}vprog', 110, 30, 6, 50, fillc=TXT)
    FCW = 46 + 12 + 46 + 12 + 56 + 12 + 46
    fcx = (FS_W - FCW) // 2
    fx = FS_W - 28
    A = RT if wide else ''
    xl = fx - 40 - 12 - 110 - 6 - 40 - 12 - 44 - 44
    if wide:
        bg = flat_bg(p, FS_W, FS_H)
        tog = f'<Button id="{p}.sw" x="{FS_W-32}" y="{FS_H-28}" up="sw_narrow" over="sw_narrowH" down="sw_narrowA" action="{TO_L}" tooltiptext="Revenir à la barre flottante" lefttop="rightbottom" rightbottom="rightbottom"/>'
    else:
        bg = frame2(p, FS_W, FS_H, resizable=False)
        tog = f'<Button id="{p}.sw" x="{FS_W-32}" y="{FS_H-28}" up="sw_wide" over="sw_wideH" down="sw_wideA" action="{TO_W}" tooltiptext="Barre pleine largeur, épinglée en bas"/>'
    return f"""{bg}
      <Text id="{p}.tcur" x="10" y="16" width="96" text="$T" font="f16" color="{hexc(TXT)}" alignment="right"/>
      <Slider id="{p}.time" x="{FTS_X}" y="10" points="(0,15),({FTS_W},15)" thickness="16" value="time" up="thf_u" over="thf_o" down="thf_d" tooltiptext="$T / $D" lefttop="lefttop" rightbottom="righttop">
        <SliderBackground id="{p}.timeBG" image="{p}prog" nbvert="{nft}"/>
      </Slider>
      <Text id="{p}.tleft" x="{FS_W-112}" y="16" width="100" text="-$L" font="f16" color="{hexc(TXT)}" {RT}/>
      <Text id="{p}.tdur" x="30" y="58" width="240" text="Durée  $D" font="f14" color="{hexc(MUT)}"/>
      <Text id="{p}.title" x="30" y="82" width="300" text="$N" font="f12" color="{hexc(MUT)}" scrolling="none"/>
      <Panel id="{p}.ctr" x="{fcx}" y="51" width="{FCW}" height="56" rightbottom="righttop">
        <Panel id="{p}.ctr2" width="{FCW}" height="56" rightbottom="righttop" xkeepratio="true">
          <Button id="{p}.stop" x="0" y="5" up="fm_stop" over="fm_stopH" down="fm_stopA" action="vlc.stop()" tooltiptext="Stop"/>
          <Button id="{p}.prev" x="58" y="5" up="fm_prev" over="fm_prevH" down="fm_prevA" action="playlist.previous()" tooltiptext="Précédent"/>
          <Checkbox id="{p}.play" x="116" y="0" state="vlc.isPlaying" up1="fp_play" over1="fp_playH" down1="fp_playA" up2="fp_pause" over2="fp_pauseH" down2="fp_pauseA" action1="vlc.play()" action2="vlc.pause()" tooltiptext1="Lecture" tooltiptext2="Pause"/>
          <Button id="{p}.next" x="184" y="5" up="fm_next" over="fm_nextH" down="fm_nextA" action="playlist.next()" tooltiptext="Suivant"/>
        </Panel>
      </Panel>
      {repeat_shuffle(p, 'ft', xl, 61, 44, A)}
      <Checkbox id="{p}.mute" x="{fx-40-12-110-6-40}" y="61" state="vlc.isMute" up1="ft_vol" over1="ft_volH" down1="ft_volA" up2="ft_mute" over2="ft_muteH" down2="ft_muteA" action1="vlc.mute()" action2="vlc.mute()" tooltiptext1="Couper le son" tooltiptext2="Rétablir le son" {A}/>
      <Slider id="{p}.vol" x="{fx-40-12-110}" y="64" points="(0,15),(110,15)" thickness="12" value="volume" up="th_u" over="th_o" down="th_d" tooltiptext="Volume $V%" {A}>
        <SliderBackground id="{p}.volBG" image="{p}vprog" nbvert="50"/>
      </Slider>
      <Button id="{p}.exit" x="{fx-40}" y="61" up="ft_fsoff" over="ft_fsoffH" down="ft_fsoffA" action="{TO_L};vlc.fullscreen()" tooltiptext="Quitter le plein écran (Échap)" {A}/>
      {tog}"""

FW, FWH = 1920, 1080
fs_layout = f"""
    <Layout id="fcL" width="1100" height="{FS_H}" minwidth="1100" maxwidth="1100" minheight="{FS_H}" maxheight="{FS_H}">{fs_bar('fcL', 1100, False)}
    </Layout>
    <Layout id="fcW" width="{FW}" height="{FWH}" minwidth="800" maxwidth="99999" minheight="{FS_H}" maxheight="99999">
      <Panel id="fcW.bar" x="0" y="{FWH-FS_H}" width="{FW}" height="{FS_H}" lefttop="leftbottom" rightbottom="rightbottom">{fs_bar('fcW', FW, True)}
      </Panel>
    </Layout>"""

xml = f'''<!DOCTYPE Theme PUBLIC "-//VideoLAN//DTD VLC Skins V2.0//EN" "skin.dtd">
<Theme version="2.0" magnet="12" alpha="255" movealpha="255">
  <ThemeInfo name="NearDark" author="NearDark contributors" email="" webpage=""/>
{chr(10).join(bitmaps)}
  <Font id="f11" file="roboto.ttf" size="11"/>
  <Font id="f12" file="roboto.ttf" size="12"/>
  <Font id="f13" file="roboto.ttf" size="13"/>
  <Font id="f14" file="roboto.ttf" size="14"/>
  <Font id="f16" file="roboto.ttf" size="16"/>
  <Font id="f18" file="roboto.ttf" size="18"/>

  <Window id="player" x="120" y="80" dragdrop="true" playondrop="true">{main_layout}
  </Window>

  <Window id="mini" x="120" y="80" visible="false" dragdrop="true" playondrop="true">{mini_layout}
  </Window>

  <Window id="plWin" x="1090" y="80" visible="false" dragdrop="true" playondrop="false">{pl_layout}
  </Window>

  <Window id="fullscreenController">{fs_layout}
  </Window>
</Theme>
'''
def _scale(xml):
    def num(m):
        k, v = m.group(1), int(m.group(2))
        if v >= 9999: return f'{k}="{v}"'
        f = SC if k in ('width', 'height', 'minwidth', 'minheight') else S
        return f'{k}="{max(1, f(v)) if k == "size" else f(v)}"'
    xml = re.sub(r'\b(x|y|width|height|minwidth|maxwidth|minheight|maxheight|thickness|size)="(-?\d+)"', num, xml)
    xml = re.sub(r'points="([^"]+)"', lambda m: 'points="' + re.sub(r'-?\d+', lambda n: str(S(int(n.group(0)))), m.group(1)) + '"', xml)
    return xml
def _strip_fs_tooltips(xml):
    a = xml.index('<Window id="fullscreenController"'); b = xml.index('</Window>', a)
    seg = re.sub(r' tooltiptext[12]?="[^"]*"', '', xml[a:b])
    return xml[:a] + seg + xml[b:]
xml = _strip_fs_tooltips(_scale(xml)).replace('="@', '="')
open(os.path.join(SKIN, 'theme.xml'), 'w', encoding='utf-8').write(xml)
vlt = os.path.join(OUT, 'NearDark.vlt')
with tarfile.open(vlt, 'w:gz') as tf:
    for f in sorted(os.listdir(SKIN)):
        tf.add(os.path.join(SKIN, f), arcname=f)
print('ok', vlt, os.path.getsize(vlt))
