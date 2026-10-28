import React from 'react';
import {Composition} from 'remotion';
import {Reel, ReelSpec, totalFrames} from './Reel';
import {ReelPro, proFrames} from './ReelPro';
import {ReelNative, nativeFrames} from './ReelNative';
import example from '../specs/f01-next-step.json';

// Spec comes from --props=specs/<id>.json at render time; the example is only the default.
export const Root: React.FC = () => (
  <>
  <Composition
    id="ReelPro"
    component={ReelPro}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={proFrames(example as ReelSpec)}
    defaultProps={example as ReelSpec}
    calculateMetadata={({props}) => ({durationInFrames: proFrames(props as ReelSpec)})}
  />
  <Composition
    id="ReelNative"
    component={ReelNative}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={nativeFrames(example as ReelSpec)}
    defaultProps={example as ReelSpec}
    calculateMetadata={({props}) => ({durationInFrames: nativeFrames(props as ReelSpec)})}
  />
  <Composition
    id="Reel"
    component={Reel}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={totalFrames(example as ReelSpec)}
    defaultProps={example as ReelSpec}
    calculateMetadata={({props}) => ({durationInFrames: totalFrames(props as ReelSpec)})}
  />
  </>
);
