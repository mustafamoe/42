import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { TransitVisual } from "../DeepVisuals";
export const TransitScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 5711, 11742]);
  return (
    <>
      <Frame title="Reserve the restricted arrival" tag="13 / FLY-IN EXPLAINED">
        <TransitVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Transit-d78fcdde8a.m4a")}
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
              text: "A restricted movement starts with one turn on the connection. The next turn must reach the destination.",
              startMs: 120,
              endMs: 5551,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Before starting, the planner checks the link's first-turn capacity and the destination's second-turn capacity.",
              startMs: 5711,
              endMs: 11582,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "This guarantees arrival without waiting in transit. Output names the connection first, then the restricted zone.",
              startMs: 11742,
              endMs: 18105,
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
