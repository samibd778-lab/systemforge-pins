// SystemForge "pro" reel: dark stage, full-width screen with depth, bold word-by-word captions with a
// highlighted keyword, punch zooms, click ripple, floating result badge, whoosh/pop/click SFX track.
// Rules from OpenMontage skills: creative/short-form.md, creative/screen-recording.md, creative/sound-design.md
import React from 'react';
import {AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {ReelSpec, Seg, Cam} from './Reel';

// theme can be overridden per reel with spec.theme (set at the top of ReelPro, read by children in the same render)
let BG1 = '#16130F';
let BG2 = '#2A211A';
let ACC = '#F2A97E';
let ACC2 = '#FFD9BF';
let GLOW = 'rgba(242,169,126,';
const WHITE = '#FFFDF9';
const SOFT = '#CFC5B8';

const FONTS = `
@font-face{font-family:MontX;src:url(${staticFile('montserrat800.woff2')}) format('woff2');font-weight:800}
@font-face{font-family:MontX;src:url(${staticFile('montserrat900.woff2')}) format('woff2');font-weight:900}
@font-face{font-family:InterW;src:url(${staticFile('inter500.woff2')}) format('woff2');font-weight:500}
@font-face{font-family:InterW;src:url(${staticFile('inter700.woff2')}) format('woff2');font-weight:700}
`;

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
const CARD_W = 1000;
const CARD_H = 720;
const CARD_TOP = 480; // card + badge stay inside the vertical safe band (168..1330)
const AR = CARD_H / CARD_W;
export const PRO_END = 3.6;

const starts = (spec: ReelSpec) => {
  const out: number[] = [];
  let acc = 0;
  for (const g of spec.segments) {
    out.push(acc);
    acc += s(g.dur);
  }
  return {starts: out, endStart: acc};
};
export const proFrames = (spec: ReelSpec) => starts(spec).endStart + s(PRO_END);

const camAt = (cams: Seg['cams'], t: number): Cam => {
  if (cams.length === 1 || t <= cams[0].t) return cams[0].cam;
  for (let i = 1; i < cams.length; i++) {
    const a = cams[i - 1];
    const b = cams[i];
    if (t <= b.t) {
      const p = interpolate(t, [a.t, b.t], [0, 1], {easing: Easing.bezier(0.7, 0, 0.2, 1)});
      return {cx: a.cam.cx + (b.cam.cx - a.cam.cx) * p, cy: a.cam.cy + (b.cam.cy - a.cam.cy) * p, w: a.cam.w + (b.cam.w - a.cam.w) * p};
    }
  }
  return cams[cams.length - 1].cam;
};

const Stage: React.FC = () => {
  const f = useCurrentFrame();
  const x = 50 + Math.sin(f / 70) * 8;
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 70% at ${x}% 62%, ${BG2} 0%, ${BG1} 62%)`}}>
      <div style={{position: 'absolute', left: 140, right: 140, top: CARD_TOP + 200, height: 600, borderRadius: 300, background: ACC, opacity: 0.16, filter: 'blur(120px)'}} />
    </AbsoluteFill>
  );
};

const Caption: React.FC<{lines: string[]; instant: boolean}> = ({lines, instant}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  let k = 0;
  return (
    <div style={{position: 'absolute', top: 200, left: 60, right: 60, textAlign: 'center'}}>
      {lines.map((line, li) => (
        <div key={li} style={{fontFamily: li === 0 ? 'MontX' : 'InterW', fontWeight: li === 0 ? 900 : 500, fontSize: li === 0 ? 66 : 40, lineHeight: li === 0 ? 1.08 : 1.25, color: li === 0 ? WHITE : SOFT, letterSpacing: li === 0 ? -1 : 0, marginTop: li === 0 ? 0 : 22}}>
          {line.split(' ').map((raw, wi) => {
            const i = k++;
            const mark = raw.startsWith('*') && raw.endsWith('*');
            const w = raw.replace(/\*/g, '');
            const p = instant && li === 0 ? 1 : spring({frame: frame - 1 - i * 2, fps, config: {damping: 13, stiffness: 210}});
            const m = spring({frame: frame - 8 - i * 2, fps, config: {damping: 15, stiffness: 180}});
            return (
              <span key={wi} style={{display: 'inline-block', marginRight: li === 0 ? 20 : 12, opacity: p, transform: `translateY(${(1 - p) * 30}px) scale(${0.85 + 0.15 * p})`}}>
                {mark ? (
                  <span style={{display: 'inline-block', padding: '0 14px', borderRadius: 14, background: ACC, color: BG1, transform: `rotate(${-2 * m}deg) scale(${0.9 + 0.1 * m})`}}>{w}</span>
                ) : (
                  w
                )}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const Badge: React.FC<{chip: NonNullable<Seg['chip']>}> = ({chip}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < s(chip.from)) return null;
  const p = spring({frame: frame - s(chip.from), fps, config: {damping: 10, stiffness: 190}});
  const tone = chip.tone ?? 'info';
  const bg = tone === 'bad' ? '#FFE1D6' : tone === 'good' ? '#DDF0D2' : WHITE;
  const fg = tone === 'bad' ? '#A3391C' : tone === 'good' ? '#2F5A22' : '#2E2A25';
  return (
    <div style={{position: 'absolute', top: CARD_TOP + CARD_H + 24, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{padding: '20px 44px', borderRadius: 70, background: bg, color: fg, fontFamily: 'MontX', fontWeight: 800, fontSize: 48, boxShadow: '0 24px 60px rgba(0,0,0,.45)', opacity: p, transform: `translateY(${(1 - p) * 40}px) scale(${0.7 + 0.3 * p}) rotate(${(1 - p) * -4}deg)`}}>
        {chip.text}
      </div>
    </div>
  );
};

const Clip: React.FC<{g: Seg; spec: ReelSpec; first: boolean}> = ({g, spec, first}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cam = camAt(g.cams, t);
  const scale = CARD_W / cam.w;
  const h = cam.w * AR;
  const left = -(cam.cx - cam.w / 2) * scale;
  const top = -(cam.cy - h / 2) * scale;
  // entrance: zoom-blur punch in (no slow fades); first frame of the video is already sharp (hook)
  const e = first ? 1 : interpolate(frame, [0, 7], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const blur = (1 - e) * 14;
  const enterScale = 1.08 - 0.08 * e;
  // slow drift so the frame is never static
  const drift = 1 + 0.012 * Math.sin(frame / 22);
  const tilt = first ? interpolate(frame, [0, 26], [7, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}) : 0;

  let ring: React.ReactNode = null;
  let ripple: React.ReactNode = null;
  if (g.ring && t >= g.ring.from - 0.25) {
    const r = g.ring;
    const rf = frame - s(g.ring.from - 0.25);
    const q = interpolate(rf, [0, 18], [0, 1], {extrapolateRight: 'clamp'});
    ripple = (
      <div style={{position: 'absolute', left: left + (r.x + r.w / 2) * scale - 60 * (0.4 + q), top: top + (r.y + r.h / 2) * scale - 60 * (0.4 + q), width: 120 * (0.4 + q), height: 120 * (0.4 + q), borderRadius: 999, border: `5px solid ${ACC}`, opacity: 1 - q}} />
    );
    if (t >= g.ring.from) {
      const rp = spring({frame: frame - s(g.ring.from), fps, config: {damping: 12, stiffness: 160}});
      ring = (
        <div style={{position: 'absolute', left: left + (r.x - 8) * scale, top: top + (r.y - 6) * scale, width: (r.w + 16) * scale, height: (r.h + 12) * scale, border: `5px solid ${ACC}`, borderRadius: 16, boxShadow: `0 0 0 ${12 * rp}px ${GLOW}.25), 0 0 40px ${GLOW}.5)`, opacity: rp, transform: `scale(${1.3 - 0.3 * rp})`}} />
      );
    }
  }

  return (
    <AbsoluteFill>
      <Caption lines={g.caption} instant={first} />
      <div style={{position: 'absolute', left: (1080 - CARD_W) / 2, top: CARD_TOP, width: CARD_W, height: CARD_H, perspective: 1800}}>
        <div
          style={{
            width: CARD_W,
            height: CARD_H,
            borderRadius: 30,
            overflow: 'hidden',
            background: '#fff',
            border: '2px solid rgba(255,255,255,.10)',
            boxShadow: '0 50px 120px rgba(0,0,0,.6)',
            transform: `rotateX(${tilt}deg) scale(${enterScale * drift})`,
            filter: blur > 0.2 ? `blur(${blur}px)` : undefined,
            opacity: 0.4 + 0.6 * e,
          }}
        >
          <OffthreadVideo src={staticFile(spec.video)} trimBefore={s(g.src)} playbackRate={g.rate ?? 1} muted style={{position: 'absolute', left, top, width: spec.videoW * scale, height: spec.videoH * scale, maxWidth: 'none'}} />
          {ripple}
          {ring}
        </div>
      </div>
      {g.chip ? <Badge chip={g.chip} /> : null}
    </AbsoluteFill>
  );
};

const End: React.FC<{end: ReelSpec['end']}> = ({end}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame, fps, config: {damping: 14}});
  const b = spring({frame: frame - 8, fps, config: {damping: 14}});
  const c = spring({frame: frame - 16, fps, config: {damping: 11, stiffness: 180}});
  const pulse = 1 + 0.04 * Math.sin(Math.max(0, frame - 30) / 4);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 90}}>
      <div style={{opacity: a, transform: `translateY(${(1 - a) * 40}px)`, fontFamily: 'MontX', fontWeight: 900, fontSize: 104, lineHeight: 1.0, color: WHITE, letterSpacing: -2}}>
        {end.title.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{opacity: b, transform: `translateY(${(1 - b) * 40}px)`, marginTop: 40, fontFamily: 'InterW', fontWeight: 500, fontSize: 44, lineHeight: 1.3, color: SOFT}}>
        {end.sub.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{opacity: c, transform: `scale(${(0.7 + 0.3 * c) * pulse})`, marginTop: 70, padding: '28px 64px', borderRadius: 80, background: ACC, color: BG1, fontFamily: 'MontX', fontWeight: 900, fontSize: 48, boxShadow: `0 20px 60px ${GLOW}.35)`}}>{end.cta} →</div>
      <div style={{position: 'absolute', bottom: 360, fontFamily: 'InterW', fontWeight: 700, fontSize: 30, color: ACC2, letterSpacing: 4, opacity: b}}>SYSTEMFORGE</div>
    </AbsoluteFill>
  );
};

type Theme = {bg1: string; bg2: string; acc: string; acc2: string; glow: string};
export const ReelPro: React.FC<ReelSpec & {sfx?: string; theme?: Theme}> = (spec) => {
  const frame = useCurrentFrame();
  const th = spec.theme ?? {bg1: '#16130F', bg2: '#2A211A', acc: '#F2A97E', acc2: '#FFD9BF', glow: 'rgba(242,169,126,'};
  BG1 = th.bg1; BG2 = th.bg2; ACC = th.acc; ACC2 = th.acc2; GLOW = th.glow;
  const {starts: st, endStart} = starts(spec);
  const total = endStart + s(PRO_END);
  return (
    <AbsoluteFill>
      <style>{FONTS}</style>
      <Stage />
      {spec.segments.map((g, i) => (
        <Sequence key={i} from={st[i]} durationInFrames={s(g.dur)}>
          <Clip g={g} spec={spec} first={i === 0} />
        </Sequence>
      ))}
      <Sequence from={endStart}>
        <End end={spec.end} />
      </Sequence>
      <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(frame / total) * 100}%`, background: ACC}} />
      {spec.music ? <Audio src={staticFile(spec.music)} volume={(f) => interpolate(f, [0, 4, total - 25, total], [0.55, 0.55, 0.55, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} /> : null}
      {spec.sfx ? <Audio src={staticFile(spec.sfx)} volume={0.9} /> : null}
    </AbsoluteFill>
  );
};
