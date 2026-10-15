import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { PipelineVisual } from "../Visuals";
export const PipelineScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat } = useBeat([120, 5004, 9699]);
  return (
    <>
      <Frame title="Three responsibilities" tag="04 / FLY-IN EXPLAINED">
        <PipelineVisual
          beat={beat}
          code={
            "    network = MapParser().parse(Path(arguments[1]))\n    routes = RoutePlanner(network).plan()\n    Simulation(network, routes, TerminalView()).run()"
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Pipeline-afe0057459.m4a")}
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
              text: "The entry point receives a map path. MapParser reads it and creates a NetworkMap.",
              startMs: 120,
              endMs: 4844,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "RoutePlanner builds complete routes for every drone, including waits and arrival times.",
              startMs: 5004,
              endMs: 9539,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Simulation converts those routes into movement events. TerminalView prints them, one turn at a time.",
              startMs: 9699,
              endMs: 15561,
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
