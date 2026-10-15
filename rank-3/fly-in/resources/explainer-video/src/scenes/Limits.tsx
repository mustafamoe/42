import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { LimitsVisual } from "../DeepVisuals";
export const LimitsScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 7538, 14772, 23185]);
  return (
    <>
      <Frame title="Understand the trade-off" tag="25 / FLY-IN EXPLAINED">
        <LimitsVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Limits-6fc3a328fb.m4a")}
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
              text: "Each drone gets its earliest route while earlier reservations remain fixed. This does not guarantee a globally optimal fleet schedule.",
              startMs: 120,
              endMs: 7378,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "More zones and a longer horizon create more location-and-turn states. Heap operations cost logarithmic time in queue size.",
              startMs: 7538,
              endMs: 14612,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Search bookkeeping, resource counters, and stored routes consume memory. Planning repeats for each drone, while distance estimates are reused.",
              startMs: 14772,
              endMs: 23025,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The design favors clear capacity checks and complete plans over changing earlier routes during every search.",
              startMs: 23185,
              endMs: 28926,
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
