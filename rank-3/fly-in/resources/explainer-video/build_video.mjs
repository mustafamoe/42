import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
  unlinkSync,
} from "node:fs";

const scenes = JSON.parse(readFileSync("src/scenes.json", "utf8"));
mkdirSync("src/scenes", { recursive: true });
const visual = {
  Intro: { component: "IntroVisual", props: "", deep: false },
  Network: { component: "NetworkVisual", props: "beat={beat}", deep: false },
  Input: {
    component: "InputVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Pipeline: { component: "PipelineVisual", props: "beat={beat}", deep: false },
  Toolkit: {
    component: "ToolkitVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Models: {
    component: "ModelsVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Parsing: {
    component: "ParsingVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Adjacency: {
    component: "AdjacencyVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Capacity: { component: "CapacityVisual", props: "", deep: false },
  Turns: {
    component: "TimedTurnsVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Parallel: { component: "ParallelVisual", props: "", deep: false },
  Costs: {
    component: "TypesVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Transit: {
    component: "TransitVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Dijkstra: {
    component: "DijkstraVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Search: { component: "SearchVisual", props: "", deep: false },
  Heap: {
    component: "HeapVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Waiting: {
    component: "ChoicesVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Reserve: {
    component: "BookingsVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Reconstruct: {
    component: "ReconstructionVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Planning: {
    component: "PlanningVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  MovementOutput: {
    component: "OutputVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Colors: {
    component: "ColorsVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Launch: {
    component: "LaunchVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Checks: {
    component: "ChecksVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Limits: {
    component: "LimitsVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
  Recap: {
    component: "RecapVisual",
    props: "beat={beat} beatFrame={beatFrame}",
    deep: true,
  },
};
for (const scene of scenes) {
  const { component, props, deep } = visual[scene.id];
  const hasBeat = props.includes("beat=");
  const hasBeatFrame = props.includes("beatFrame=");
  const code = scene.code ? ` code={${JSON.stringify(scene.code)}}` : "";
  const source = `import React from 'react';
import {staticFile,useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import {Frame${hasBeat ? ",useBeat" : ""}} from '../Visuals';
import {${component}} from '../${deep ? "DeepVisuals" : "Visuals"}';
export const ${scene.id}Scene:React.FC=()=>{
 const {fps}=useVideoConfig();
 ${hasBeat ? `const {beat${hasBeatFrame ? ",beatFrame" : ""}}=useBeat(${JSON.stringify(scene.captions.map((c) => c.startMs))});` : ""}
 return <>
  <Frame title=${JSON.stringify(scene.title)} tag=${JSON.stringify(scene.tag)}><${component} ${props}${code}/></Frame>
  <Audio name="Narration" src={staticFile(${JSON.stringify(scene.audio)})} from={${scene.leadSeconds}*fps} premountFor={fps}/>
  <div style={{position:'absolute',left:100,top:903,width:2866,scale:.6,transformOrigin:'top left'}}>
   <BasicCaptions name="English captions" premountFor={fps} width={2866} combineTokensWithinMilliseconds={0} captions={${JSON.stringify(scene.captions)}}/>
  </div>
 </>;
};`;
  writeFileSync(`src/scenes/${scene.id}.tsx`, source);
}
const imports = scenes
  .map((s) => `import {${s.id}Scene} from './scenes/${s.id}';`)
  .join("\n");
const sequences = scenes
  .map(
    (s) =>
      `<Series.Sequence name=${JSON.stringify(s.title)} durationInFrames={${s.durationInFrames}} premountFor={fps}><${s.id}Scene/></Series.Sequence>`,
  )
  .join("\n");
writeFileSync(
  "src/FlyInVideo.tsx",
  `import React from 'react';\nimport {Series,useVideoConfig} from 'remotion';\n${imports}\nexport const FlyInVideo:React.FC=()=>{const {fps}=useVideoConfig();return <Series>${sequences}</Series>;};\n`,
);
const total = scenes.reduce((sum, s) => sum + s.durationInFrames, 0);
const compositions = scenes
  .map(
    (s) =>
      `<Composition id=${JSON.stringify(s.id)} component={${s.id}Scene} width={1920} height={1080} fps={30} durationInFrames={${s.durationInFrames}}/>`,
  )
  .join("\n");
writeFileSync(
  "src/Root.tsx",
  `import React from 'react';\nimport {Composition,Folder} from 'remotion';\nimport {FlyInVideo} from './FlyInVideo';\n${imports}\nexport const RemotionRoot:React.FC=()=> <><Composition id="FlyInExplained" component={FlyInVideo} width={1920} height={1080} fps={30} durationInFrames={${total}}/><Folder name="Chapters">${compositions}</Folder></>;\n`,
);
for (const old of [
  "Idea",
  "Map",
  "Graph",
  "Demo",
  "Restricted",
  "States",
  "Astar",
  "Reservations",
  "Output",
  "Run",
  "Defense",
  "Estimate",
]) {
  if (scenes.some((s) => s.id === old)) continue;
  for (const path of [`src/scenes/${old}.tsx`, `public/${old}.m4a`])
    if (existsSync(path)) unlinkSync(path);
}
console.log(`Built ${scenes.length} visual chapters, ${total / 30}s.`);
