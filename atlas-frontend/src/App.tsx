import { useEffect } from "react";
import MapView from "./components/MapView";
import Timeline from "./components/Timeline";
import ExplorerTabs from "./components/ExplorerTabs";
import Inspector from "./components/Inspector";
import { useAtlasStore } from "./context/atlasStore";

function App() {
  const fetchAtlas = useAtlasStore((s) => s.fetchAtlas);

  useEffect(() => {
    fetchAtlas();
  }, [fetchAtlas]);

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      <div className="md:w-2/3 h-1/2 md:h-screen">
        <MapView />
      </div>
      <div className="md:w-1/3 p-4 space-y-4 overflow-auto">
        <ExplorerTabs />
        <Timeline />
        <Inspector />
      </div>
    </div>
  );
}

export default App;
