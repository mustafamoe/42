import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { NetworkVisual } from "../Visuals";
export const NetworkScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat } = useBeat([120, 5312, 10178]);
  return (
    <>
      <Frame title="The network is a graph" tag="02 / FLY-IN EXPLAINED">
        <NetworkVisual beat={beat} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Network-b4a45b889a.m4a")}
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
              text: "Each location is a zone, also called a graph node. Each connection is a two-way edge.",
              startMs: 120,
              endMs: 5152,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Drones can move only between connected neighbors, and they can wait when a resource is busy.",
              startMs: 5312,
              endMs: 10018,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Coordinates describe locations; the destination's type determines travel time, rather than physical distance.",
              startMs: 10178,
              endMs: 16850,
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
