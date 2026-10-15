import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ChoicesVisual } from "../DeepVisuals";
export const WaitingScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 4724, 9818, 14426]);
  return (
    <>
      <Frame title="Offer a wait or a move" tag="17 / FLY-IN EXPLAINED">
        <ChoicesVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Waiting-cd829af1f1.m4a")}
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
              text: "The wait helper advances one turn and checks whether the current zone still has space then.",
              startMs: 120,
              endMs: 4564,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The move helper rejects blocked destinations and checks the link at departure and the zone at arrival.",
              startMs: 4724,
              endMs: 9658,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The offer helper records useful states and pushes their estimated arrival into the heap.",
              startMs: 9818,
              endMs: 14266,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Priority zones use a lower secondary penalty; they do not reduce the one-turn movement cost.",
              startMs: 14426,
              endMs: 19895,
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
