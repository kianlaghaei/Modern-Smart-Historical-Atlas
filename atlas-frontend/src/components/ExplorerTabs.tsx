import { useState } from "react";
import { useAtlasStore } from "../context/atlasStore";

export default function ExplorerTabs() {
  const atlas = useAtlasStore((s) => s.atlas);
  const [tab, setTab] = useState<"locations" | "people" | "writings" | "events">("locations");
  const data = atlas ? (atlas as any)[tab] : [];

  return (
    <div>
      <div className="flex space-x-2">
        {["locations", "people", "writings", "events"].map((t) => (
          <button
            key={t}
            className={`px-3 py-1 ${tab === t ? "bg-blue-500 text-white" : "bg-gray-200"}`}
            onClick={() => setTab(t as any)}
          >
            {t}
          </button>
        ))}
      </div>
      <ul className="mt-2 max-h-48 overflow-auto">
        {data.map((item: any) => (
          <li key={item.id} className="border-b py-1">
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
