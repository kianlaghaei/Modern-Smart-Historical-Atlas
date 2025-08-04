import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useAtlasStore } from "../context/atlasStore";

export default function MapView() {
  const atlas = useAtlasStore((s) => s.atlas);
  const locations = atlas?.locations ?? [];
  const events = atlas?.events ?? [];

  const journeyLines = events
    .filter((e) => e.type === "journey" && e.journeyPath)
    .map((e) =>
      e.journeyPath!
        .map((id) => locations.find((l) => l.id === id)?.coords)
        .filter(Boolean) as [number, number][]
    );

  return (
    <MapContainer className="w-full h-full" center={[0, 0]} zoom={2}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {locations.map((loc) => (
        <Marker key={loc.id} position={loc.coords}>
          <Popup>{loc.name}</Popup>
        </Marker>
      ))}
      {journeyLines.map((coords, i) => (
        <Polyline key={i} positions={coords} />
      ))}
    </MapContainer>
  );
}
