#!/usr/bin/env node

const http = require('http');

const PORT = Number(process.env.SNAKE_LLM_PORT || 8787);
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434/api/chat';
const MODEL = process.env.SNAKE_LLM_MODEL || 'qwen2.5:1.5b';
const REQUEST_TIMEOUT_MS = Number(process.env.SNAKE_LLM_TIMEOUT_MS || 8000);

const responseSchema = {
    type: 'object',
    properties: {
        move: {
            type: 'string',
            enum: ['up', 'down', 'left', 'right']
        }
    },
    required: ['move'],
    additionalProperties: false
};

function sendJson(res, statusCode, payload) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end(JSON.stringify(payload));
}

function readBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => {
            body += chunk;
            if (body.length > 20000) {
                reject(new Error('Request body too large'));
                req.destroy();
            }
        });
        req.on('end', () => resolve(body));
        req.on('error', reject);
    });
}

function normalizeMove(move, legalMoves) {
    if (typeof move !== 'string') return null;
    const normalized = move.toLowerCase().trim();
    if (!['up', 'down', 'left', 'right'].includes(normalized)) return null;
    if (Array.isArray(legalMoves) && legalMoves.length > 0 && !legalMoves.includes(normalized)) return null;
    return normalized;
}

function fallbackMove(state) {
    if (Array.isArray(state.legalMoves) && state.legalMoves.length > 0) {
        return state.legalMoves[0];
    }
    return state.direction || 'right';
}

function directionVector(move) {
    const directions = {
        up: {
            x: 0,
            y: -1
        },
        down: {
            x: 0,
            y: 1
        },
        left: {
            x: -1,
            y: 0
        },
        right: {
            x: 1,
            y: 0
        }
    };
    return directions[move] || directions.right;
}

function buildDecisionState(state) {
    const legalMoves = Array.isArray(state.legalMoves) ? state.legalMoves : [];
    const candidateMoves = legalMoves.map(move => {
        const direction = directionVector(move);
        const nextHead = {
            x: state.head.x + direction.x,
            y: state.head.y + direction.y
        };
        return {
            move,
            nextHead,
            distanceToFood: Math.abs(nextHead.x - state.food.x) + Math.abs(nextHead.y - state.food.y),
            keepsDirection: move === state.direction
        };
    });

    return {
        ...state,
        candidateMoves
    };
}

async function askOllama(state) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
        const decisionState = buildDecisionState(state);
        const prompt = [
            'You control a Snake game.',
            'Return exactly one JSON object matching this schema: {"move":"up|down|left|right"}.',
            'Choose only from legalMoves.',
            'Pick the candidateMoves item with the smallest distanceToFood.',
            'If there is a tie, keep the current direction when it is legal.',
            '',
            JSON.stringify(decisionState)
        ].join('\n');

        const response = await fetch(OLLAMA_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: MODEL,
                stream: false,
                format: responseSchema,
                options: {
                    temperature: 0,
                    num_predict: 24
                },
                messages: [{
                    role: 'user',
                    content: prompt
                }]
            }),
            signal: controller.signal
        });

        if (!response.ok) {
            throw new Error(`Ollama HTTP ${response.status}`);
        }

        const data = await response.json();
        const content = data.message && data.message.content ? data.message.content : '{}';
        const parsed = JSON.parse(content);
        return normalizeMove(parsed.move, state.legalMoves);
    } finally {
        clearTimeout(timeout);
    }
}

const server = http.createServer(async (req, res) => {
    if (req.method === 'OPTIONS') {
        sendJson(res, 204, {});
        return;
    }

    if (req.method !== 'POST' || req.url !== '/snake/decide') {
        sendJson(res, 404, {
            error: 'Not found'
        });
        return;
    }

    let state = null;

    try {
        const body = await readBody(req);
        state = JSON.parse(body);
        const move = await askOllama(state);

        sendJson(res, 200, {
            move: move || fallbackMove(state)
        });
    } catch (error) {
        sendJson(res, 200, {
            move: state ? fallbackMove(state) : 'right',
            fallback: true,
            error: error.message
        });
    }
});

server.listen(PORT, () => {
    console.log(`Snake LLM proxy listening on http://localhost:${PORT}/snake/decide`);
    console.log(`Using Ollama model: ${MODEL}`);
});
