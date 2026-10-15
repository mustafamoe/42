import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { HeapVisual } from "../DeepVisuals";
export const HeapScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 4910, 11413, 17600]);
  return (
    <>
      <Frame title="A* chooses what to explore" tag="16 / FLY-IN EXPLAINED">
        <HeapVisual
          beat={beat}
          beatFrame={beatFrame}
          code={
            "estimate = turn + self._heuristic[zone_name]\nheapq.heappush(\n    search.queue,\n    (estimate, turn, preference, next(search.tie_breaker), zone_name),\n)"
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Heap-2318d4d9f9.m4a")}
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
              text: "A star estimates arrival by adding the current turn to the shortest remaining travel time.",
              startMs: 120,
              endMs: 4750,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A min-heap explores the smallest estimate first. Time and priority penalties resolve secondary choices.",
              startMs: 4910,
              endMs: 11253,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The search stores its heap, best preference per state, predecessor records, and an insertion counter.",
              startMs: 11413,
              endMs: 17440,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A better route updates the state record. Old heap entries with outdated preferences are skipped.",
              startMs: 17600,
              endMs: 22648,
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
