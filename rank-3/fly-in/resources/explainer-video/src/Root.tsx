import React from "react";
import { Composition, Folder } from "remotion";
import { FlyInVideo } from "./FlyInVideo";
import { IntroScene } from "./scenes/Intro";
import { NetworkScene } from "./scenes/Network";
import { InputScene } from "./scenes/Input";
import { PipelineScene } from "./scenes/Pipeline";
import { ToolkitScene } from "./scenes/Toolkit";
import { ModelsScene } from "./scenes/Models";
import { ParsingScene } from "./scenes/Parsing";
import { AdjacencyScene } from "./scenes/Adjacency";
import { CapacityScene } from "./scenes/Capacity";
import { TurnsScene } from "./scenes/Turns";
import { ParallelScene } from "./scenes/Parallel";
import { CostsScene } from "./scenes/Costs";
import { TransitScene } from "./scenes/Transit";
import { DijkstraScene } from "./scenes/Dijkstra";
import { SearchScene } from "./scenes/Search";
import { HeapScene } from "./scenes/Heap";
import { WaitingScene } from "./scenes/Waiting";
import { ReserveScene } from "./scenes/Reserve";
import { ReconstructScene } from "./scenes/Reconstruct";
import { PlanningScene } from "./scenes/Planning";
import { MovementOutputScene } from "./scenes/MovementOutput";
import { ColorsScene } from "./scenes/Colors";
import { LaunchScene } from "./scenes/Launch";
import { ChecksScene } from "./scenes/Checks";
import { LimitsScene } from "./scenes/Limits";
import { RecapScene } from "./scenes/Recap";
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="FlyInExplained"
      component={FlyInVideo}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={16324}
    />
    <Folder name="Chapters">
      <Composition
        id="Intro"
        component={IntroScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={429}
      />
      <Composition
        id="Network"
        component={NetworkScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={511}
      />
      <Composition
        id="Input"
        component={InputScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={788}
      />
      <Composition
        id="Pipeline"
        component={PipelineScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={473}
      />
      <Composition
        id="Toolkit"
        component={ToolkitScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={748}
      />
      <Composition
        id="Models"
        component={ModelsScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={793}
      />
      <Composition
        id="Parsing"
        component={ParsingScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={754}
      />
      <Composition
        id="Adjacency"
        component={AdjacencyScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={459}
      />
      <Composition
        id="Capacity"
        component={CapacityScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={702}
      />
      <Composition
        id="Turns"
        component={TurnsScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={484}
      />
      <Composition
        id="Parallel"
        component={ParallelScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={470}
      />
      <Composition
        id="Costs"
        component={CostsScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={531}
      />
      <Composition
        id="Transit"
        component={TransitScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={549}
      />
      <Composition
        id="Dijkstra"
        component={DijkstraScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={722}
      />
      <Composition
        id="Search"
        component={SearchScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={495}
      />
      <Composition
        id="Heap"
        component={HeapScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={685}
      />
      <Composition
        id="Waiting"
        component={WaitingScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={603}
      />
      <Composition
        id="Reserve"
        component={ReserveScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={677}
      />
      <Composition
        id="Reconstruct"
        component={ReconstructScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={447}
      />
      <Composition
        id="Planning"
        component={PlanningScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={673}
      />
      <Composition
        id="MovementOutput"
        component={MovementOutputScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={717}
      />
      <Composition
        id="Colors"
        component={ColorsScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={706}
      />
      <Composition
        id="Launch"
        component={LaunchScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={782}
      />
      <Composition
        id="Checks"
        component={ChecksScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={799}
      />
      <Composition
        id="Limits"
        component={LimitsScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={874}
      />
      <Composition
        id="Recap"
        component={RecapScene}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={453}
      />
    </Folder>
  </>
);
