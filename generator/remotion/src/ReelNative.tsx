// SystemForge "native" reel: TikTok-native look. The recording fills the whole 9:16 frame and the camera
// follows the action (card drags), big white captions with a black outline like phone-made videos,
// sticker-style result tag, hard cuts with a white flash, light end card.
import React from 'react';
import {AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {ReelSpec, Seg, Cam} from './Reel';

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
const W = 1080;
const H = 1920;
export const NATIVE_END = 3.4;

const FONTS = `
@font-face{font-family:MontX;src:url(${staticFile('montserrat800.woff2')}) format('woff2');font-weight:800}
@font-face{font-family:MontX;src:url(${staticFile('montserrat900.woff2')}) format('woff2');font-weight:900}
@font-face{font-family:InterW;src:url(${staticFile('inter700.woff2')}) format('woff2');font-weight:700}
`;

const starts = (spec: ReelSpec) => {
  const out: number[] = [];
  let acc = 0;
  for (const g of spec.segments) {
    out.push(acc);
    acc += s(g.dur);
  }
  return {starts: out, endStart: acc};
};
export const nativeFrames = (spec: ReelSpec) => starts(spec).endStart + s(NATIVE_END);

const camAt = (cams: Seg['cams'], t: number): Cam => {
  if (cams.length === 1 || t <= cams[0].t) return cams[0].cam;
  for (let i = 1; i < cams.length; i++) {
    const a = cams[i - 1];
    const b = cams[i];
    if (t <= b.t) {
      const p = interpolate(t, [a.t, b.t], [0, 1], {easing: Easing.bezier(0.45, 0, 0.25, 1)});
      return {cx: a.cam.cx + (b.cam.cx - a.cam.cx) * p, cy: a.cam.cy + (b.cam.cy - a.cam.cy) * p, w: a.cam.w + (b.cam.w - a.cam.w) * p};
    }
  }
  return cams[cams.length - 1].cam;
};

const outline = (r: number) => {
  const out: string[] = [];
  for (let a = 0; a < 16; a++) out.push(`${(Math.cos((a / 16) * Math.PI * 2) * r).toFixed(1)}px ${(Math.sin((a / 16) * Math.PI * 2) * r).toFixed(1)}px 0 #000`);
  return out.join(',') + `, 0 ${r + 4}px 0 rgba(0,0,0,.5)`;
};

// white text, thick black outline, yellow keyword: the look of captions typed in the TikTok editor
const Caption: React.FC<{lines: string[]; instant: boolean}> = ({lines, instant}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  let k = 0;
  return (
    <div style={{position: 'absolute', top: 250, left: 50, right: 50, textAlign: 'center'}}>
      {lines.map((line, li) => (
        <div key={li} style={{fontFamily: 'MontX', fontWeight: li === 0 ? 900 : 800, fontSize: li === 0 ? 80 : 56, lineHeight: 1.12, marginTop: li === 0 ? 0 : 18}}>
          {line.split(' ').map((raw, wi) => {
            const i = k++;
            const mark = raw.startsWith('*') && raw.endsWith('*');
            const w = raw.replace(/\*/g, '');
            const p = instant && li === 0 ? 1 : spring({frame: frame - i * 3, fps, config: {damping: 9, stiffness: 260}});
            return (
              <span
                key={wi}
                style={{
                  display: 'inline-block',
                  marginRight: li === 0 ? 22 : 16,
                  color: mark ? '#FFE14D' : '#FFFFFF',
                  textShadow: outline(li === 0 ? 6 : 4),
                  opacity: Math.min(1, p * 1.5),
                  transform: `scale(${0.4 + 0.6 * p})`,
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const Sticker: React.FC<{chip: NonNullable<Seg['chip']>}> = ({chip}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < s(chip.from)) return null;
  const p = spring({frame: frame - s(chip.from), fps, config: {damping: 8, stiffness: 220}});
  const wob = Math.sin((frame - s(chip.from)) / 6) * 1.2;
  return (
    <div style={{position: 'absolute', top: 1180, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{padding: '22px 40px', borderRadius: 22, background: '#FFFFFF', color: '#111', fontFamily: 'MontX', fontWeight: 900, fontSize: 50, border: '6px solid #111', boxShadow: '10px 10px 0 #111', transform: `scale(${p}) rotate(${-5 + wob}deg)`}}>{chip.text}</div>
    </div>
  );
};

const Clip: React.FC<{g: Seg; spec: ReelSpec; first: boolean}> = ({g, spec, first}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cam = camAt(g.cams, t);
  const scale = W / cam.w;
  const h = cam.w * (H / W);
  const left = -(cam.cx - cam.w / 2) * scale;
  const top = -(cam.cy - h / 2) * scale;
  // hard cut with a short punch-in + white flash (no fades)
  const punch = first ? 1 : interpolate(frame, [0, 6], [1.12, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const flash = first ? 0 : interpolate(frame, [0, 4], [0.85, 0], {extrapolateRight: 'clamp'});
  let ring: React.ReactNode = null;
  if (g.ring && t >= g.ring.from) {
    const r = g.ring;
    const rp = spring({frame: frame - s(r.from), fps, config: {damping: 10, stiffness: 170}});
    ring = <div style={{position: 'absolute', left: left + (r.x - 8) * scale, top: top + (r.y - 8) * scale, width: (r.w + 16) * scale, height: (r.h + 16) * scale, border: '9px solid #FFE14D', borderRadius: 26, boxShadow: '0 0 0 6px #111', opacity: rp, transform: `scale(${1.25 - 0.25 * rp})`}} />;
  }
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      <AbsoluteFill style={{transform: `scale(${punch})`}}>
        <OffthreadVideo src={staticFile(spec.video)} trimBefore={s(g.src)} playbackRate={g.rate ?? 1} muted style={{position: 'absolute', left, top, width: spec.videoW * scale, height: spec.videoH * scale, maxWidth: 'none'}} />
        {ring}
      </AbsoluteFill>
      {/* soft top shade so the captions read on any screen */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 760, background: 'linear-gradient(rgba(0,0,0,.42), rgba(0,0,0,0))'}} />
      <Caption lines={g.caption} instant={first} />
      {g.chip ? <Sticker chip={g.chip} /> : null}
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
};

const End: React.FC<{end: ReelSpec['end']}> = ({end}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame, fps, config: {damping: 9, stiffness: 200}});
  const b = spring({frame: frame - 7, fps, config: {damping: 12}});
  const c = spring({frame: frame - 14, fps, config: {damping: 8, stiffness: 220}});
  return (
    <AbsoluteFill style={{background: '#FFE14D', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 80}}>
      <div style={{fontFamily: 'MontX', fontWeight: 900, fontSize: 112, lineHeight: 1.0, color: '#111', letterSpacing: -2, transform: `scale(${a}) rotate(${(1 - a) * -8}deg)`}}>
        {end.title.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{opacity: b, marginTop: 36, fontFamily: 'MontX', fontWeight: 800, fontSize: 46, lineHeight: 1.25, color: '#111'}}>
        {end.sub.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div style={{marginTop: 64, padding: '26px 58px', borderRadius: 22, background: '#fff', border: '6px solid #111', boxShadow: '10px 10px 0 #111', fontFamily: 'MontX', fontWeight: 900, fontSize: 52, color: '#111', transform: `scale(${c}) rotate(-3deg)`}}>{end.cta} 👆</div>
    </AbsoluteFill>
  );
};

export const ReelNative: React.FC<ReelSpec & {sfx?: string}> = (spec) => {
  const frame = useCurrentFrame();
  const {starts: st, endStart} = starts(spec);
  const total = endStart + s(NATIVE_END);
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      <style>{FONTS}</style>
      {spec.segments.map((g, i) => (
        <Sequence key={i} from={st[i]} durationInFrames={s(g.dur)}>
          <Clip g={g} spec={spec} first={i === 0} />
        </Sequence>
      ))}
      <Sequence from={endStart}>
        <End end={spec.end} />
      </Sequence>
      <div style={{position: 'absolute', left: 0, top: 0, height: 10, width: `${(frame / total) * 100}%`, background: '#FFE14D'}} />
      {spec.music ? <Audio src={staticFile(spec.music)} volume={(f) => interpolate(f, [0, total - 25, total], [0.55, 0.55, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} /> : null}
      {spec.sfx ? <Audio src={staticFile(spec.sfx)} volume={0.9} /> : null}
    </AbsoluteFill>
  );
};
