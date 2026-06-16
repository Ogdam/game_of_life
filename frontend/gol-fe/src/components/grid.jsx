'use client';

import { useEffect, useRef } from 'react';
import { Application, Graphics } from 'pixi.js';
import {cantor_calcul, getCellColor} from '../utils/common';

export default function Grid(props) {
    const containerRef = useRef(null);
    const appRef = useRef(null);
    const renderedCells = useRef(new Map());

    // INIT ONCE
    useEffect(() => {
        let isDestroyed = false;

        (async () => {
            const app = new Application();

            await app.init({
                width: props.width,
                height: props.height,
                background: '#222'
            });

            if (isDestroyed) {
                app.destroy(true, { children: true, texture: true, context: true });
                return;
            }

            app.stage.eventMode = 'static';
            app.stage.hitArea = app.screen;

            appRef.current = app;
            containerRef.current?.appendChild(app.canvas);

            const size = 10;

            app.stage.on('pointerdown', (event) => {
                const pos = event.global;
                const x = Math.floor(pos.x / size);
                const y = Math.floor(pos.y / size);
                props.toggle_cell(x, y);
            });
        })();

        return () => {
            isDestroyed = true;

            if (appRef.current) {
                appRef.current.destroy(true, {
                    children: true,
                    texture: true,
                    context: true
                });
                appRef.current = null;
            }
        };
    }, []);

    useEffect(() => {
        const app = appRef.current;
        if (!app) return;

        const size = 10;
        const map = renderedCells.current;

        // ADD / UPDATE
        for (const [id, data] of props.grid) {
            const cell = map.get(id);

            if (!cell) {
                const newCell = new Graphics();

                newCell.rect(0, 0, size, size);
                newCell.x = data.x * size;
                newCell.y = data.y * size;

                map.set(id, newCell);
                app.stage.addChild(newCell);
            }

            const gfx = map.get(id);

            gfx.clear();
            gfx.rect(0, 0, size, size);
            gfx.fill(getCellColor(props.generation, data.tick));
        }

        // REMOVE
        for (const [id, cell] of map.entries()) {
            if (props.grid.has(id)) continue;

            app.stage.removeChild(cell);
            cell.destroy();
            map.delete(id);
        }

    }, [props.grid, props.generation]);

    return <div ref={containerRef} />;
}