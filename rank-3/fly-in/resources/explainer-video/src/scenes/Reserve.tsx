import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { BookingsVisual } from "../DeepVisuals";
export const ReserveScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 5700, 10709, 16656]);
  return (
    <>
      <Frame title="Book zones and connections" tag="18 / FLY-IN EXPLAINED">
        <BookingsVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Reserve-d8c015eebf.m4a")}
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
              text: "After finding a route, the planner increments its zone and link usage counters for specific turns.",
              startMs: 120,
              endMs: 5540,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Waiting actions reserve zone occupancy too, even though they produce no movement output.",
              startMs: 5700,
              endMs: 10549,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Later drones search around these bookings. End-of-turn occupancy permits one drone to leave as another enters.",
              startMs: 10709,
              endMs: 16496,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Connection keys are direction-independent, so opposite traversals consume the same capacity allowance.",
              startMs: 16656,
              endMs: 22367,
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
