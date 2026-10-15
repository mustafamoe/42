# Fly-in: complete visual walkthrough

**9 minutes 4 seconds.** A standalone explanation of the project,
its Python implementation, and the reasons behind its design.

Watch at <http://localhost:3123/FlyInExplained>. Press Play.
Expand Chapters in the preview to inspect an individual section.

| Time | Chapter |
| --- | --- |
| 00:00 | Deliver the whole fleet |
| 00:14 | The network is a graph |
| 00:31 | Read the map format |
| 00:57 | Three responsibilities |
| 01:13 | Python tools, by role |
| 01:38 | Objects describe the problem |
| 02:04 | Validate before planning |
| 02:29 | Build the adjacency list |
| 02:45 | Check two separate limits |
| 03:08 | Three turns, two drones |
| 03:24 | Use alternate routes |
| 03:40 | Destination type sets the cost |
| 03:58 | Reserve the restricted arrival |
| 04:16 | Compute the remaining time |
| 04:40 | Search location AND time |
| 04:56 | A* chooses what to explore |
| 05:19 | Offer a wait or a move |
| 05:39 | Book zones and connections |
| 06:02 | Turn predecessors into a route |
| 06:17 | Plan the fleet in order |
| 06:39 | Convert actions into output |
| 07:03 | Use colors without changing tokens |
| 07:27 | Run and inspect the program |
| 07:53 | Check behavior, style, and types |
| 08:19 | Understand the trade-off |
| 08:49 | From map to safe arrivals |

The narration determines the duration: there are no forced scene-length holds.
Sentence gaps are 160 ms; section transitions are at most 0.34 seconds.
Leading and trailing silence are trimmed from each speech segment.
The audio check found no silent interval lasting one second.

`lesson.json` owns the narration. `npm run regenerate` rebuilds local speech,
timed captions, and the timeline. `npm run dev` starts the preview.
Existing narration is included; regeneration uses macOS say and FFmpeg.

`src/FlyInVideo.tsx` is the complete timeline. Every scene is registered
independently in `src/Root.tsx`. `src/Visuals.tsx` contains animated graph
examples; `src/DeepVisuals.tsx` connects diagrams, domain objects, and code.
`transcript.txt` contains the complete narration.

Validation: ESLint and TypeScript; flake8 and mypy for the asset builder;
52 chapter/phase layout checks; trimmed-audio timing and silence checks.
The project's 17 private tests pass. Source hashes confirm that the submitted
Python files were not changed by this video work.
