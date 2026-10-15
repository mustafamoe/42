import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { TimedTurnsVisual } from "../DeepVisuals";
export const TurnsScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 3772, 9826]);
  return (
    <>
      <Frame title="Three turns, two drones" tag="10 / FLY-IN EXPLAINED">
        <TimedTurnsVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Turns-428cf33aa8.m4a")}
        from={0.12 * fps}
        premountFor={fps}
      />
      <div
        style={{
          position: "absolute",
          left: 100,
          top: 903,
          width: 2866,
          scale: 0.6,
          transformOrigin: "top left",
        }}
      >
        <BasicCaptions
          name="English captions"
          premountFor={fps}
          width={2866}
          combineTokensWithinMilliseconds={0}
          captions={[
            {
              text: "On turn one, drone one enters A. Drone two waits at start.",
              startMs: 120,
              endMs: 3612,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "On turn two, drone one reaches goal while drone two enters A. Departure frees space during that same turn.",
              startMs: 3772,
              endMs: 9666,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "On turn three, drone two reaches goal. Simultaneous movement is represented by the schedule's turns.",
              startMs: 9826,
              endMs: 15947,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
          ]}
        />
      </div>
    </>
  );
};
