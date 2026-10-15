import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame } from "../Visuals";
import { ParallelVisual } from "../Visuals";
export const ParallelScene: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      <Frame title="Use alternate routes" tag="11 / FLY-IN EXPLAINED">
        <ParallelVisual />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Parallel-01d2e28385.m4a")}
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
              text: "Four drones on one two-edge route take five turns because the middle zone holds only one drone.",
              startMs: 120,
              endMs: 4898,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Split the fleet across two independent routes and they finish in three turns.",
              startMs: 5058,
              endMs: 8837,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A useful route depends on travel time and available capacity. The shortest individual path can become a bottleneck.",
              startMs: 8997,
              endMs: 15464,
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
