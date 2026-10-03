#!/usr/bin/env node

'use strict';

const assert = require('node:assert/strict');
const {
    normalizeMove,
    fallbackMove,
    directionVector,
    buildDecisionState,
    createServer
} = require('./snake_llm_proxy');

function sampleState() {
    return {
        gridSize: 20,
        head: {x: 10, y: 10},
        snake: [{x: 10, y: 10}],
        direction: 'right',
        food: {x: 14, y: 10},
        obstacles: [],
        score: 0,
        level: 1,
        legalMoves: ['up', 'down', 'right']
    };
}

async function withServer(decide, run) {
    const server = createServer(decide);
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const address = server.address();
    try {
        await run(`http://127.0.0.1:${address.port}`);
    } finally {
        await new Promise((resolve, reject) =>
            server.close(error => (error ? reject(error) : resolve()))
        );
    }
}

async function postState(baseUrl, state) {
    const response = await fetch(`${baseUrl}/snake/decide`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(state)
    });
    assert.equal(response.status, 200);
    return response.json();
}

async function main() {
    assert.equal(normalizeMove(' UP ', ['up', 'right']), 'up');
    assert.equal(normalizeMove('left', ['up', 'right']), null);
    assert.equal(normalizeMove('jump', ['up']), null);
    assert.equal(normalizeMove(null, ['up']), null);

    assert.equal(
        fallbackMove({legalMoves: ['down', 'left'], direction: 'right'}),
        'down'
    );
    assert.equal(fallbackMove({legalMoves: [], direction: 'left'}), 'left');
    assert.deepEqual(directionVector('left'), {x: -1, y: 0});

    const decision = buildDecisionState(sampleState());
    const right = decision.candidateMoves.find(item => item.move === 'right');
    const up = decision.candidateMoves.find(item => item.move === 'up');
    assert.equal(right.distanceToFood, 3);
    assert.equal(right.keepsDirection, true);
    assert.equal(up.distanceToFood, 5);

    await withServer(async () => 'up', async baseUrl => {
        const body = await postState(baseUrl, sampleState());
        assert.deepEqual(body, {move: 'up'});
    });

    await withServer(async () => 'left', async baseUrl => {
        const body = await postState(baseUrl, sampleState());
        assert.equal(body.move, 'up');
    });

    await withServer(
        async () => {
            throw new Error('simulated model failure');
        },
        async baseUrl => {
            const body = await postState(baseUrl, sampleState());
            assert.equal(body.move, 'up');
            assert.equal(body.fallback, true);
            assert.match(body.error, /simulated model failure/);
        }
    );

    console.log('snake proxy unit checks passed');
}

main().catch(error => {
    console.error(error);
    process.exitCode = 1;
});
