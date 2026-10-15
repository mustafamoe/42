import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { RecapVisual } from "../DeepVisuals";
export const RecapScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 3054, 8136]);
  return (
    <>
      <Frame title="From map to safe arrivals" tag="26 / FLY-IN EXPLAINED">
        <RecapVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Recap-568edc7f9b.m4a")}
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
              text: "Parse the map into typed objects and a custom graph.",
              startMs: 120,
              endMs: 2894,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Compute remaining distances, search timed routes, and reserve each drone's resources.",
              startMs: 3054,
              endMs: 7976,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Convert actions into movement lines until the entire fleet arrives. Routes, timing, and capacity work together.",
              startMs: 8136,
              endMs: 14894,
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
