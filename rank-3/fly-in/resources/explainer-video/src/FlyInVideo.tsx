import React from "react";
import { Series, useVideoConfig } from "remotion";
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
export const FlyInVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      <Series.Sequence
        name="Deliver the whole fleet"
        durationInFrames={429}
        premountFor={fps}
      >
        <IntroScene />
      </Series.Sequence>
      <Series.Sequence
        name="The network is a graph"
        durationInFrames={511}
        premountFor={fps}
      >
        <NetworkScene />
      </Series.Sequence>
      <Series.Sequence
        name="Read the map format"
        durationInFrames={788}
        premountFor={fps}
      >
        <InputScene />
      </Series.Sequence>
      <Series.Sequence
        name="Three responsibilities"
        durationInFrames={473}
        premountFor={fps}
      >
        <PipelineScene />
      </Series.Sequence>
      <Series.Sequence
        name="Python tools, by role"
        durationInFrames={748}
        premountFor={fps}
      >
        <ToolkitScene />
      </Series.Sequence>
      <Series.Sequence
        name="Objects describe the problem"
        durationInFrames={793}
        premountFor={fps}
      >
        <ModelsScene />
      </Series.Sequence>
      <Series.Sequence
        name="Validate before planning"
        durationInFrames={754}
        premountFor={fps}
      >
        <ParsingScene />
      </Series.Sequence>
      <Series.Sequence
        name="Build the adjacency list"
        durationInFrames={459}
        premountFor={fps}
      >
        <AdjacencyScene />
      </Series.Sequence>
      <Series.Sequence
        name="Check two separate limits"
        durationInFrames={702}
        premountFor={fps}
      >
        <CapacityScene />
      </Series.Sequence>
      <Series.Sequence
        name="Three turns, two drones"
        durationInFrames={484}
        premountFor={fps}
      >
        <TurnsScene />
      </Series.Sequence>
      <Series.Sequence
        name="Use alternate routes"
        durationInFrames={470}
        premountFor={fps}
      >
        <ParallelScene />
      </Series.Sequence>
      <Series.Sequence
        name="Destination type sets the cost"
        durationInFrames={531}
        premountFor={fps}
      >
        <CostsScene />
      </Series.Sequence>
      <Series.Sequence
        name="Reserve the restricted arrival"
        durationInFrames={549}
        premountFor={fps}
      >
        <TransitScene />
      </Series.Sequence>
      <Series.Sequence
        name="Compute the remaining time"
        durationInFrames={722}
        premountFor={fps}
      >
        <DijkstraScene />
      </Series.Sequence>
      <Series.Sequence
        name="Search location AND time"
        durationInFrames={495}
        premountFor={fps}
      >
        <SearchScene />
      </Series.Sequence>
      <Series.Sequence
        name="A* chooses what to explore"
        durationInFrames={685}
        premountFor={fps}
      >
        <HeapScene />
      </Series.Sequence>
      <Series.Sequence
        name="Offer a wait or a move"
        durationInFrames={603}
        premountFor={fps}
      >
        <WaitingScene />
      </Series.Sequence>
      <Series.Sequence
        name="Book zones and connections"
        durationInFrames={677}
        premountFor={fps}
      >
        <ReserveScene />
      </Series.Sequence>
      <Series.Sequence
        name="Turn predecessors into a route"
        durationInFrames={447}
        premountFor={fps}
      >
        <ReconstructScene />
      </Series.Sequence>
      <Series.Sequence
        name="Plan the fleet in order"
        durationInFrames={673}
        premountFor={fps}
      >
        <PlanningScene />
      </Series.Sequence>
      <Series.Sequence
        name="Convert actions into output"
        durationInFrames={717}
        premountFor={fps}
      >
        <MovementOutputScene />
      </Series.Sequence>
      <Series.Sequence
        name="Use colors without changing tokens"
        durationInFrames={706}
        premountFor={fps}
      >
        <ColorsScene />
      </Series.Sequence>
      <Series.Sequence
        name="Run and inspect the program"
        durationInFrames={782}
        premountFor={fps}
      >
        <LaunchScene />
      </Series.Sequence>
      <Series.Sequence
        name="Check behavior, style, and types"
        durationInFrames={799}
        premountFor={fps}
      >
        <ChecksScene />
      </Series.Sequence>
      <Series.Sequence
        name="Understand the trade-off"
        durationInFrames={874}
        premountFor={fps}
      >
        <LimitsScene />
      </Series.Sequence>
      <Series.Sequence
        name="From map to safe arrivals"
        durationInFrames={453}
        premountFor={fps}
      >
        <RecapScene />
      </Series.Sequence>
    </Series>
  );
};
