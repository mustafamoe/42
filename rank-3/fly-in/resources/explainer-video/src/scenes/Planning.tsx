import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { PlanningVisual } from "../DeepVisuals";
export const PlanningScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 5789, 10872, 16499]);
  return (
    <>
      <Frame title="Plan the fleet in order" tag="20 / FLY-IN EXPLAINED">
        <PlanningVisual
          beat={beat}
          beatFrame={beatFrame}
          code={
            "for drone_id in range(1, self._network.drone_count + 1):\n    route = self._find_route(drone_id)\n    self._reserve(route)\n    routes.append(route)"
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Planning-8a38471507.m4a")}
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
              text: "Drones are planned in identifier order. Each completed route is reserved before the next drone is searched.",
              startMs: 120,
              endMs: 5629,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The search horizon is the latest existing arrival plus the unconstrained shortest travel time.",
              startMs: 5789,
              endMs: 10712,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Waiting at the unlimited start until earlier drones finish guarantees a clear fallback route within that bound.",
              startMs: 10872,
              endMs: 16339,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A disconnected or blocked-off goal raises PlanningError. Complete routes avoid runtime deadlock decisions.",
              startMs: 16499,
              endMs: 22226,
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
