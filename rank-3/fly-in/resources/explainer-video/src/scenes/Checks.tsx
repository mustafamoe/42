import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ChecksVisual } from "../DeepVisuals";
export const ChecksScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 5527, 14272, 19633]);
  return (
    <>
      <Frame
        title="Check behavior, style, and types"
        tag="24 / FLY-IN EXPLAINED"
      >
        <ChecksVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Checks-ad61412143.m4a")}
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
              text: "flake8 checks style. mypy checks type hints. Docstrings explain classes and methods.",
              startMs: 120,
              endMs: 5367,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Private tests cover malformed input, blocked routes, capacities, priority choices, restricted transit, and same-turn departures.",
              startMs: 5527,
              endMs: 14112,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "They reconstruct resource usage from planned actions and verify that every drone reaches goal safely.",
              startMs: 14272,
              endMs: 19473,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Supplied maps and larger fleets also test performance. A valid schedule matters before optimizing its turn count.",
              startMs: 19633,
              endMs: 26422,
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
