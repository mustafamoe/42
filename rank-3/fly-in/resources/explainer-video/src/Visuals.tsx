import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const C = {
  paper: "#f6f4ec",
  ink: "#18313a",
  muted: "#6d7c7b",
  line: "#ccd4ce",
  white: "#fffefa",
  teal: "#008674",
  blue: "#3977bd",
  amber: "#ce8629",
  red: "#d45148",
  soft: "#e3efe8",
};
export const mono = "SFMono-Regular, Menlo, Consolas, monospace";
export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

export const Frame: React.FC<{
  title: string;
  tag: string;
  children: React.ReactNode;
}> = ({ title, tag, children }) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill
      data-lesson-canvas="true"
      style={{
        background: C.paper,
        color: C.ink,
        fontFamily: "Helvetica Neue, Arial, sans-serif",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 100,
          top: 70,
          fontSize: 26,
          color: C.teal,
          letterSpacing: 3,
          fontWeight: 700,
        }}
      >
        {tag}
      </div>
      <div
        style={{
          position: "absolute",
          right: 100,
          top: 70,
          fontSize: 26,
          color: C.muted,
          letterSpacing: 3,
        }}
      >
        FLY-IN
      </div>
      <div
        style={{
          position: "absolute",
          left: 100,
          top: 126,
          right: 100,
          fontSize: 82,
          lineHeight: 1.1,
          fontWeight: 700,
          letterSpacing: -2,
        }}
      >
        {title}
      </div>
      <div
        style={{
          position: "absolute",
          left: 100,
          top: 275,
          width: 1720,
          height: 585,
        }}
      >
        {children}
      </div>
      <div
        style={{
          position: "absolute",
          left: 100,
          right: 100,
          bottom: 35,
          height: 4,
          background: C.line,
        }}
      >
        <div
          style={{
            height: 4,
            background: C.teal,
            width: `${Math.min(100, (f / durationInFrames) * 100)}%`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const useBeat = (starts: number[]) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beat = Math.max(
    0,
    starts.filter((ms) => ms <= (frame / fps) * 1000).length - 1,
  );
  return { beat, beatFrame: Math.max(0, frame - (starts[beat] / 1000) * fps) };
};

export const useTurn = (count: number) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const span = (durationInFrames - 0.7 * fps) / count;
  const t = Math.max(0, frame - 0.7 * fps);
  const turn = Math.min(count, Math.floor(t / span) + 1);
  const local = t - (turn - 1) * span;
  const blend = interpolate(local, [0, 0.9 * fps], [0, 1], {
    ...clamp,
    easing: Easing.inOut(Easing.cubic),
  });
  return { turn, blend };
};

type Point = { x: number; y: number };
export const Edge: React.FC<{
  a: Point;
  b: Point;
  color?: string;
  dashed?: boolean;
  radius?: number;
}> = ({ a, b, color = C.line, dashed = false, radius = 75 }) => {
  const dx = b.x - a.x,
    dy = b.y - a.y,
    d = Math.hypot(dx, dy);
  return (
    <line
      x1={a.x + (dx / d) * radius}
      y1={a.y + (dy / d) * radius}
      x2={b.x - (dx / d) * radius}
      y2={b.y - (dy / d) * radius}
      stroke={color}
      strokeWidth={8}
      strokeLinecap="round"
      strokeDasharray={dashed ? "13 13" : undefined}
    />
  );
};
export const Node: React.FC<{
  x: number;
  y: number;
  label: string;
  sub?: string;
  color?: string;
  used?: number;
  capacity?: number;
  labelOffset?: number;
}> = ({
  x,
  y,
  label,
  sub,
  color = C.line,
  used,
  capacity = 1,
  labelOffset = 132,
}) => (
  <g>
    <circle
      cx={x}
      cy={y}
      r={76}
      fill={C.white}
      stroke={color}
      strokeWidth={5}
    />
    <text
      x={x}
      y={y + labelOffset}
      textAnchor="middle"
      fill={C.ink}
      fontSize={37}
      fontWeight={600}
    >
      {label}
    </text>
    {sub ? (
      <text x={x} y={y + 175} textAnchor="middle" fill={C.muted} fontSize={28}>
        {sub}
      </text>
    ) : null}
    {used !== undefined ? (
      <g>
        <rect
          x={x - 51}
          y={y - 141}
          width={102}
          height={49}
          rx={24}
          fill={used >= capacity ? "#fae7c9" : C.soft}
        />
        <text
          x={x}
          y={y - 107}
          textAnchor="middle"
          fill={used >= capacity ? C.amber : C.teal}
          fontSize={29}
          fontWeight={700}
        >
          {used}/{capacity}
        </text>
      </g>
    ) : null}
  </g>
);
export const Drone: React.FC<{
  x: number;
  y: number;
  id: number;
  color?: string;
  opacity?: number;
  size?: number;
}> = ({ x, y, id, color = C.teal, opacity = 1, size = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${size})`} opacity={opacity}>
    {[
      [-30, -30],
      [30, -30],
      [-30, 30],
      [30, 30],
    ].map(([dx, dy], i) => (
      <g key={i}>
        <line x1={0} y1={0} x2={dx} y2={dy} stroke={color} strokeWidth={9} />
        <circle
          cx={dx}
          cy={dy}
          r={13}
          fill={C.paper}
          stroke={color}
          strokeWidth={5}
        />
      </g>
    ))}
    <rect x={-28} y={-25} width={56} height={50} rx={16} fill={color} />
    <text y={8} fill="white" fontWeight={700} fontSize={20} textAnchor="middle">
      D{id}
    </text>
  </g>
);

export const Flow: React.FC<{
  turn: number;
  blend: number;
  drones?: number;
  branches?: number;
  width?: number;
  compact?: boolean;
  showOutput?: boolean;
}> = ({
  turn,
  blend,
  drones = 2,
  branches = 1,
  width = 1720,
  compact = false,
  showOutput = false,
}) => {
  const height = compact ? 440 : 520;
  const S = { x: compact ? 110 : 170, y: branches === 2 ? 225 : 215 };
  const G = { x: width - S.x, y: S.y };
  const mids =
    branches === 2
      ? [
          { x: width / 2, y: 115 },
          { x: width / 2, y: 335 },
        ]
      : [{ x: width / 2, y: S.y }];
  const delivered = Array.from({ length: drones }, (_, i) => i).filter(
    (i) =>
      turn - 1 - Math.floor(i / branches) >= 2 ||
      (turn - Math.floor(i / branches) >= 2 && blend === 1),
  ).length;
  const names = ["A", "B"];
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      {mids.map((p, i) => (
        <g key={i}>
          <Edge a={S} b={p} />
          <Edge a={p} b={G} />
        </g>
      ))}
      <Node {...S} label="S" sub="start · unlimited" color={C.blue} />
      <Node
        {...G}
        label="G"
        sub={
          delivered ? `${delivered}/${drones} delivered` : "goal · unlimited"
        }
        color={delivered === drones ? C.teal : C.blue}
      />
      {mids.map((p, i) => (
        <Node
          key={i}
          {...p}
          label={names[i]}
          sub={compact ? undefined : "capacity 1"}
          labelOffset={compact ? 96 : 132}
          color={C.teal}
        />
      ))}
      {Array.from({ length: drones }, (_, i) => {
        const delay = Math.floor(i / branches),
          branch = i % branches;
        const before = Math.min(2, Math.max(0, turn - 1 - delay)),
          after = Math.min(2, Math.max(0, turn - delay));
        const progress = before + (after - before) * blend;
        const points = [S, mids[branch], G];
        const k = Math.min(1, Math.floor(progress));
        const p = progress - k;
        let x = points[k].x + (points[k + 1].x - points[k].x) * p;
        let y = points[k].y + (points[k + 1].y - points[k].y) * p;
        if (progress === 0) {
          x += i % 2 === 0 ? -32 : 32;
          y += Math.floor(i / 2) * 65 - 28;
        }
        const gone = progress === 2;
        return (
          <Drone
            key={i}
            id={i + 1}
            x={x}
            y={y}
            size={compact ? 0.72 : 0.95}
            color={i % 2 === 0 ? C.teal : C.amber}
            opacity={gone ? 0 : 1}
          />
        );
      })}
      {showOutput ? (
        <text
          x={width / 2}
          y={480}
          textAnchor="middle"
          fontFamily={mono}
          fontSize={39}
          fill={C.teal}
        >
          {["D1-A", "D1-G D2-A", "D2-G"][Math.min(2, turn - 1)]}
        </text>
      ) : null}
    </svg>
  );
};

export const IntroVisual: React.FC = () => {
  const { turn, blend } = useTurn(3);
  return (
    <>
      <Flow turn={turn} blend={blend} drones={4} branches={2} />
      <div
        style={{
          position: "absolute",
          left: 600,
          bottom: 10,
          fontSize: 47,
          fontWeight: 600,
          color: C.teal,
        }}
      >
        Minimize turns. Respect capacity.
      </div>
    </>
  );
};

export const NetworkVisual: React.FC<{ beat: number }> = ({ beat }) => (
  <>
    <svg width={1720} height={450}>
      <Edge
        a={{ x: 200, y: 200 }}
        b={{ x: 850, y: 200 }}
        color={beat ? C.teal : C.line}
      />
      <Edge a={{ x: 850, y: 200 }} b={{ x: 1520, y: 200 }} />
      <Node x={200} y={200} label="S" sub="start" color={C.blue} />
      <Node x={850} y={200} label="A" sub="zone / node" color={C.teal} />
      <Node x={1520} y={200} label="G" sub="goal" color={C.blue} />
      <text x={510} y={140} textAnchor="middle" fill={C.teal} fontSize={34}>
        ↔ connection / edge
      </text>
      <text x={200} y={208} textAnchor="middle" fill={C.blue} fontSize={43}>
        S
      </text>
      <text x={850} y={208} textAnchor="middle" fill={C.teal} fontSize={43}>
        A
      </text>
      <text x={1520} y={208} textAnchor="middle" fill={C.blue} fontSize={43}>
        G
      </text>
    </svg>
    <div
      style={{
        display: "flex",
        gap: 60,
        fontFamily: mono,
        fontSize: 37,
        padding: "26px 40px",
        background: C.white,
        borderTop: `3px solid ${C.line}`,
      }}
    >
      <span style={{ color: C.teal }}>hub: A 1 0</span>
      <span style={{ color: C.blue }}>connection: S-A</span>
      <span style={{ color: C.muted }}>nb_drones: 2</span>
    </div>
  </>
);

export const CapacityVisual: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = interpolate(frame, [fps, 2.2 * fps], [0, 1], clamp);
  return (
    <>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          fontSize: 42,
          fontWeight: 600,
        }}
      >
        <span>ZONE: 1 space</span>
        <span>LINK: 1 crossing / turn</span>
      </div>
      <svg width={1720} height={480}>
        <line
          x1={860}
          y1={45}
          x2={860}
          y2={430}
          stroke={C.line}
          strokeWidth={2}
        />
        <Edge a={{ x: 180, y: 225 }} b={{ x: 620, y: 225 }} />
        <Node
          x={620}
          y={225}
          label="A"
          sub="full → wait"
          used={1}
          color={C.amber}
        />
        <Drone x={620} y={225} id={1} />
        <Drone x={180 + 230 * p} y={225} id={2} color={C.amber} />
        <text x={390} y={130} textAnchor="middle" fill={C.amber} fontSize={33}>
          WAIT
        </text>
        <Edge a={{ x: 1010, y: 225 }} b={{ x: 1550, y: 225 }} />
        <Node x={1010} y={225} label="S" />
        <Node x={1550} y={225} label="A" />
        <Drone x={1210 + 230 * p} y={225} id={1} />
        <Drone x={1060} y={225} id={2} color={C.amber} />
        <line
          x1={1140}
          y1={175}
          x2={1140}
          y2={275}
          stroke={C.amber}
          strokeWidth={8}
        />
        <text x={1290} y={130} textAnchor="middle" fill={C.amber} fontSize={33}>
          1 / 1 used this turn
        </text>
      </svg>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          textAlign: "center",
          fontSize: 45,
          color: C.teal,
          fontWeight: 600,
        }}
      >
        Both limits must allow the move.
      </div>
    </>
  );
};

export const TurnsVisual: React.FC = () => {
  const { turn, blend } = useTurn(3);
  return (
    <>
      <div style={{ fontSize: 49, fontWeight: 700, color: C.teal }}>
        TURN {turn}
        <span
          style={{
            fontSize: 30,
            fontWeight: 400,
            color: C.muted,
            marginLeft: 30,
          }}
        >
          end-of-turn positions
        </span>
      </div>
      <div style={{ marginTop: 20 }}>
        <Flow turn={turn} blend={blend} showOutput />
      </div>
    </>
  );
};

export const ParallelVisual: React.FC = () => {
  const single = useTurn(5);
  return (
    <div style={{ display: "flex", gap: 65 }}>
      <div style={{ width: 825 }}>
        <div style={{ fontSize: 43, fontWeight: 700 }}>
          ONE ROUTE{" "}
          <span style={{ float: "right", color: C.amber }}>5 turns</span>
        </div>
        <Flow
          width={825}
          compact
          turn={single.turn}
          blend={single.blend}
          drones={4}
        />
        <div style={{ fontSize: 36, color: C.amber, textAlign: "center" }}>
          A queue at the bottleneck
        </div>
      </div>
      <div style={{ width: 825 }}>
        <div style={{ fontSize: 43, fontWeight: 700 }}>
          TWO ROUTES{" "}
          <span style={{ float: "right", color: C.teal }}>3 turns</span>
        </div>
        <Flow
          width={825}
          compact
          turn={single.turn}
          blend={single.blend}
          drones={4}
          branches={2}
        />
        <div style={{ fontSize: 36, color: C.teal, textAlign: "center" }}>
          Two drones can advance each turn
        </div>
      </div>
    </div>
  );
};

export const CostsVisual: React.FC<{ beat: number; beatFrame: number }> = ({
  beat,
  beatFrame,
}) => {
  const { fps } = useVideoConfig();
  const arrival = beatFrame >= 3.8 * fps;
  const x = arrival
    ? interpolate(beatFrame, [3.8 * fps, 4.7 * fps], [860, 1420], clamp)
    : interpolate(beatFrame, [0, 0.9 * fps], [300, 860], clamp);
  if (!beat)
    return (
      <>
        <svg width={1720} height={470}>
          {[
            { x: 285, label: "NORMAL", color: C.teal, cost: "1 turn" },
            {
              x: 860,
              label: "PRIORITY",
              color: C.blue,
              cost: "1 turn · preferred",
            },
            { x: 1435, label: "BLOCKED", color: C.red, cost: "no entry" },
          ].map((v) => (
            <g key={v.label}>
              <Node
                x={v.x}
                y={200}
                label={v.label}
                sub={v.cost}
                color={v.color}
              />
              {v.label === "BLOCKED" ? (
                <g stroke={C.red} strokeWidth={9} strokeLinecap="round">
                  <line x1={v.x - 26} y1={174} x2={v.x + 26} y2={226} />
                  <line x1={v.x + 26} y1={174} x2={v.x - 26} y2={226} />
                </g>
              ) : (
                <Drone x={v.x} y={200} id={1} color={v.color} />
              )}
            </g>
          ))}
        </svg>
        <div style={{ fontSize: 44, color: C.teal, textAlign: "center" }}>
          Cost is set by the destination.
        </div>
      </>
    );
  return (
    <>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 45,
          fontWeight: 700,
        }}
      >
        <span style={{ color: C.amber }}>TURN {arrival ? 2 : 1}</span>
        <span style={{ color: C.teal, fontSize: 34 }}>
          ✓ Arrival space booked before takeoff
        </span>
      </div>
      <svg width={1720} height={440}>
        <Edge a={{ x: 300, y: 215 }} b={{ x: 1420, y: 215 }} color={C.amber} />
        <Node x={300} y={215} label="S" sub="start" color={C.blue} />
        <Node
          x={1420}
          y={215}
          label="R"
          sub="restricted · 2 turns"
          used={arrival ? 1 : 0}
          color={C.amber}
        />
        <Drone x={x} y={215} id={1} />
        <text x={860} y={365} textAnchor="middle" fill={C.amber} fontSize={37}>
          {arrival ? "arrive at destination" : "in transit on the connection"}
        </text>
      </svg>
      <div
        style={{
          fontFamily: mono,
          fontSize: 43,
          textAlign: "center",
          color: C.teal,
        }}
      >
        {arrival ? "D1-R" : "D1-S-R"}
      </div>
    </>
  );
};

export const SearchVisual: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const xs = [300, 680, 1060, 1440],
    ys = [85, 235, 385];
  const points = [
    { x: xs[0], y: ys[0] },
    { x: xs[1], y: ys[0] },
    { x: xs[2], y: ys[1] },
    { x: xs[3], y: ys[2] },
  ];
  const progress = interpolate(frame, [2 * fps, 9 * fps], [0, 3], clamp);
  return (
    <>
      <svg width={1720} height={485}>
        {xs.map((x, i) => (
          <g key={i}>
            <text x={x} y={30} textAnchor="middle" fill={C.muted} fontSize={28}>
              TURN {i}
            </text>
            <line
              x1={x}
              y1={27}
              x2={x}
              y2={440}
              stroke={C.line}
              strokeWidth={2}
              strokeDasharray="6 8"
            />
          </g>
        ))}
        {["S", "A", "G"].map((z, r) => (
          <g key={z}>
            <text
              x={90}
              y={ys[r] + 12}
              fill={C.ink}
              fontSize={40}
              fontWeight={700}
            >
              {z}
            </text>
            {xs.map((x, i) => (
              <g key={i}>
                <circle
                  cx={x}
                  cy={ys[r]}
                  r={34}
                  fill={r === 1 && i === 1 ? "#f7d9d5" : C.white}
                  stroke={r === 1 && i === 1 ? C.red : C.line}
                  strokeWidth={3}
                />
                <text
                  x={x}
                  y={ys[r] + 65}
                  fill={C.muted}
                  textAnchor="middle"
                  fontFamily={mono}
                  fontSize={23}
                >
                  ('{z}', {i})
                </text>
              </g>
            ))}
          </g>
        ))}
        <path
          d={`M ${xs[0]} ${ys[0]} L ${xs[1]} ${ys[1]} L ${xs[2]} ${ys[2]}`}
          stroke={C.blue}
          strokeWidth={4}
          fill="none"
          strokeDasharray="9 9"
          opacity={0.35}
        />
        <text
          x={xs[1]}
          y={ys[1] + 10}
          textAnchor="middle"
          fill={C.red}
          fontSize={28}
          fontWeight={700}
        >
          D1
        </text>
        <text
          x={xs[1]}
          y={ys[1] - 56}
          textAnchor="middle"
          fill={C.red}
          fontSize={28}
        >
          busy
        </text>
        <text
          x={xs[2]}
          y={ys[1] - 56}
          textAnchor="middle"
          fill={C.teal}
          fontSize={28}
        >
          free
        </text>
        {points.slice(1).map((b, i) => (
          <line
            key={i}
            x1={points[i].x}
            y1={points[i].y}
            x2={
              points[i].x +
              (b.x - points[i].x) * Math.min(1, Math.max(0, progress - i))
            }
            y2={
              points[i].y +
              (b.y - points[i].y) * Math.min(1, Math.max(0, progress - i))
            }
            stroke={C.teal}
            strokeWidth={10}
            strokeLinecap="round"
          />
        ))}
        <text
          x={490}
          y={55}
          textAnchor="middle"
          fill={C.amber}
          fontSize={26}
          fontWeight={700}
        >
          WAIT
        </text>
        {points.map((p, i) => (
          <circle
            key={i}
            {...{ cx: p.x, cy: p.y }}
            r={13}
            fill={progress >= i ? C.teal : C.line}
          />
        ))}
        <text x={xs[3] + 65} y={ys[2] + 10} fill={C.teal} fontSize={30}>
          D2 arrives
        </text>
      </svg>
      <div
        style={{
          fontSize: 40,
          textAlign: "center",
          fontFamily: mono,
          color: C.teal,
        }}
      >
        state = (zone, turn)
      </div>
    </>
  );
};

export const EstimateVisual: React.FC<{ beat: number; code: string }> = ({
  beat,
  code,
}) => (
  <>
    <div
      style={{
        fontSize: 42,
        display: "flex",
        alignItems: "center",
        gap: 35,
        marginBottom: 30,
      }}
    >
      <span style={{ color: C.blue }}>current turn</span>
      <span>+</span>
      <span style={{ color: C.teal }}>remaining travel</span>
      <span>=</span>
      <span style={{ fontWeight: 700 }}>estimated arrival</span>
    </div>
    <div style={{ display: "flex", gap: 70 }}>
      <div
        style={{
          width: 1000,
          background: C.white,
          padding: "40px 50px",
          borderLeft: `6px solid ${C.teal}`,
        }}
      >
        <div style={{ fontFamily: mono, fontSize: 42, color: C.muted }}>
          state ('A', 2)
        </div>
        <div
          style={{
            display: "flex",
            gap: 35,
            fontSize: 110,
            fontWeight: 650,
            alignItems: "center",
            margin: "26px 0",
          }}
        >
          <span style={{ color: C.blue }}>2</span>
          <span style={{ fontSize: 64, color: C.muted }}>+</span>
          <span style={{ color: C.teal }}>1</span>
          <span style={{ fontSize: 64, color: C.muted }}>=</span>
          <span style={{ color: C.teal }}>3</span>
        </div>
        <div style={{ fontSize: 32, color: C.muted }}>
          Shortest remaining time ignores congestion.
        </div>
      </div>
      <div style={{ width: 650 }}>
        <div
          style={{
            fontSize: 30,
            letterSpacing: 2,
            color: C.muted,
            marginBottom: 15,
          }}
        >
          EXAMPLE: LOWEST ESTIMATE FIRST
        </div>
        {[
          ["A", 2, 3],
          ["S", 2, 4],
          ["S", 3, 5],
        ].map(([zone, turn, total], i) => (
          <div
            key={i}
            style={{
              padding: "24px 25px",
              fontFamily: mono,
              fontSize: 36,
              background: i === 0 ? C.soft : C.white,
              color: i === 0 ? C.teal : C.muted,
              marginBottom: 12,
              border: i === 0 ? `3px solid ${C.teal}` : `3px solid ${C.line}`,
            }}
          >
            ('{zone}', {turn}){" "}
            <span style={{ float: "right", fontWeight: 700 }}>
              {total}
              {i === 0 ? " ← next" : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
    <div
      style={{
        fontFamily: mono,
        fontSize: 30,
        marginTop: 32,
        color: beat ? C.teal : C.muted,
      }}
    >
      {code}
    </div>
  </>
);

export const ReserveVisual: React.FC<{ beat: number; beatFrame: number }> = ({
  beat,
  beatFrame,
}) => {
  const { fps } = useVideoConfig();
  const cells = [
    [1, 2, 0],
    [1, 2, 0],
    [0, 1, 2],
  ];
  return (
    <>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "450px repeat(3,1fr)",
          gap: 7,
          fontSize: 35,
        }}
      >
        {["RESOURCE / TURN", "1", "2", "3"].map((v) => (
          <div
            key={v}
            style={{
              padding: "18px 20px",
              color: C.muted,
              textAlign: v === "RESOURCE / TURN" ? "left" : "center",
            }}
          >
            {v}
          </div>
        ))}
        {["ZONE A", "LINK S–A", "LINK A–G"].map((label, r) => (
          <React.Fragment key={label}>
            <div
              style={{
                padding: "30px 25px",
                background: C.white,
                fontFamily: mono,
              }}
            >
              {label}
            </div>
            {cells[r].map((id, c) => {
              const visible =
                id === 1
                  ? beat > 0 || beatFrame > r * 0.6 * fps
                  : id === 2 && beat > 0;
              return (
                <div
                  key={c}
                  style={{
                    padding: "28px 25px",
                    background: visible
                      ? id === 1
                        ? "#d8eee7"
                        : "#fae7ca"
                      : C.white,
                    color: visible ? (id === 1 ? C.teal : C.amber) : C.muted,
                    fontSize: 38,
                    fontWeight: visible ? 700 : 400,
                    textAlign: "center",
                  }}
                >
                  {visible ? `D${id} · 1/1` : "0/1"}
                </div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
      <div
        style={{
          display: "flex",
          gap: 65,
          alignItems: "center",
          marginTop: 34,
          fontSize: 34,
        }}
      >
        <span style={{ color: C.teal, fontWeight: 600 }}>D1 books first</span>
        <span style={{ color: C.amber, fontWeight: 600 }}>
          D2 uses other turns
        </span>
        <span style={{ color: C.muted }}>Earlier routes stay fixed.</span>
      </div>
    </>
  );
};

export const PipelineVisual: React.FC<{ beat: number; code: string }> = ({
  beat,
  code,
}) => {
  const lines = code.split("\n");
  return (
    <>
      <div style={{ display: "flex", gap: 25, alignItems: "center" }}>
        {["PARSE", "PLAN", "PRINT"].map((name, i) => (
          <React.Fragment key={name}>
            {i ? <span style={{ color: C.muted, fontSize: 55 }}>→</span> : null}
            <div
              style={{
                flex: 1,
                borderBottom: `6px solid ${beat === i ? C.teal : C.line}`,
                padding: "16px 22px",
                fontSize: 40,
                fontWeight: 700,
                color: beat === i ? C.teal : C.muted,
              }}
            >
              {name}
              <div style={{ fontSize: 27, fontWeight: 400, marginTop: 12 }}>
                {
                  [
                    "map → graph",
                    "graph → schedule",
                    "schedule → movement lines",
                  ][i]
                }
              </div>
            </div>
          </React.Fragment>
        ))}
      </div>
      <div
        style={{
          height: 290,
          marginTop: 30,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {beat === 0 ? (
          <div style={{ display: "flex", gap: 90, alignItems: "center" }}>
            <div>
              <div
                style={{
                  fontSize: 24,
                  color: C.muted,
                  letterSpacing: 2,
                  marginBottom: 20,
                }}
              >
                MAP EXCERPT
              </div>
              <pre
                style={{
                  fontFamily: mono,
                  fontSize: 33,
                  lineHeight: 1.5,
                  margin: 0,
                  color: C.blue,
                }}
              >
                {"nb_drones: 2\nhub: A 1 0\nconnection: S-A"}
              </pre>
            </div>
            <span style={{ fontSize: 70, color: C.muted }}>→</span>
            <svg width={650} height={260}>
              <Edge a={{ x: 90, y: 85 }} b={{ x: 325, y: 85 }} />
              <Edge a={{ x: 325, y: 85 }} b={{ x: 560, y: 85 }} />
              <Node x={90} y={85} label="S" />
              <Node x={325} y={85} label="A" />
              <Node x={560} y={85} label="G" />
            </svg>
          </div>
        ) : beat === 1 ? (
          <div style={{ display: "flex", alignItems: "center", gap: 80 }}>
            <DroneBadge />
            <span style={{ fontSize: 72, color: C.muted }}>→</span>
            <div
              style={{
                fontFamily: mono,
                fontSize: 37,
                lineHeight: 1.7,
                color: C.teal,
              }}
            >
              D1: S → A → G<br />
              D2: wait → A → G
            </div>
          </div>
        ) : (
          <div style={{ display: "flex", gap: 100 }}>
            <pre
              style={{
                fontFamily: mono,
                fontSize: 43,
                lineHeight: 1.5,
                color: C.teal,
                margin: 0,
              }}
            >
              {"D1-A\nD1-G D2-A\nD2-G"}
            </pre>
            <div style={{ fontSize: 34, color: C.muted, lineHeight: 1.8 }}>
              One line per turn
              <br />
              Waiting drones omitted
              <br />
              End after final arrival
            </div>
          </div>
        )}
      </div>
      <div
        style={{
          fontFamily: mono,
          fontSize: 31,
          padding: "27px 30px",
          background: C.white,
          borderTop: `2px solid ${C.line}`,
          color: C.teal,
        }}
      >
        {lines[Math.min(beat, 2)]}
      </div>
    </>
  );
};
const DroneBadge = () => (
  <svg width={150} height={150}>
    <Drone x={75} y={75} id={1} size={1.4} />
  </svg>
);
