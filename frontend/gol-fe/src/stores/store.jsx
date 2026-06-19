import { create } from "zustand";
import { cantor_calcul } from "../utils/common";

export const useSimulationStore = create((set, get) => ({
  generation: 0,
  isRunning: false,
  currentGrid: new Map(),
  send: null,
  numberCellHeight: 90,
  numberCellWidth: 90,

  setSend: (sendFn) => set({ send: sendFn }),

  setGeneration: (g) => set({ generation: g }),
  setIsRunning: (v) => set({ isRunning: v }),

  setNumberCellWidth: (w) => set({ numberCellWidth: w }),
  setNumberCellHeight: (h) => set({ numberCellHeight: h }),


  setFullGrid: (grid, tick) => {
    const newGrid = new Map();

    for (const c of grid) {
      newGrid.set(
        cantor_calcul(c[0], c[1]),
        { tick, x: c[0], y: c[1] }
      );
    }

    set({
      currentGrid: newGrid,
      generation: tick,
    });
  },

  applyBirthDeath: (birth, death, tick) => {
    const newGrid = new Map(get().currentGrid);

    for (const c of birth) {
      newGrid.set(
        cantor_calcul(c[0], c[1]),
        { tick, x: c[0], y: c[1] }
      );
    }

    for (const c of death) {
      newGrid.delete(cantor_calcul(c[0], c[1]));
    }

    set({
      currentGrid: newGrid,
      generation: tick,
    });
  },

  resetLocal: () =>
    set({
      currentGrid: new Map(),
      generation: 0,
      isRunning: false,
    }),

  start: () => {
    const send = get().send;
    send?.({ type: "start" });
  },

  stop: () => {
    const send = get().send;
    send?.({ type: "stop" });
  },

  reset: () => {
    const send = get().send;
    send?.({ type: "reset" });
    get().resetLocal();
  },

  toggleCell: (x, y) => {
    const send = get().send;
    send?.({ type: "toggle_cell", x, y });
  },

  setTickRate : (speed) => {
    const send = get().send;
    send?.({ type: "set_speed", speed });
  },

  setGridSize: (width, height) => {
    const send = get().send;
    send?.({ type: "grid_size", width, height});
  },

}));