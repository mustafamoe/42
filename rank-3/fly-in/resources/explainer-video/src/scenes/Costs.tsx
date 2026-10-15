import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { TypesVisual } from "../DeepVisuals";
export const CostsScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 7144, 11317]);
  return (
    <>
      <Frame title="Destination type sets the cost" tag="12 / FLY-IN EXPLAINED">
        <TypesVisual
          beat={beat}
          beatFrame={beatFrame}
          code={"if self.kind is ZoneType.RESTRICTED:\n    return 2\nreturn 1"}
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Costs-712d252525.m4a")}
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
              text: "Normal zones take one turn to enter. Priority zones also take one turn, but influence equal-time route choices.",
              startMs: 120,
              endMs: 6984,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Blocked zones cannot be entered. Restricted zones take two turns to enter.",
              startMs: 7144,
              endMs: 11157,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Leaving a restricted zone for a normal destination takes one turn. The destination always determines the cost.",
              startMs: 11317,
              endMs: 17494,
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
