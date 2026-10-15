import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { LaunchVisual } from "../DeepVisuals";
export const LaunchScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 4821, 11529, 18381]);
  return (
    <>
      <Frame title="Run and inspect the program" tag="23 / FLY-IN EXPLAINED">
        <LaunchVisual beat={beat} beatFrame={beatFrame} />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Launch-05a417766d.m4a")}
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
              text: "Run from the submission directory and pass a real map path with the Makefile's MAP setting.",
              startMs: 120,
              endMs: 4661,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The direct Python command also accepts a map path. Without a MAP setting, make run looks for map.txt.",
              startMs: 4821,
              endMs: 11369,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Make install installs the development checks. Make debug opens the Python debugger; make clean removes caches.",
              startMs: 11529,
              endMs: 18221,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "The submission contains the Python modules, Makefile, README, and .gitignore. Maps and private tests are kept separately.",
              startMs: 18381,
              endMs: 25886,
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
