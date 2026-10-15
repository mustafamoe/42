import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ColorsVisual } from "../DeepVisuals";
export const ColorsScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 5179, 10951, 16576]);
  return (
    <>
      <Frame
        title="Use colors without changing tokens"
        tag="22 / FLY-IN EXPLAINED"
      >
        <ColorsVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Colors-fdf760a5ea.m4a")}
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
              text: "A movement token contains the drone identifier and target, such as D1-A.",
              startMs: 120,
              endMs: 5019,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "On an interactive terminal, destination color metadata selects an ANSI color for that token.",
              startMs: 5179,
              endMs: 10791,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Piped or redirected output stays plain, and the NO_COLOR environment variable disables color.",
              startMs: 10951,
              endMs: 16416,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Expected parsing and planning errors go to standard error, with exit status one; successful runs return zero.",
              startMs: 16576,
              endMs: 23326,
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
