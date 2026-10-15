import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame } from "../Visuals";
import { SearchVisual } from "../Visuals";
export const SearchScene: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      <Frame title="Search location AND time" tag="15 / FLY-IN EXPLAINED">
        <SearchVisual />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Search-072b244d86.m4a")}
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
              text: "Knowing the zone alone is insufficient: A can be busy on turn one and free on turn two.",
              startMs: 120,
              endMs: 4856,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A search state contains the zone name and the turn. Waiting reaches a later state in the same zone.",
              startMs: 5016,
              endMs: 10190,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Moving reaches a neighboring zone at its arrival turn. Capacity checks decide which transitions are allowed.",
              startMs: 10350,
              endMs: 16288,
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
