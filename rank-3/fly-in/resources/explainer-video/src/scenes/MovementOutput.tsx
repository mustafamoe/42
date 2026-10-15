import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { OutputVisual } from "../DeepVisuals";
export const MovementOutputScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 6836, 12284, 19124]);
  return (
    <>
      <Frame title="Convert actions into output" tag="21 / FLY-IN EXPLAINED">
        <OutputVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("MovementOutput-baf9c6a60a.m4a")}
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
              text: "Simulation groups Movement records by turn. A record contains a drone identifier, target, and color.",
              startMs: 120,
              endMs: 6676,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Wait actions are skipped. Restricted movement adds a connection event before its destination event.",
              startMs: 6836,
              endMs: 12124,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "TerminalView sorts movements by drone identifier and prints space-separated tokens. Each line represents one turn.",
              startMs: 12284,
              endMs: 18964,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Delivered drones have no later actions. Output stops at the final drone's arrival.",
              startMs: 19124,
              endMs: 23704,
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
