import React from "react";
import { interpolate, useVideoConfig } from "remotion";
import {
  C,
  mono,
  clamp,
  Node,
  Edge,
  Drone,
  Flow,
  CostsVisual,
  EstimateVisual,
  ReserveVisual,
  PipelineVisual,
} from "./Visuals";

type BeatProps = { beat: number; beatFrame: number; code?: string };
const labelStyle: React.CSSProperties = {
  fontSize: 29,
  color: C.muted,
  letterSpacing: 2,
};
const chipStyle: React.CSSProperties = {
  background: C.white,
  padding: "20px 26px",
  borderLeft: `5px solid ${C.teal}`,
  fontFamily: mono,
  fontSize: 31,
  lineHeight: 1.4,
};
export const Code: React.FC<{
  text: string;
  label?: string;
  focus?: number[];
  fontSize?: number;
}> = ({ text, label, focus = [], fontSize = 30 }) => (
  <div
    style={{
      background: C.white,
      border: `1px solid ${C.line}`,
      borderRadius: 8,
      overflow: "hidden",
    }}
  >
    {label ? (
      <div
        style={{
          padding: "17px 25px",
          fontSize: 24,
          color: C.muted,
          fontFamily: mono,
          borderBottom: `1px solid ${C.line}`,
        }}
      >
        {label}
      </div>
    ) : null}
    <div
      style={{
        padding: "22px 25px",
        fontFamily: mono,
        fontSize,
        lineHeight: 1.5,
      }}
    >
      {text.split("\n").map((t, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            background: focus.includes(i) ? C.soft : "transparent",
          }}
        >
          <span
            style={{
              color: C.muted,
              fontSize: fontSize - 5,
              width: 45,
              flexShrink: 0,
              paddingTop: 4,
            }}
          >
            {i + 1}
          </span>
          <span
            style={{
              whiteSpace: "pre-wrap",
              overflowWrap: "anywhere",
              color: C.ink,
            }}
          >
            {t || " "}
          </span>
        </div>
      ))}
    </div>
  </div>
);
const Note: React.FC<{ children: React.ReactNode; color?: string }> = ({
  children,
  color = C.teal,
}) => (
  <div
    style={{
      fontSize: 36,
      lineHeight: 1.35,
      color,
      marginTop: 25,
      borderLeft: `5px solid ${color}`,
      paddingLeft: 22,
    }}
  >
    {children}
  </div>
);
const Row: React.FC<{ name: string; value: string; active?: boolean }> = ({
  name,
  value,
  active = false,
}) => (
  <div
    style={{
      display: "flex",
      gap: 25,
      padding: "18px 22px",
      borderBottom: `1px solid ${C.line}`,
      background: active ? C.soft : C.white,
      fontSize: 32,
    }}
  >
    <span
      style={{ width: 245, color: active ? C.teal : C.ink, fontFamily: mono }}
    >
      {name}
    </span>
    <span style={{ color: C.muted }}>{value}</span>
  </div>
);

export const InputVisual: React.FC<BeatProps> = ({ beat }) => {
  const map =
    "nb_drones: 2\nstart_hub: S 0 0 [color=blue]\nhub: A 1 0 [zone=normal max_drones=1]\nend_hub: G 2 0 [color=green]\nconnection: S-A [max_link_capacity=1]\nconnection: A-G";
  return (
    <>
      <div style={{ display: "flex", gap: 60, alignItems: "center" }}>
        <div style={{ width: 1070 }}>
          <Code
            text={map}
            label="A complete, valid example map"
            focus={
              beat === 0
                ? [0, 1, 3]
                : beat === 1
                  ? [1, 2, 3, 4, 5]
                  : beat === 2
                    ? [2, 4]
                    : [2, 5]
            }
          />
        </div>
        <svg width={590} height={420}>
          <Edge a={{ x: 90, y: 200 }} b={{ x: 295, y: 200 }} />
          <Edge a={{ x: 295, y: 200 }} b={{ x: 500, y: 200 }} />
          <Node x={90} y={200} label="S" color={C.blue} />
          <Node x={295} y={200} label="A" color={C.teal} />
          <Node x={500} y={200} label="G" color={C.blue} />
        </svg>
      </div>
      <Note>
        {
          [
            "Positive drone count · exactly one start and goal",
            "Declare zones first · names contain no spaces or dashes",
            "Optional metadata in [brackets] · # comments ignored",
            "Defaults: normal · no color · zone 1 · link 1",
          ][Math.min(beat, 3)]
        }
      </Note>
    </>
  );
};

export const ToolkitVisual: React.FC<BeatProps> = ({ beat }) => {
  const groups = [
    [
      "dataclasses · Enum · typing",
      "Objects, supported types, typed interfaces",
    ],
    ["re · pathlib", "Match declarations and read map files"],
    [
      "heapq · defaultdict · count",
      "Prioritize states, count bookings, break ties",
    ],
    ["sys · os", "Arguments, exit status, streams, terminal settings"],
  ];
  return (
    <>
      <div
        style={{
          display: "flex",
          gap: 40,
          alignItems: "baseline",
          marginBottom: 35,
        }}
      >
        <span style={{ fontSize: 70, fontWeight: 700, color: C.teal }}>
          Python 3.10+
        </span>
        <span style={{ fontSize: 35, color: C.muted }}>
          standard-library runtime
        </span>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        {groups.map(([title, detail], i) => (
          <div
            key={title}
            style={{
              padding: "30px 30px",
              borderTop: `5px solid ${(beat === 1 ? [0] : beat === 2 ? [1, 2] : beat === 3 ? [2, 3] : []).includes(i) ? C.teal : C.line}`,
              background: C.white,
            }}
          >
            <div
              style={{
                fontFamily: mono,
                fontSize: 34,
                color: (beat === 1
                  ? [0]
                  : beat === 2
                    ? [1, 2]
                    : beat === 3
                      ? [2, 3]
                      : []
                ).includes(i)
                  ? C.teal
                  : C.ink,
              }}
            >
              {title}
            </div>
            <div
              style={{
                fontSize: 28,
                color: C.muted,
                marginTop: 19,
                lineHeight: 1.35,
              }}
            >
              {detail}
            </div>
          </div>
        ))}
      </div>
      <Note>Graph representation and routing are written directly.</Note>
    </>
  );
};

export const ModelsVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 0)
    return (
      <>
        <div style={{ display: "flex", gap: 70 }}>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>ZONE / LOCATION</div>
            <div style={{ marginTop: 20 }}>
              {[
                ["name", "A"],
                ["x, y", "1, 0"],
                ["kind", "ZoneType.NORMAL"],
                ["color", "none"],
                ["max_drones", "1"],
              ].map(([a, b]) => (
                <Row key={a} name={a} value={b} />
              ))}
            </div>
          </div>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>CONNECTION / TWO-WAY LINK</div>
            <div style={{ marginTop: 20 }}>
              {[
                ["first", "S"],
                ["second", "A"],
                ["capacity", "1"],
                ["key", "('A', 'S')"],
                ["label", "S-A"],
              ].map(([a, b]) => (
                <Row key={a} name={a} value={b} />
              ))}
            </div>
          </div>
        </div>
        <Note>Data describes locations, links, and their constraints.</Note>
      </>
    );
  if (beat === 1)
    return (
      <>
        <div style={{ display: "flex", gap: 70 }}>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>NETWORKMAP</div>
            {[
              ["drone_count", "2"],
              ["zones", "name → Zone"],
              ["connections", "tuple of Connection"],
              ["start, end", "S, G"],
              ["adjacency", "zone → neighboring links"],
            ].map(([a, b]) => (
              <Row key={a} name={a} value={b} />
            ))}
          </div>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>ROUTEACTION</div>
            {[
              ["start_time", "1"],
              ["end_time", "2"],
              ["origin", "S"],
              ["destination", "A"],
              ["connection", "S–A"],
            ].map(([a, b]) => (
              <Row key={a} name={a} value={b} />
            ))}
          </div>
        </div>
      </>
    );
  if (beat === 2)
    return (
      <>
        <div style={{ fontSize: 48, fontWeight: 700, marginBottom: 28 }}>
          DroneRoute = identifier + actions + arrival
        </div>
        <Code
          text={
            "DroneRoute(\n    drone_id=2,\n    actions=(wait_at_S, move_to_A, move_to_G),\n    arrival_time=3,\n)"
          }
          label="A complete plan for drone 2"
        />
        <Note>Wait: origin = destination, connection = None.</Note>
      </>
    );
  return (
    <>
      <Code
        text={
          "@dataclass(frozen=True)\nclass Zone:\n    name: str\n    x: int\n    y: int\n    kind: ZoneType = ZoneType.NORMAL"
        }
        label="models.py / typed domain records"
      />
      <div
        style={{
          display: "flex",
          gap: 60,
          fontSize: 34,
          marginTop: 28,
          color: C.teal,
        }}
      >
        <span>Generated constructor</span>
        <span>Immutable record</span>
        <span>Explicit field types</span>
      </div>
    </>
  );
};

export const ParsingVisual: React.FC<BeatProps> = ({ beat, code = "" }) => {
  if (beat === 2)
    return (
      <>
        <svg width={1720} height={330}>
          <Edge a={{ x: 350, y: 150 }} b={{ x: 1370, y: 150 }} color={C.teal} />
          <Node x={350} y={150} label="A" />
          <Node x={1370} y={150} label="B" />
          <text x={860} y={120} textAnchor="middle" fontSize={50} fill={C.teal}>
            A–B = B–A
          </text>
        </svg>
        <div style={chipStyle}>direction-independent key = ('A', 'B')</div>
        <Note>One physical connection, one shared identity.</Note>
      </>
    );
  return (
    <>
      <Code
        text={code}
        label="parser.py / strip comments and preserve line numbers"
        focus={[1]}
      />
      <div
        style={{
          display: "flex",
          gap: 25,
          alignItems: "center",
          marginTop: 35,
          fontSize: 33,
        }}
      >
        {["syntax", "metadata", "constraints", "objects"].map((x, i) => (
          <React.Fragment key={x}>
            {i ? <span>→</span> : null}
            <div
              style={{
                padding: "20px 30px",
                background: beat > 0 && i === 2 ? "#f7d9d5" : C.soft,
                color: beat > 0 && i === 2 ? C.red : C.teal,
              }}
            >
              {x}
              {beat > 0 && i === 2 ? " ×" : ""}
            </div>
          </React.Fragment>
        ))}
      </div>
      {beat > 0 ? (
        <>
          <div style={{ ...chipStyle, marginTop: 28, color: C.red }}>
            max_drones=0 → rejected
          </div>
          <Note color={C.red}>
            ParseError: line 3 · max_drones must be a positive integer
          </Note>
        </>
      ) : (
        <Note>Read safely → remove # comments → parse → validate.</Note>
      )}
    </>
  );
};

export const AdjacencyVisual: React.FC<BeatProps> = ({ beat, code = "" }) => (
  <>
    <Code
      text={code}
      label="models.py / NetworkMap.__post_init__"
      focus={beat === 0 ? [0] : beat === 1 ? [2, 3] : []}
    />
    <div style={{ display: "flex", gap: 55, marginTop: 35 }}>
      <div style={{ flex: 1, ...chipStyle, color: C.teal }}>S → [S–A]</div>
      <div style={{ flex: 1, ...chipStyle, color: C.blue }}>A → [S–A, A–G]</div>
      <div style={{ flex: 1, ...chipStyle, color: C.teal }}>G → [A–G]</div>
    </div>
    <Note>Connection.other('S') returns 'A' for link S–A.</Note>
  </>
);

export const TypesVisual: React.FC<BeatProps> = ({ beat, code = "" }) => (
  <>
    <svg width={1720} height={300}>
      {[
        { x: 175, name: "NORMAL", cost: "1 turn", color: C.teal },
        { x: 630, name: "PRIORITY", cost: "1 turn · preferred", color: C.blue },
        { x: 1085, name: "BLOCKED", cost: "no entry", color: C.red },
        { x: 1540, name: "RESTRICTED", cost: "2 turns", color: C.amber },
      ].map((v) => (
        <g key={v.name}>
          <Node x={v.x} y={110} label={v.name} sub={v.cost} color={v.color} />
          <text
            x={v.x}
            y={125}
            textAnchor="middle"
            fontSize={55}
            fontWeight={700}
            fill={v.color}
          >
            {v.name === "BLOCKED" ? "×" : v.name === "RESTRICTED" ? "2" : "1"}
          </text>
        </g>
      ))}
    </svg>
    <Code
      text={code}
      label="models.py / Zone.travel_time · blocked moves are rejected by the planner"
      fontSize={29}
    />
    {beat === 2 ? (
      <div style={{ fontSize: 29, color: C.teal, marginTop: 8 }}>
        R → G costs 1 turn when G is normal.
      </div>
    ) : null}
  </>
);

export const TimedTurnsVisual: React.FC<BeatProps> = ({ beat, beatFrame }) => {
  const { fps } = useVideoConfig();
  const turn = Math.min(3, beat + 1);
  const blend = interpolate(beatFrame, [0, 0.85 * fps], [0, 1], clamp);
  return (
    <>
      <div style={{ fontSize: 48, fontWeight: 700, color: C.teal }}>
        TURN {turn}
        <span
          style={{
            fontSize: 29,
            color: C.muted,
            fontWeight: 400,
            marginLeft: 30,
          }}
        >
          end-of-turn positions
        </span>
      </div>
      <Flow turn={turn} blend={blend} showOutput />
    </>
  );
};
export const TransitVisual: React.FC<BeatProps> = ({ beat, beatFrame }) => {
  const { fps } = useVideoConfig();
  const phase =
    beat === 0
      ? Math.min(beatFrame, 3 * fps)
      : beat === 1
        ? 3.8 * fps + beatFrame
        : 5 * fps;
  return <CostsVisual beat={1} beatFrame={phase} />;
};

export const DijkstraVisual: React.FC<BeatProps> = ({ beat }) => {
  const values = beat === 0 ? ["?", "?", "0"] : ["3", "1", "0"];
  return (
    <>
      <svg width={1720} height={480}>
        <Edge a={{ x: 230, y: 225 }} b={{ x: 860, y: 225 }} color={C.teal} />
        <Edge a={{ x: 860, y: 225 }} b={{ x: 1490, y: 225 }} color={C.teal} />
        <Node x={230} y={225} label="S" sub="start" color={C.blue} />
        <Node x={860} y={225} label="R" sub="restricted" color={C.amber} />
        <Node x={1490} y={225} label="G" sub="goal" color={C.teal} />
        {[230, 860, 1490].map((x, i) => (
          <g key={i}>
            <rect
              x={x - 96}
              y={47}
              width={192}
              height={67}
              rx={12}
              fill={C.soft}
            />
            <text
              x={x}
              y={93}
              textAnchor="middle"
              fill={C.teal}
              fontFamily={mono}
              fontSize={40}
            >
              h = {values[i]}
            </text>
          </g>
        ))}
        <text x={545} y={190} textAnchor="middle" fontSize={31} fill={C.amber}>
          enter R: 2
        </text>
        <text x={1175} y={190} textAnchor="middle" fontSize={31} fill={C.teal}>
          enter G: 1
        </text>
        <text x={1175} y={275} textAnchor="middle" fontSize={46} fill={C.teal}>
          ←
        </text>
        <text x={545} y={275} textAnchor="middle" fontSize={46} fill={C.teal}>
          ←
        </text>
      </svg>
      <div style={chipStyle}>
        {beat < 2
          ? "h(S) = 2 + 1 = 3 turns"
          : "Precompute once · ignore bookings · reuse for every drone"}
      </div>
    </>
  );
};

export const HeapVisual: React.FC<BeatProps> = ({ beat, code = "" }) => {
  if (beat < 2)
    return <EstimateVisual beat={beat} code={code.split("\n")[0]} />;
  return (
    <>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 24,
          marginBottom: 28,
        }}
      >
        {[
          ["queue", "heap of candidate states"],
          ["best_preference", "state → lowest penalty"],
          ["previous", "state → predecessor + action"],
          ["tie_breaker", "unique insertion counter"],
        ].map(([a, b]) => (
          <div
            key={a}
            style={{
              background: C.white,
              padding: "18px 24px",
              borderTop: `4px solid ${C.teal}`,
            }}
          >
            <div style={{ fontFamily: mono, fontSize: 34, color: C.teal }}>
              {a}
            </div>
            <div style={{ fontSize: 29, color: C.muted, marginTop: 12 }}>
              {b}
            </div>
          </div>
        ))}
      </div>
      {beat === 2 ? (
        <Code
          text={code}
          label="planner.py / _RouteSearch is fresh for each drone"
          fontSize={26}
        />
      ) : (
        <>
          <div
            style={{ display: "flex", gap: 50, fontFamily: mono, fontSize: 40 }}
          >
            <div style={{ ...chipStyle, color: C.red }}>
              old ('A', 2): penalty 2 ✕
            </div>
            <div style={{ ...chipStyle, color: C.teal }}>
              best ('A', 2): penalty 1 ✓
            </div>
          </div>
          <Note>Skip outdated entries. Keep the improved state.</Note>
        </>
      )}
    </>
  );
};

export const ChoicesVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 3)
    return (
      <>
        <div style={{ fontSize: 46, fontWeight: 700, marginBottom: 30 }}>
          Same arrival time → prefer priority destinations
        </div>
        <div style={{ display: "flex", gap: 65 }}>
          {[
            ["NORMAL", "travel = 1", "penalty = 1", C.muted],
            ["PRIORITY", "travel = 1", "penalty = 0", C.teal],
          ].map(([a, b, c, color]) => (
            <div
              key={a}
              style={{
                width: 825,
                padding: "50px 45px",
                background: C.white,
                borderTop: `6px solid ${color}`,
              }}
            >
              <div style={{ fontSize: 43, color }}>{a}</div>
              <div style={{ fontSize: 52, fontFamily: mono, margin: "35px 0" }}>
                {b}
              </div>
              <div style={{ fontSize: 37, color }}>{c}</div>
            </div>
          ))}
        </div>
        <Note>Preference is separate from movement cost.</Note>
      </>
    );
  return (
    <>
      <div style={{ display: "flex", gap: 65 }}>
        {[
          ["WAIT", "('A', 1)", "('A', 2)", "zone A has space at T2"],
          ["MOVE", "('A', 1)", "('G', 2)", "link A–G at T2 + arrival capacity"],
        ].map(([name, from, to, rule], i) => (
          <div
            key={name}
            style={{
              width: 825,
              background: C.white,
              padding: "35px 28px",
              borderTop: `5px solid ${beat === i ? C.teal : C.line}`,
            }}
          >
            <div
              style={{
                fontSize: 43,
                fontWeight: 700,
                color: beat === i ? C.teal : C.muted,
              }}
            >
              {name}
            </div>
            <div style={{ fontFamily: mono, fontSize: 37, margin: "45px 0" }}>
              {from} → {to}
            </div>
            <div style={{ fontSize: 32, color: C.teal }}>✓ {rule}</div>
          </div>
        ))}
      </div>
      <div style={{ ...chipStyle, marginTop: 36 }}>
        offer(next_state) → record predecessor → heap
      </div>
      <Note>Reject blocked zones and transitions beyond the horizon.</Note>
    </>
  );
};

export const BookingsVisual: React.FC<BeatProps> = ({ beat, beatFrame }) => {
  if (beat === 1)
    return (
      <>
        <div style={{ fontSize: 48, fontWeight: 700, marginBottom: 25 }}>
          A waiting drone still occupies its zone.
        </div>
        <svg width={1720} height={300}>
          <Node x={370} y={140} label="A at T1" used={1} color={C.teal} />
          <Node x={1350} y={140} label="A at T2" used={1} color={C.teal} />
          <Drone x={370} y={140} id={1} />
          <Drone x={1350} y={140} id={1} />
          <Edge
            a={{ x: 370, y: 140 }}
            b={{ x: 1350, y: 140 }}
            color={C.amber}
          />
          <text
            x={860}
            y={105}
            textAnchor="middle"
            fill={C.amber}
            fontSize={42}
          >
            WAIT 1 TURN
          </text>
        </svg>
        <div style={{ ...chipStyle, marginTop: 30 }}>
          connection = None · destination = A · reserve (A, 2)
        </div>
      </>
    );
  return <ReserveVisual beat={beat === 0 ? 0 : 1} beatFrame={beatFrame} />;
};

export const ReconstructionVisual: React.FC<BeatProps> = ({
  beat,
  code = "",
}) => (
  <>
    <svg width={1720} height={200}>
      {["('S', 0)", "('S', 1)", "('A', 2)", "('G', 3)"].map((v, i) => (
        <g key={v}>
          <circle
            cx={200 + i * 440}
            cy={90}
            r={45}
            fill={C.white}
            stroke={beat < 2 ? C.blue : C.teal}
            strokeWidth={4}
          />
          <text
            x={200 + i * 440}
            y={186}
            textAnchor="middle"
            fontFamily={mono}
            fontSize={33}
            fill={C.ink}
          >
            {v}
          </text>
          {i < 3 ? (
            <text
              x={420 + i * 440}
              y={105}
              textAnchor="middle"
              fontSize={55}
              fill={beat < 2 ? C.blue : C.teal}
            >
              {beat < 2 ? "←" : "→"}
            </text>
          ) : null}
        </g>
      ))}
    </svg>
    <div style={{ fontSize: 32, color: C.muted, marginBottom: 20 }}>
      {beat < 2
        ? "Follow previous-state pointers backward"
        : "Reverse the collected actions: WAIT → MOVE → MOVE"}
    </div>
    <Code text={code} label="planner.py / reconstruct" fontSize={26} />
  </>
);

export const PlanningVisual: React.FC<BeatProps> = ({ beat, code = "" }) => {
  if (beat === 0)
    return (
      <>
        <Code
          text={code}
          label="planner.py / one completed route before the next"
          focus={[1, 2]}
        />
        <div
          style={{
            display: "flex",
            gap: 55,
            alignItems: "center",
            marginTop: 45,
            fontSize: 42,
          }}
        >
          <span style={{ color: C.teal }}>D1: search → reserve</span>
          <span>→</span>
          <span style={{ color: C.amber }}>D2: search → reserve</span>
        </div>
      </>
    );
  if (beat === 3)
    return (
      <>
        <svg width={1720} height={370}>
          <Node x={310} y={170} label="S" color={C.blue} />
          <Node x={1410} y={170} label="G" color={C.red} />
          <Edge
            a={{ x: 310, y: 170 }}
            b={{ x: 1410, y: 170 }}
            dashed
            color={C.line}
          />
          <text x={860} y={188} fill={C.red} fontSize={74} textAnchor="middle">
            ×
          </text>
        </svg>
        <div style={{ ...chipStyle, color: C.red }}>
          PlanningError: no accessible route from start to end
        </div>
      </>
    );
  return (
    <>
      <div
        style={{
          fontFamily: mono,
          fontSize: 45,
          color: C.teal,
          marginBottom: 45,
        }}
      >
        horizon = latest arrival + shortest travel = 2 + 2 = 4
      </div>
      <svg width={1720} height={310}>
        {["S @ T0", "S @ T1", "S @ T2", "A @ T3", "G @ T4"].map((v, i) => (
          <g key={v}>
            <circle
              cx={160 + i * 350}
              cy={105}
              r={48}
              fill={C.white}
              stroke={i < 3 ? C.amber : C.teal}
              strokeWidth={4}
            />
            <text
              x={160 + i * 350}
              y={203}
              textAnchor="middle"
              fontFamily={mono}
              fontSize={29}
              fill={C.ink}
            >
              {v}
            </text>
            {i < 4 ? (
              <text
                x={335 + i * 350}
                y={120}
                textAnchor="middle"
                fill={i < 2 ? C.amber : C.teal}
                fontSize={44}
              >
                →
              </text>
            ) : null}
          </g>
        ))}
      </svg>
      <Note>
        Safe fallback: wait at S until prior drones finish, then travel.
      </Note>
    </>
  );
};

export const OutputVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 0)
    return (
      <>
        <div style={{ fontSize: 45, fontWeight: 700, marginBottom: 35 }}>
          RouteAction → Movement → turn bucket
        </div>
        <Code
          text={
            "Movement(\n    drone_id=1,\n    target='A',\n    color='red',\n)"
          }
          label="simulation.py / one output event"
        />
        <Note>Group each event by its exact output turn.</Note>
      </>
    );
  if (beat === 1)
    return (
      <>
        <div style={{ display: "flex", gap: 65 }}>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>WAIT</div>
            <div style={{ ...chipStyle, marginTop: 30 }}>connection = None</div>
            <Note color={C.muted}>No movement token</Note>
          </div>
          <div style={{ width: 825 }}>
            <div style={labelStyle}>RESTRICTED MOVE</div>
            <div style={{ ...chipStyle, marginTop: 30 }}>
              T1: D1-S-R
              <br />
              T2: D1-R
            </div>
            <Note>Connection event, then destination event</Note>
          </div>
        </div>
      </>
    );
  return (
    <>
      <div style={{ display: "flex", gap: 85, alignItems: "center" }}>
        <div style={{ width: 890 }}>
          <Code
            text={"D1-A\nD1-G D2-A\nD2-G"}
            label="STDOUT / one line per turn"
            fontSize={47}
          />
        </div>
        <div style={{ fontSize: 36, lineHeight: 1.8, color: C.muted }}>
          Sorted by drone ID
          <br />
          Space-separated tokens
          <br />
          Waits omitted
          <br />
          Delivered drones stop appearing
          <br />
          End at the last arrival
        </div>
      </div>
    </>
  );
};

export const ColorsVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 3)
    return (
      <>
        <div style={{ display: "flex", gap: 70 }}>
          <div style={{ width: 825, background: C.soft, padding: "60px 45px" }}>
            <div style={{ fontSize: 74, color: C.teal, fontWeight: 700 }}>
              0 ✓
            </div>
            <div style={{ fontSize: 35, marginTop: 25 }}>Success</div>
            <div style={{ fontFamily: mono, fontSize: 29, marginTop: 25 }}>
              stdout: movement lines
            </div>
          </div>
          <div
            style={{ width: 825, background: "#f7d9d5", padding: "60px 45px" }}
          >
            <div style={{ fontSize: 74, color: C.red, fontWeight: 700 }}>
              1 ×
            </div>
            <div style={{ fontSize: 35, marginTop: 25 }}>
              Expected input / planning failure
            </div>
            <div style={{ fontFamily: mono, fontSize: 29, marginTop: 25 }}>
              stderr: clear error message
            </div>
          </div>
        </div>
      </>
    );
  return (
    <>
      <div style={{ display: "flex", gap: 65 }}>
        {[true, false].map((color) => (
          <div
            key={String(color)}
            style={{
              width: 825,
              background: color ? "#152331" : C.white,
              padding: "32px 35px",
              border: `1px solid ${C.line}`,
            }}
          >
            <div
              style={{
                fontSize: 26,
                letterSpacing: 2,
                color: color ? "#a5b5c2" : C.muted,
                marginBottom: 35,
              }}
            >
              {color
                ? "TERMINAL EXAMPLE / A=red, G=blue"
                : "PIPE / REDIRECT / NO_COLOR"}
            </div>
            <div
              style={{
                fontFamily: mono,
                fontSize: 40,
                lineHeight: 1.8,
                color: color ? "#eeefe8" : C.ink,
              }}
            >
              <span style={{ color: color ? "#f38776" : undefined }}>D1-A</span>
              <br />
              <span style={{ color: color ? "#79a9ee" : undefined }}>
                D1-G
              </span>{" "}
              <span style={{ color: color ? "#f38776" : undefined }}>D2-A</span>
              <br />
              <span style={{ color: color ? "#79a9ee" : undefined }}>D2-G</span>
            </div>
          </div>
        ))}
      </div>
      <div style={{ ...chipStyle, marginTop: 35 }}>
        stream.isatty() and "NO_COLOR" not in os.environ
      </div>
      <Note>Color belongs to the destination. Token text stays identical.</Note>
    </>
  );
};

export const LaunchVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat < 2)
    return (
      <>
        <div style={labelStyle}>FROM rank-3/fly-in/submission/</div>
        <div style={{ marginTop: 30 }}>
          <Code
            text={
              "make run MAP=../resources/maps/easy/01_linear_path.txt\n\npython3.10 fly_in.py ../resources/maps/easy/01_linear_path.txt"
            }
            label="Pass a real map file"
            focus={beat === 0 ? [0] : [2]}
            fontSize={32}
          />
        </div>
        <Note>Default MAP=map.txt applies only when no path is supplied.</Note>
      </>
    );
  if (beat === 2)
    return (
      <>
        {[
          ["make install", "Install flake8 and mypy"],
          ["make run MAP=…", "Run a map"],
          ["make debug MAP=…", "Step through with pdb"],
          ["make clean", "Remove Python caches"],
          ["make lint", "Check style and types"],
        ].map(([a, b]) => (
          <Row key={a} name={a} value={b} />
        ))}
      </>
    );
  return (
    <>
      <div style={{ fontSize: 39, fontWeight: 700, marginBottom: 25 }}>
        Submitted Python modules
      </div>
      {[
        ["fly_in.py", "coordinate the application"],
        ["models.py", "domain objects and graph"],
        ["parser.py", "read and validate maps"],
        ["planner.py", "search and reserve routes"],
        ["simulation.py", "movement events and terminal view"],
      ].map(([a, b]) => (
        <Row key={a} name={a} value={b} />
      ))}
      <Note>Also: Makefile · README.md · .gitignore</Note>
    </>
  );
};

export const ChecksVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 0)
    return (
      <>
        <div style={{ display: "flex", gap: 70 }}>
          {[
            ["flake8", "Style and readability"],
            ["mypy", "Function and data types"],
          ].map(([a, b]) => (
            <div
              key={a}
              style={{
                width: 825,
                padding: "50px 40px",
                background: C.white,
                borderTop: `6px solid ${C.teal}`,
              }}
            >
              <div style={{ fontFamily: mono, fontSize: 68, color: C.teal }}>
                {a}
              </div>
              <div style={{ fontSize: 37, marginTop: 24 }}>{b}</div>
            </div>
          ))}
        </div>
        <Note>Docstrings document the purpose of classes and methods.</Note>
      </>
    );
  if (beat === 2)
    return (
      <>
        <div style={{ fontSize: 45, fontWeight: 700, marginBottom: 25 }}>
          Reconstruct usage independently
        </div>
        {[
          ["zone_usage[(zone, turn)]", "must be ≤ max_drones"],
          ["link_usage[(key, turn)]", "must be ≤ link capacity"],
          ["end_time - start_time", "must match destination cost"],
          ["final zone", "must equal goal"],
        ].map(([a, b]) => (
          <div
            key={a}
            style={{
              display: "flex",
              gap: 45,
              padding: "25px 25px",
              background: C.white,
              borderBottom: `1px solid ${C.line}`,
              fontSize: 31,
            }}
          >
            <span style={{ fontFamily: mono, width: 890 }}>{a}</span>
            <span style={{ color: C.teal }}>✓ {b}</span>
          </div>
        ))}
      </>
    );
  return (
    <>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 25 }}>
        {[
          "Malformed maps",
          "Blocked / disconnected routes",
          "Zone + link capacities",
          "Priority ties",
          "Restricted arrival timing",
          "Same-turn departure + entry",
          "Single and large fleets",
          "Supplied performance maps",
        ].map((v) => (
          <div
            key={v}
            style={{
              padding: "25px 30px",
              background: C.white,
              fontSize: 32,
              borderLeft: `5px solid ${C.teal}`,
            }}
          >
            ✓ {v}
          </div>
        ))}
      </div>
    </>
  );
};

export const LimitsVisual: React.FC<BeatProps> = ({ beat }) => {
  if (beat === 0 || beat === 3)
    return (
      <>
        <div style={{ display: "flex", gap: 65 }}>
          <div
            style={{
              width: 825,
              background: C.white,
              padding: "45px 40px",
              borderTop: `6px solid ${C.teal}`,
            }}
          >
            <div style={{ fontSize: 44, color: C.teal, fontWeight: 700 }}>
              Prioritized planning
            </div>
            <div style={{ fontSize: 35, lineHeight: 1.8, marginTop: 25 }}>
              Search D1 → reserve
              <br />
              Search D2 → reserve
              <br />
              Search D3 → reserve
            </div>
          </div>
          <div
            style={{
              width: 825,
              background: C.white,
              padding: "45px 40px",
              borderTop: `6px solid ${C.amber}`,
            }}
          >
            <div style={{ fontSize: 44, color: C.amber, fontWeight: 700 }}>
              Trade-off
            </div>
            <div style={{ fontSize: 35, lineHeight: 1.8, marginTop: 25 }}>
              Earlier routes stay fixed.
              <br />
              Each next route is earliest available.
              <br />
              Global optimum is not guaranteed.
            </div>
          </div>
        </div>
        <Note>Complete plans simplify capacity safety.</Note>
      </>
    );
  return (
    <>
      <div style={{ display: "flex", gap: 90, alignItems: "center" }}>
        <svg width={790} height={380}>
          {Array.from({ length: 4 }, (_, r) =>
            Array.from({ length: 4 }, (_, c) => (
              <g key={`${r}-${c}`}>
                <circle
                  cx={130 + c * 170}
                  cy={65 + r * 85}
                  r={24}
                  fill={C.soft}
                  stroke={C.teal}
                  strokeWidth={3}
                />
                {r === 0 ? (
                  <text
                    x={130 + c * 170}
                    y={23}
                    textAnchor="middle"
                    fontSize={24}
                    fill={C.muted}
                  >
                    T{c}
                  </text>
                ) : null}
                {c === 0 ? (
                  <text
                    x={65}
                    y={75 + r * 85}
                    textAnchor="middle"
                    fontSize={24}
                    fill={C.muted}
                  >
                    {["S", "A", "B", "G"][r]}
                  </text>
                ) : null}
              </g>
            )),
          )}
        </svg>
        <div style={{ width: 800, fontSize: 36, lineHeight: 1.6 }}>
          <div style={{ fontFamily: mono, color: C.teal, fontSize: 40 }}>
            states ≤ V × (T + 1)
          </div>
          <div style={{ marginTop: 24 }}>
            More zones + more turns → more states
          </div>
          <div>D drones → repeated route searches</div>
          <div>Heap operations → log(queue size)</div>
        </div>
      </div>
      <div style={chipStyle}>
        {beat === 1
          ? "A distinct state combines one zone with one turn."
          : "Memory: graph + search records + counters + complete routes"}
      </div>
      <Note>Shortest-distance estimates are shared across the fleet.</Note>
    </>
  );
};

export const RecapVisual: React.FC<BeatProps> = ({ beat }) => {
  const code =
    "network = MapParser().parse(Path(arguments[1]))\nroutes = RoutePlanner(network).plan()\nSimulation(network, routes, TerminalView()).run()";
  return <PipelineVisual beat={Math.min(2, beat)} code={code} />;
};
