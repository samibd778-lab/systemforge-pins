import React from 'react';
import {Composition} from 'remotion';
import {Reel, ReelSpec, totalFrames} from './Reel';
import example from '../specs/f01-next-step.json';

// Spec comes from --props=specs/<id>.json at render time; the example is only the default.
export const Root: React.FC = () => (
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
);
