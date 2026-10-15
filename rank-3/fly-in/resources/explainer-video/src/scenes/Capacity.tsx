import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame } from "../Visuals";
import { CapacityVisual } from "../Visuals";
export const CapacityScene: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      <Frame title="Check two separate limits" tag="09 / FLY-IN EXPLAINED">
        <CapacityVisual />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Capacity-a47a31943d.m4a")}
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
              text: "Zone capacity limits how many drones occupy a location. Link capacity limits traversals during one turn.",
              startMs: 120,
              endMs: 6700,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Both directions share the same link capacity. A larger zone cannot bypass a narrow connection.",
              startMs: 6860,
              endMs: 12162,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Start and goal have unlimited zone capacity; their capacity metadata is ignored. Their connections still have limits.",
              startMs: 12322,
              endMs: 18947,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "If either required resource is full, the drone must wait or choose another route.",
              startMs: 19107,
              endMs: 23202,
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
