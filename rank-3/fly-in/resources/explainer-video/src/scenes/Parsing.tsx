import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BasicCaptions } from "../basic-captions";
import { Frame, useBeat } from "../Visuals";
import { ParsingVisual } from "../DeepVisuals";
export const ParsingScene: React.FC = () => {
  const { fps } = useVideoConfig();
  const { beat, beatFrame } = useBeat([120, 6667, 13126, 18632]);
  return (
    <>
      <Frame title="Validate before planning" tag="07 / FLY-IN EXPLAINED">
        <ParsingVisual
          beat={beat}
          beatFrame={beatFrame}
          code={
            'for line_number, raw_line in enumerate(lines, start=1):\n    text = raw_line.split("#", 1)[0].strip()\n    if not text:\n        continue'
          }
        />
      </Frame>
      <Audio
        name="Narration"
        src={staticFile("Parsing-20b09278a5.m4a")}
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
              text: "The parser reads the file with a context manager, removes comments, and matches each declaration's syntax.",
              startMs: 120,
              endMs: 6507,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "It validates metadata, positive regular-zone and link capacities, unique names, and known endpoints.",
              startMs: 6667,
              endMs: 12966,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "A connection from A to B duplicates B to A. Sorting the endpoint pair gives both the same identity.",
              startMs: 13126,
              endMs: 18472,
              timestampMs: null,
              confidence: null,
              pageBreakAfter: true,
            },
            {
              text: "Malformed input raises ParseError with a useful cause and line number when available. Missing files are handled too.",
              startMs: 18632,
              endMs: 24933,
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
