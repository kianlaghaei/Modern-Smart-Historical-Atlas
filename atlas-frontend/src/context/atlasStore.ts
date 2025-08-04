import { create } from "zustand";
import axios from "axios";

export interface Location {
  id: string;
  name: string;
  type: string;
  coords: [number, number];
  description?: string;
}

export interface Person {
  id: string;
  name: string;
  role?: string;
}

export interface Writing {
  id: string;
  name: string;
  locId?: string;
  year?: number;
}

export interface Event {
  id: string;
  name: string;
  type: string;
  dateStart: string;
  dateEnd?: string;
  locId?: string;
  journeyPath?: string[];
  peopleIds?: string[];
  writingIds?: string[];
  source?: string;
}

export interface AtlasDB {
  locations: Location[];
  people: Person[];
  writings: Writing[];
  events: Event[];
}

interface AtlasState {
  atlas: AtlasDB | null;
  fetchAtlas: () => Promise<void>;
  extractAtlas: (text: string) => Promise<void>;
}

export const useAtlasStore = create<AtlasState>((set) => ({
  atlas: null,
  fetchAtlas: async () => {
    const { data } = await axios.get<AtlasDB>("/api/atlas");
    set({ atlas: data });
  },
  extractAtlas: async (text: string) => {
    const { data } = await axios.post<AtlasDB>("/api/extract", text, {
      headers: { "Content-Type": "text/plain" },
    });
    set({ atlas: data });
  },
}));
