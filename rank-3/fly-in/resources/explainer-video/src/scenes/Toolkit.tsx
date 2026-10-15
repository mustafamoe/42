import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ToolkitVisual } from "../DeepVisuals";
export const ToolkitScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 6567, 12671, 17969]);
  return (
    <>
      <Frame title="Python tools, by role" tag="05 / FLY-IN EXPLAINED">
        <ToolkitVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Toolkit-e7c7901c62.m4a")}
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
              text: "The runtime uses Python 3.10 or later and the standard library. Graph logic is implemented directly.",
              startMs: 120,
              endMs: 6407,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Dataclasses define data objects; Enum defines zone types; typing describes interfaces.",
              startMs: 6567,
              endMs: 12511,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Regular expressions and pathlib handle parsing and files. heapq supplies the priority queue.",
              startMs: 12671,
              endMs: 17809,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "defaultdict supplies zero-based counters, itertools.count breaks ties, and sys and os handle terminal behavior.",
              startMs: 17969,
              endMs: 24728,
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
