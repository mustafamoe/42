import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame } from "../Visuals";
import { IntroVisual } from "../Visuals";
export const IntroScene: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      <Frame title="Deliver the whole fleet" tag="01 / FLY-IN EXPLAINED">
        <IntroVisual />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Intro-1b0c8f8b48.m4a")}
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
              text: "Fly-in simulates drones moving from one start zone to one goal through a connected network.",
              startMs: 120,
              endMs: 4805,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The objective is to finish the entire fleet in as few turns as possible.",
              startMs: 4965,
              endMs: 8632,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A valid schedule must respect movement costs, zone space, and connection capacity.",
              startMs: 8792,
              endMs: 14115,
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
