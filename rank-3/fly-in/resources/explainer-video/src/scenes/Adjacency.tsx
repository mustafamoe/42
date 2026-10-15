import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { AdjacencyVisual } from "../DeepVisuals";
export const AdjacencyScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 3619, 9746]);
  return (
    <>
      <Frame title="Build the adjacency list" tag="08 / FLY-IN EXPLAINED">
        <AdjacencyVisual
          beat={beat}
          beatFrame={beatFrame}
          code={
            "self.adjacency = {name: [] for name in self.zones}\nfor connection in self.connections:\n    self.adjacency[connection.first].append(connection)\n    self.adjacency[connection.second].append(connection)"
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Adjacency-758f735c8a.m4a")}
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
              text: "NetworkMap maps every zone name to a list of its connections.",
              startMs: 120,
              endMs: 3459,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A bidirectional connection is added to both endpoints' lists. Connection.other() returns the opposite endpoint.",
              startMs: 3619,
              endMs: 9586,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "This makes finding neighbors direct, without scanning every edge. No graph library is needed.",
              startMs: 9746,
              endMs: 15090,
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
