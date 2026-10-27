import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

// ---- SystemForge brand ----
const CREAM = '#F6F1E9';
const PAP = '#FFFDF9';
const SAGE = '#7A8B6F';
const SAGEL = '#E3E8DC';
const CLAY = '#EFDCCB';
const ACC = '#D9A07B';
const INK = '#2E2A25';
const MUT = '#5C554C';

const FONTS = `
@font-face{font-family:Fraunces;src:url(${staticFile('fraunces600.woff2')}) format('woff2');font-weight:600}
@font-face{font-family:InterW;src:url(${staticFile('inter500.woff2')}) format('woff2');font-weight:500}
@font-face{font-family:InterW;src:url(${staticFile('inter700.woff2')}) format('woff2');font-weight:700}
`;

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);

/** Camera = the region of the recording (in recording pixels) that fills the video card. */
export type Cam = {cx: number; cy: number; w: number};
export type Seg = {
  src: number; // start time in the recording (s)
  dur: number; // length in the reel (s)
  rate?: number; // playback speed, e.g. 1.6 to speed up a slow part
  caption: string[]; // 1 or 2 lines: big line, then smaller line
  cams: {t: number; cam: Cam}[]; // keyframes, t = seconds from the start of this segment
  ring?: {from: number; x: number; y: number; w: number; h: number}; // highlight box, recording pixels
  chip?: {from: number; text: string; tone?: 'bad' | 'good' | 'info'}; // big result pill under the card (bold style)
};
export type ReelSpec = {
  id: string;
  video: string; // file in public/, e.g. "rec-f01.mp4"
  videoW: number; // recording size, usually 1920
  videoH: number; // usually 1080
  windowTitle: string; // shown in the card's title bar
  music?: string; // file in public/, our own synthesized track
  segments: Seg[];
  end: {title: string[]; sub: string[]; cta: string};
  style?: 'classic' | 'bold'; // bold = big screen, marker words, result chip, punchy zooms
};

const LAYOUT = {
  classic: {cardW: 1000, cardH: 620, cardTop: 690, capTop: 330, cap1: 72, cap2: 60},
  bold: {cardW: 1040, cardH: 880, cardTop: 470, capTop: 170, cap1: 76, cap2: 52},
};
const lay = (spec: {style?: string}) => (spec.style === 'bold' ? LAYOUT.bold : LAYOUT.classic);
const FADE = 9;

const segStarts = (spec: ReelSpec) => {
  const out: number[] = [];
  let acc = 0;
  for (const g of spec.segments) {
    out.push(acc);
    acc += s(g.dur);
  }
  return {starts: out, endStart: acc};
};
export const END_SECONDS = 3.8;
export const totalFrames = (spec: ReelSpec) => segStarts(spec).endStart + s(END_SECONDS);

const camAt = (cams: Seg['cams'], t: number, punch = false): Cam => {
  if (cams.length === 1 || t <= cams[0].t) return cams[0].cam;
  for (let i = 1; i < cams.length; i++) {
    const a = cams[i - 1];
    const b = cams[i];
    if (t <= b.t) {
      const p = interpolate(t, [a.t, b.t], [0, 1], {easing: punch ? Easing.bezier(0.8, 0, 0.15, 1) : Easing.bezier(0.65, 0, 0.35, 1)});
      return {cx: a.cam.cx + (b.cam.cx - a.cam.cx) * p, cy: a.cam.cy + (b.cam.cy - a.cam.cy) * p, w: a.cam.w + (b.cam.w - a.cam.w) * p};
    }
  }
  return cams[cams.length - 1].cam;
};

const Caption: React.FC<{lines: string[]; style?: string; instant?: boolean}> = ({lines, style, instant}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const L = lay({style});
  const bold = style === 'bold';
  let idx = 0;
  return (
    <div style={{position: 'absolute', top: L.capTop, left: 50, right: 50, textAlign: 'center'}}>
      {lines.map((line, li) => (
        <div key={li} style={{fontFamily: li === 0 || !bold ? 'Fraunces' : 'InterW', fontWeight: li === 0 || !bold ? 600 : 500, fontSize: li === 0 ? L.cap1 : L.cap2, lineHeight: 1.12, color: li === 0 ? INK : MUT, letterSpacing: li === 0 ? -1.5 : 0, marginTop: li === 0 ? 0 : 14}}>
          {line.split(' ').map((raw, wi) => {
            const k = idx++;
            const mark = raw.startsWith('*') && raw.endsWith('*');
            const w = raw.replace(/\*/g, '');
            const p = instant ? 1 : spring({frame: frame - 2 - k * 2.5, fps, config: {damping: 14, stiffness: 180}});
            const m = spring({frame: frame - 12 - k * 2.5, fps, config: {damping: 18}});
            return (
              <span key={wi} style={{position: 'relative', display: 'inline-block', marginRight: 16, opacity: p, transform: `translateY(${(1 - p) * 26}px)`}}>
                {mark ? <span style={{position: 'absolute', left: -8, right: -8, bottom: 6, height: '42%', background: '#F3C9A6', borderRadius: 8, transformOrigin: 'left', transform: `scaleX(${m})`, zIndex: -1}} /> : null}
                <span style={{position: 'relative'}}>{w}</span>
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const Chip: React.FC<{chip: NonNullable<Seg['chip']>; top: number}> = ({chip, top}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: frame - s(chip.from), fps, config: {damping: 11, stiffness: 170}});
  if (frame < s(chip.from)) return null;
  const tone = chip.tone ?? 'info';
  const bg = tone === 'bad' ? '#F6D9CF' : tone === 'good' ? '#DCE8D4' : PAP;
  const fg = tone === 'bad' ? '#9A3B22' : tone === 'good' ? '#3D5A2E' : INK;
  return (
    <div style={{position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{padding: '22px 46px', borderRadius: 60, background: bg, color: fg, fontFamily: 'InterW', fontWeight: 700, fontSize: 50, boxShadow: '0 18px 40px rgba(46,42,37,.14)', opacity: p, transform: `scale(${0.6 + 0.4 * p})`}}>{chip.text}</div>
    </div>
  );
};

const Clip: React.FC<{g: Seg; spec: ReelSpec; first?: boolean}> = ({g, spec, first}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const L = lay(spec);
  const CARD_W = L.cardW;
  const CARD_H = L.cardH;
  const AR = CARD_H / CARD_W;
  const bold = spec.style === 'bold';
  const cam = camAt(g.cams, t, bold);
  const scale = CARD_W / cam.w;
  const h = cam.w * AR;
  const left = -(cam.cx - cam.w / 2) * scale;
  const top = -(cam.cy - h / 2) * scale;
  const fadeIn = first && bold ? 1 : interpolate(frame, [0, FADE], [0, 1], {extrapolateRight: 'clamp'});
  const pop = spring({frame: frame - 6, fps, config: {damping: 16}});

  let ring: React.ReactNode = null;
  if (g.ring && t >= g.ring.from) {
    const rp = spring({frame: frame - s(g.ring.from), fps, config: {damping: 12, stiffness: 140}});
    const r = g.ring;
    ring = (
      <div
        style={{
          position: 'absolute',
          left: left + (r.x - 8) * scale,
          top: top + (r.y - 6) * scale,
          width: (r.w + 16) * scale,
          height: (r.h + 12) * scale,
          border: `4px solid ${ACC}`,
          borderRadius: 14,
          boxShadow: `0 0 0 ${10 * rp}px rgba(217,160,123,.22)`,
          opacity: rp,
          transform: `scale(${1.25 - 0.25 * rp})`,
        }}
      />
    );
  }

  return (
    <AbsoluteFill style={{opacity: fadeIn}}>
      <Caption lines={g.caption} style={spec.style} instant={first && bold} />
      <div
        style={{
          position: 'absolute',
          left: (1080 - CARD_W) / 2,
          top: L.cardTop,
          width: CARD_W,
          height: CARD_H + 54,
          borderRadius: 30,
          background: PAP,
          boxShadow: '0 40px 80px rgba(46,42,37,.18)',
          overflow: 'hidden',
          transform: `scale(${0.94 + 0.06 * pop})`,
        }}
      >
        <div style={{height: 54, display: 'flex', alignItems: 'center', gap: 12, paddingLeft: 26, background: '#F1ECE4'}}>
          {['#E8A598', '#E9C98F', '#A9C29A'].map((c) => (
            <div key={c} style={{width: 16, height: 16, borderRadius: 8, background: c}} />
          ))}
          <div style={{marginLeft: 18, fontFamily: 'InterW', fontWeight: 500, fontSize: 22, color: MUT}}>{spec.windowTitle}</div>
        </div>
        <div style={{position: 'relative', width: CARD_W, height: CARD_H, overflow: 'hidden', background: '#fff'}}>
          <OffthreadVideo
            src={staticFile(spec.video)}
            trimBefore={s(g.src)}
            playbackRate={g.rate ?? 1}
            muted
            style={{position: 'absolute', left, top, width: spec.videoW * scale, height: spec.videoH * scale, maxWidth: 'none'}}
          />
          {ring}
        </div>
      </div>
      {g.chip ? <Chip chip={g.chip} top={L.cardTop + CARD_H + 54 + 36} /> : null}
    </AbsoluteFill>
  );
};

const EndCard: React.FC<{end: ReelSpec['end']}> = ({end}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame, fps, config: {damping: 15}});
  const b = spring({frame: frame - 10, fps, config: {damping: 15}});
  const c = spring({frame: frame - 20, fps, config: {damping: 15}});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 80}}>
      <div style={{opacity: a, transform: `translateY(${(1 - a) * 30}px)`, width: 120, height: 120, borderRadius: 60, background: SAGE, color: PAP, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Fraunces', fontStyle: 'italic', fontSize: 50}}>SF</div>
      <div style={{opacity: a, transform: `translateY(${(1 - a) * 30}px)`, marginTop: 50, fontFamily: 'Fraunces', fontWeight: 600, fontSize: 92, lineHeight: 1.05, color: INK, letterSpacing: -2}}>
        {end.title.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{opacity: b, transform: `translateY(${(1 - b) * 30}px)`, marginTop: 36, fontFamily: 'InterW', fontWeight: 500, fontSize: 40, color: MUT}}>
        {end.sub.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{opacity: c, transform: `scale(${0.8 + 0.2 * c})`, marginTop: 60, padding: '22px 48px', borderRadius: 60, background: INK, color: PAP, fontFamily: 'InterW', fontWeight: 700, fontSize: 38}}>{end.cta}</div>
    </AbsoluteFill>
  );
};

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 60) * 20;
  return (
    <AbsoluteFill style={{background: CREAM, overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: 450, background: SAGEL, left: -380 + drift, top: -360}} />
      <div style={{position: 'absolute', width: 1000, height: 1000, borderRadius: 500, background: CLAY, right: -460, bottom: -420 - drift}} />
    </AbsoluteFill>
  );
};

const Footer: React.FC = () => (
  <div style={{position: 'absolute', bottom: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16}}>
    <div style={{width: 58, height: 58, borderRadius: 29, background: SAGE, color: PAP, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Fraunces', fontStyle: 'italic', fontSize: 26}}>SF</div>
    <div style={{fontFamily: 'InterW', fontWeight: 700, fontSize: 30, color: INK}}>SystemForge</div>
  </div>
);

export const Reel: React.FC<ReelSpec> = (spec) => {
  const frame = useCurrentFrame();
  const {starts, endStart} = segStarts(spec);
  const total = endStart + s(END_SECONDS);
  return (
    <AbsoluteFill>
      <style>{FONTS}</style>
      <Background />
      {spec.segments.map((g, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={s(g.dur)}>
          <Clip g={g} spec={spec} first={i === 0} />
        </Sequence>
      ))}
      {spec.style === 'bold' ? null : (
        <Sequence from={0} durationInFrames={endStart}>
          <Footer />
        </Sequence>
      )}
      <Sequence from={endStart}>
        <EndCard end={spec.end} />
      </Sequence>
      <div style={{position: 'absolute', left: 0, bottom: 0, height: 10, width: `${(frame / total) * 100}%`, background: ACC}} />
      {spec.music ? (
        <Audio
          src={staticFile(spec.music)}
          volume={(f) => interpolate(f, [0, 15, total - 30, total], [0, 0.8, 0.8, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}
        />
      ) : null}
    </AbsoluteFill>
  );
};
