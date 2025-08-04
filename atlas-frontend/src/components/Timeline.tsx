import Plot from "react-plotly.js";
import { useAtlasStore } from "../context/atlasStore";

export default function Timeline() {
  const events = useAtlasStore((s) => s.atlas?.events ?? []);
  const data = [
    {
      type: "scatter",
      mode: "markers",
      x: events.map((e) => e.dateStart),
      y: events.map((e) => e.type),
      text: events.map((e) => e.name),
      marker: { color: "rgb(131, 167, 234)", size: 10 },
    },
  ];

  return <Plot data={data} layout={{ title: "Timeline", yaxis: { type: "category" } }} />;
}
