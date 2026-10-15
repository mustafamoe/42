import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { DijkstraVisual } from "../DeepVisuals";
export const DijkstraScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 6289, 12588, 17628]);
  return (
    <>
      <Frame title="Compute the remaining time" tag="14 / FLY-IN EXPLAINED">
        <DijkstraVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Dijkstra-0885566b38.m4a")}
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
              text: "Before planning drones, reverse Dijkstra computes shortest travel times from every accessible zone to the goal.",
              startMs: 120,
              endMs: 6129,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The goal has distance zero. A restricted entry costs two, so this example needs three turns from start.",
              startMs: 6289,
              endMs: 12428,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Reverse search uses the original forward destination cost. Blocked zones are excluded.",
              startMs: 12588,
              endMs: 17468,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "These distances ignore reservations, making them lower bounds. They are computed once and reused for all drones.",
              startMs: 17628,
              endMs: 23874,
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
