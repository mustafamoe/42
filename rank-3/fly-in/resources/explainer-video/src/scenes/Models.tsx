import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ModelsVisual } from "../DeepVisuals";
export const ModelsScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 7519, 14111, 18497]);
  return (
    <>
      <Frame title="Objects describe the problem" tag="06 / FLY-IN EXPLAINED">
        <ModelsVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Models-00e6181c9e.m4a")}
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
              text: "Zone stores a name, coordinates, type, color, and capacity. Connection stores endpoints and link capacity.",
              startMs: 120,
              endMs: 7359,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "NetworkMap holds the graph and drone count. RouteAction describes one movement or wait, with start and end times.",
              startMs: 7519,
              endMs: 13951,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "DroneRoute groups a drone's actions and final arrival. A wait has no connection.",
              startMs: 14111,
              endMs: 18337,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Dataclasses generate constructors, frozen records prevent accidental changes, and type hints make these relationships explicit.",
              startMs: 18497,
              endMs: 26249,
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
