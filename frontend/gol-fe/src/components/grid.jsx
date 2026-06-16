'use client';

import { useEffect, useRef } from 'react';
import { Application, Graphics } from 'pixi.js';

export default function Grid() {
    const containerRef = useRef(null);

    useEffect(() => {
        let app;

        async function init() {
            app = new Application();

            await app.init({
                width: 800,
                height: 600,
                background: '#222222'
            });

            containerRef.current.appendChild(app.canvas);

            const graphics = new Graphics();

            graphics.rect(100, 100, 200, 100);
            graphics.fill(0xff0000);

            app.stage.addChild(graphics);
        }

        init();

        return () => {
            if (app) {
                app.destroy(true);
            }
        };
    }, []);

    return <div ref={containerRef} />;
}