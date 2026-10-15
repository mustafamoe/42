import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ReconstructionVisual } from "../DeepVisuals";
export const ReconstructScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 4074, 10303]);
  return (
    <>
      <Frame title="Turn predecessors into a route" tag="19 / FLY-IN EXPLAINED">
        <ReconstructionVisual
          beat={beat}
          beatFrame={beatFrame}
          code={
            "actions: List[RouteAction] = []\nwhile state in previous:\n    state, action = previous[state]\n    actions.append(action)\nactions.reverse()\nreturn tuple(actions)"
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Reconstruct-f85284d0e0.m4a")}
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
              text: "Every accepted state remembers the previous state and the action that reached it.",
              startMs: 120,
              endMs: 3914,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "When the search reaches goal, it follows those pointers backward, collects the actions, and reverses them.",
              startMs: 4074,
              endMs: 10143,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The resulting DroneRoute is a complete sequence of waits and movements with exact times.",
              startMs: 10303,
              endMs: 14695,
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
