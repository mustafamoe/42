import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { InputVisual } from "../DeepVisuals";
export const InputScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 6134, 13265, 20249]);
  return (
    <>
      <Frame title="Read the map format" tag="03 / FLY-IN EXPLAINED">
        <InputVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Input-578e15453d.m4a")}
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
              text: "The first data declaration gives a positive drone count. Exactly one start and one end are required.",
              startMs: 120,
              endMs: 5974,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Every zone has a unique name and integer coordinates. Declare all zones before connections, whose endpoints must exist.",
              startMs: 6134,
              endMs: 13105,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Bracket metadata sets zone type, color, zone capacity, or link capacity. Comments begin with a hash.",
              startMs: 13265,
              endMs: 20089,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Defaults are normal zones, no color, and capacities of one. Metadata order does not matter.",
              startMs: 20249,
              endMs: 26079,
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
