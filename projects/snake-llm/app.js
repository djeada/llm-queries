function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000)
        .toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

function getCookie(name) {
    const match = document.cookie.match(
        new RegExp('(?:^|; )' + name + '=([^;]*)')
    );
    return match ? decodeURIComponent(match[1]) : null;
}


const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const controllerMode = document.getElementById('controller-mode');
const llmStatus = document.getElementById('llm-status');
const gridSize = 20;
const cellSize = canvas.width / gridSize;
const LLM_ENDPOINT = 'http://localhost:8787/snake/decide';
let isPaused = false;
let lastTapTime = 0;


let game;
let highScore = parseInt(getCookie('SNAKE_HIGH_SCORE')) || 0;

const Directions = {
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

function directionToName(direction) {
    return Object.keys(Directions).find(name =>
        Directions[name].x === direction.x && Directions[name].y === direction.y
    ) || 'right';
}

function setLlmStatus(message) {
    if (llmStatus) llmStatus.textContent = message;
}

function isReverseDirection(currentDirection, candidateDirection) {
    return currentDirection.x === -candidateDirection.x &&
        currentDirection.y === -candidateDirection.y;
}

function isSameDirection(currentDirection, candidateDirection) {
    return currentDirection.x === candidateDirection.x &&
        currentDirection.y === candidateDirection.y;
}

function getNextHead(head, direction) {
    return {
        x: head.x + direction.x,
        y: head.y + direction.y
    };
}

function isCellBlocked(gameState, position) {
    if (position.x < 0 || position.x >= gridSize || position.y < 0 || position.y >= gridSize) return true;
    if (gameState.obstacles.some(obs => obs.x === position.x && obs.y === position.y)) return true;

    const bodyWithoutTail = gameState.snake.body.slice(0, -1);
    return bodyWithoutTail.some(segment => segment.x === position.x && segment.y === position.y);
}

function getLegalMoves(gameState) {
    const currentDirection = gameState.snake.direction;
    const head = gameState.snake.head();

    return Object.entries(Directions)
        .filter(([, direction]) => !isReverseDirection(currentDirection, direction))
        .filter(([, direction]) => !isCellBlocked(gameState, getNextHead(head, direction)))
        .map(([name]) => name);
}

function getSafeMove(gameState) {
    const legalMoves = getLegalMoves(gameState);
    if (legalMoves.length === 0) return directionToName(gameState.snake.direction);

    const head = gameState.snake.head();
    const currentDirectionName = directionToName(gameState.snake.direction);
    const rankedMoves = legalMoves
        .map(name => {
            const nextHead = getNextHead(head, Directions[name]);
            const distance = Math.abs(nextHead.x - gameState.food.x) + Math.abs(nextHead.y - gameState.food.y);
            const turnPenalty = name === currentDirectionName ? 0 : 0.25;
            return {
                name,
                score: distance + turnPenalty
            };
        })
        .sort((a, b) => a.score - b.score);

    return rankedMoves[0].name;
}

function applyControllerMove(gameState, moveName, source) {
    if (!Directions[moveName]) return false;

    const legalMoves = getLegalMoves(gameState);
    if (!legalMoves.includes(moveName)) return false;

    const direction = Directions[moveName];
    if (isSameDirection(gameState.snake.direction, direction)) return true;

    gameState.snake.setDirection(direction);
    if (source === 'llm') setLlmStatus(`LLM move: ${moveName}`);
    return true;
}

function getControllerMode() {
    return controllerMode ? controllerMode.value : 'human';
}

class LlmController {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.pending = false;
        this.lastRequestTime = 0;
        this.requestGapMs = 250;
        this.timeoutMs = 8000;
    }

    update(gameState) {
        if (gameState.gameOver || isPaused) return;

        const safeMove = getSafeMove(gameState);
        applyControllerMove(gameState, safeMove, 'fallback');

        if (this.pending) return;

        const now = Date.now();
        if (now - this.lastRequestTime < this.requestGapMs) return;

        this.pending = true;
        this.lastRequestTime = now;
        setLlmStatus('LLM thinking...');

        const controllerState = gameState.getStateForController();
        const timeout = new AbortController();
        const timeoutId = window.setTimeout(() => timeout.abort(), this.timeoutMs);

        fetch(this.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(controllerState),
                signal: timeout.signal
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(decision => {
                const move = typeof decision.move === 'string' ? decision.move.toLowerCase() : '';
                const applied = applyControllerMove(gameState, move, 'llm');
                if (!applied) setLlmStatus(`Rejected LLM move: ${move || 'none'}`);
            })
            .catch(error => {
                const message = error.name === 'AbortError' ? 'LLM timeout; using safe fallback' : 'LLM unavailable; using safe fallback';
                setLlmStatus(message);
            })
            .finally(() => {
                window.clearTimeout(timeoutId);
                this.pending = false;
            });
    }
}

const llmController = new LlmController(LLM_ENDPOINT);



class Game {
    constructor() {
        this.grid = Array(gridSize).fill(null).map(() => Array(gridSize).fill(CellState.EMPTY));
        this.snake = new Snake();
        this.food = new Food();
        this.level = 1;
        this.score = 0;
        this.speed = 200;
        this.gameOver = false;
        this.interval = null;
        this.obstacles = [];
    }

    start() {
        this.reset();
        this.interval = setInterval(() => this.gameLoop(), this.speed);
    }

    reset() {
        this.grid.forEach(row => row.fill(CellState.EMPTY));
        this.snake.reset();
        this.food.place(this.snake.body);
        this.level = 1;
        this.score = 0;
        this.speed = 200;
        this.gameOver = false;
        this.obstacles = [];
        this.generateObstacles();
    }

    gameLoop() {
        if (this.gameOver || isPaused) return;

        if (getControllerMode() === 'llm') {
            llmController.update(this);
        }

        this.snake.move();

        if (this.checkCollision()) {
            this.endGame();
            return;
        }

        if (this.snake.eat(this.food)) {
            this.score++;
            if (this.score > highScore) {
                highScore = this.score;
                setCookie('SNAKE_HIGH_SCORE', highScore, 365);
            }
            this.food.place(this.snake.body.concat(this.obstacles));
            if (this.score % 5 === 0) this.levelUp();
        }

        this.render();
    }

    getStateForController() {
        return {
            gridSize,
            head: {
                ...this.snake.head()
            },
            snake: this.snake.body.map(segment => ({
                ...segment
            })),
            direction: directionToName(this.snake.direction),
            food: {
                x: this.food.x,
                y: this.food.y
            },
            obstacles: this.obstacles.map(obstacle => ({
                ...obstacle
            })),
            score: this.score,
            level: this.level,
            legalMoves: getLegalMoves(this)
        };
    }

    checkCollision() {
        const head = this.snake.head();
        if (head.x < 0 || head.x >= gridSize || head.y < 0 || head.y >= gridSize) return true;
        if (this.snake.collidesWithSelf()) return true;
        if (this.obstacles.some(obs => obs.x === head.x && obs.y === head.y)) return true;
        return false;
    }

    endGame() {
        this.gameOver = true;
        clearInterval(this.interval);
        this.renderGameOver();
    }

    levelUp() {
        this.level++;
        this.speed = Math.max(50, this.speed - 20);
        clearInterval(this.interval);
        this.interval = setInterval(() => this.gameLoop(), this.speed);
        this.generateObstacles();
    }

    generateObstacles() {
        for (let i = 0; i < this.level; i++) {
            let obstacle;
            do {
                obstacle = {
                    x: Math.floor(Math.random() * gridSize),
                    y: Math.floor(Math.random() * gridSize)
                };
            } while (this.snake.isOnBody(obstacle.x, obstacle.y) || this.food.isAt(obstacle.x, obstacle.y));
            this.obstacles.push(obstacle);
        }
    }

    render() {

        const FONT = '16px "Helvetica Neue", sans-serif';
        const TEXT_COLOR = 'rgba(255,255,255,0.9)';
        const PANEL_BG = 'rgba(255,255,255,0.15)';
        const PANEL_BORDER = 'rgba(255,255,255,0.4)';
        const SHADOW_COLOR = 'rgba(0,0,0,0.3)';
        const SHADOW_BLUR = 10;
        const RADIUS = 8;
        const PADDING_X = 12;
        const PADDING_Y = 8;


        function drawPanel(textLines, x, y) {
            ctx.font = FONT;

            const widths = textLines.map(t => ctx.measureText(t).width);
            const w = Math.max(...widths) + PADDING_X * 2;
            const h = textLines.length * (parseInt(FONT) + 4) + PADDING_Y * 2;


            ctx.shadowColor = SHADOW_COLOR;
            ctx.shadowBlur = SHADOW_BLUR;


            ctx.fillStyle = PANEL_BG;
            ctx.strokeStyle = PANEL_BORDER;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x + RADIUS, y);
            ctx.lineTo(x + w - RADIUS, y);
            ctx.quadraticCurveTo(x + w, y, x + w, y + RADIUS);
            ctx.lineTo(x + w, y + h - RADIUS);
            ctx.quadraticCurveTo(x + w, y + h, x + w - RADIUS, y + h);
            ctx.lineTo(x + RADIUS, y + h);
            ctx.quadraticCurveTo(x, y + h, x, y + h - RADIUS);
            ctx.lineTo(x, y + RADIUS);
            ctx.quadraticCurveTo(x, y, x + RADIUS, y);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();


            ctx.shadowBlur = 0;


            ctx.fillStyle = TEXT_COLOR;
            ctx.textBaseline = 'top';
            ctx.textAlign = 'left';
            textLines.forEach((line, i) => {
                ctx.fillText(
                    line,
                    x + PADDING_X,
                    y + PADDING_Y + i * (parseInt(FONT) + 4)
                );
            });

            return w;
        }


        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let y = 0; y < gridSize; y++) {
            for (let x = 0; x < gridSize; x++) {
                ctx.fillStyle = (x + y) % 2 === 0 ? '#AAD751' : '#A2D149';
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }


        ctx.fillStyle = '#8B4513';
        this.obstacles.forEach(o =>
            ctx.fillRect(o.x * cellSize, o.y * cellSize, cellSize, cellSize)
        );
        this.food.render();
        this.snake.render();



        drawPanel(
            [`Score: ${this.score}`, `High: ${highScore}`],
            10, 10
        );


        const lvlText = [`Level: ${this.level}`];
        const panelW = drawPanel(
            lvlText,
            canvas.width - 10 - (ctx.measureText(lvlText[0]).width + PADDING_X * 2),
            10
        );
    }

    renderGameOver() {

        const FONT_TITLE = '36px "Helvetica Neue", sans-serif';
        const FONT_BODY = '20px "Helvetica Neue", sans-serif';
        const TEXT_COLOR = 'rgba(255,255,255,0.9)';
        const PANEL_BG = 'rgba(0, 0, 0, 0.6)';
        const PANEL_BORDER = 'rgba(255,255,255,0.3)';
        const SHADOW_COLOR = 'rgba(0,0,0,0.4)';
        const SHADOW_BLUR = 12;
        const RADIUS = 12;
        const PADDING = 20;

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;


        const lines = [{
                text: 'Game Over',
                font: FONT_TITLE,
                gap: 0
            },
            {
                text: `Score: ${this.score}`,
                font: FONT_BODY,
                gap: 16
            },
            {
                text: 'Tap to Restart',
                font: FONT_BODY,
                gap: 32
            },
        ];


        ctx.textAlign = 'center';
        let panelWidth = 0;
        let panelHeight = PADDING * 2;
        lines.forEach(({
            text,
            font,
            gap
        }) => {
            ctx.font = font;
            const w = ctx.measureText(text).width;
            panelWidth = Math.max(panelWidth, w);
            panelHeight += parseInt(font) + gap;
        });
        panelWidth += PADDING * 2;

        const panelX = centerX - panelWidth / 2;
        const panelY = centerY - panelHeight / 2;


        ctx.shadowColor = SHADOW_COLOR;
        ctx.shadowBlur = SHADOW_BLUR;


        ctx.fillStyle = PANEL_BG;
        ctx.strokeStyle = PANEL_BORDER;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(panelX + RADIUS, panelY);
        ctx.lineTo(panelX + panelWidth - RADIUS, panelY);
        ctx.quadraticCurveTo(panelX + panelWidth, panelY, panelX + panelWidth, panelY + RADIUS);
        ctx.lineTo(panelX + panelWidth, panelY + panelHeight - RADIUS);
        ctx.quadraticCurveTo(panelX + panelWidth, panelY + panelHeight, panelX + panelWidth - RADIUS, panelY + panelHeight);
        ctx.lineTo(panelX + RADIUS, panelY + panelHeight);
        ctx.quadraticCurveTo(panelX, panelY + panelHeight, panelX, panelY + panelHeight - RADIUS);
        ctx.lineTo(panelX, panelY + RADIUS);
        ctx.quadraticCurveTo(panelX, panelY, panelX + RADIUS, panelY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();


        ctx.shadowBlur = 0;


        let cursorY = panelY + PADDING;
        lines.forEach(({
            text,
            font,
            gap
        }) => {
            ctx.font = font;
            ctx.fillStyle = TEXT_COLOR;
            ctx.textBaseline = 'top';
            ctx.fillText(text, centerX, cursorY);
            cursorY += parseInt(font) + gap;
        });
    }

}

class Snake {
    constructor() {
        this.body = [];
        this.direction = {
            x: 1,
            y: 0
        };
        this.nextDirection = {
            x: 1,
            y: 0
        };
        this.reset();
    }

    reset() {
        this.body = [{
            x: Math.floor(gridSize / 2),
            y: Math.floor(gridSize / 2)
        }];
        this.direction = {
            x: 1,
            y: 0
        };
        this.nextDirection = {
            x: 1,
            y: 0
        };
    }

    move() {
        this.direction = this.nextDirection;
        const head = {
            x: this.head().x + this.direction.x,
            y: this.head().y + this.direction.y
        };
        this.body.unshift(head);
        this.body.pop();
    }

    grow() {
        const tail = this.body[this.body.length - 1];
        this.body.push({
            x: tail.x,
            y: tail.y
        });
    }

    eat(food) {
        if (this.head().x === food.x && this.head().y === food.y) {
            this.grow();
            return true;
        }
        return false;
    }

    head() {
        return this.body[0];
    }

    isOnBody(x, y) {
        return this.body.some(segment => segment.x === x && segment.y === y);
    }

    collidesWithSelf() {
        const head = this.head();
        return this.body.slice(1).some(segment => segment.x === head.x && segment.y === head.y);
    }

    setDirection(newDirection) {
        if ((this.direction.x !== -newDirection.x || this.direction.y !== -newDirection.y) &&
            (this.direction.x !== newDirection.x || this.direction.y !== newDirection.y)) {
            this.nextDirection = newDirection;
        }
    }

    render() {

        ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
        ctx.shadowBlur = 4;

        this.body.forEach((segment, index) => {
            const x = segment.x * cellSize;
            const y = segment.y * cellSize;

            if (index === 0) {

                ctx.fillStyle = 'darkgreen';
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 2;
                ctx.fillRect(x, y, cellSize, cellSize);
                ctx.strokeRect(x, y, cellSize, cellSize);


                const eyeSize = cellSize / 6;
                const eyeOffsetX = this.direction.x === 0 ?
                    cellSize / 4 :
                    (this.direction.x > 0 ?
                        3 * cellSize / 4 - eyeSize / 2 :
                        cellSize / 4 - eyeSize / 2);
                const eyeOffsetY = this.direction.y === 0 ?
                    cellSize / 4 :
                    (this.direction.y > 0 ?
                        3 * cellSize / 4 - eyeSize / 2 :
                        cellSize / 4 - eyeSize / 2);

                ctx.fillStyle = 'white';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 1;
                ctx.fillRect(x + eyeOffsetX, y + eyeOffsetY, eyeSize, eyeSize);
                ctx.strokeRect(x + eyeOffsetX, y + eyeOffsetY, eyeSize, eyeSize);

            } else {

                ctx.fillStyle = 'green';
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 1;
                ctx.fillRect(x, y, cellSize, cellSize);
                ctx.strokeRect(x, y, cellSize, cellSize);
            }
        });


        ctx.shadowBlur = 0;
    }

}

class Food {
    constructor() {
        this.x = 0;
        this.y = 0;
    }

    place(occupiedPositions) {
        let validPosition = false;
        while (!validPosition) {
            this.x = Math.floor(Math.random() * gridSize);
            this.y = Math.floor(Math.random() * gridSize);
            if (!occupiedPositions.some(pos => pos.x === this.x && pos.y === this.y)) {
                validPosition = true;
            }
        }
    }

    isAt(x, y) {
        return this.x === x && this.y === y;
    }

    render() {
        const x = this.x * cellSize + cellSize / 2;
        const y = this.y * cellSize + cellSize / 2;
        const radius = cellSize * 0.4;


        ctx.save();
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 4;
        ctx.shadowOffsetX = 1;
        ctx.shadowOffsetY = 1;


        const grad = ctx.createRadialGradient(
            x - radius * 0.3, y - radius * 0.3, radius * 0.2,
            x, y, radius
        );
        grad.addColorStop(0, '#ff6b6b');
        grad.addColorStop(1, '#c0392b');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();


        ctx.restore();


        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.beginPath();
        ctx.ellipse(
            x - radius * 0.3,
            y - radius * 0.3,
            radius * 0.3,
            radius * 0.2,
            -Math.PI / 4,
            0,
            Math.PI * 2
        );
        ctx.fill();


        ctx.strokeStyle = 'rgba(0,0,0,0.2)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.stroke();
    }

}


const CellState = {
    EMPTY: 'empty',
    SNAKE: 'snake',
    FOOD: 'food',
    OBSTACLE: 'obstacle'
};


window.addEventListener('keydown', e => {
    const directionKeys = {
        ArrowUp: {
            x: 0,
            y: -1
        },
        ArrowDown: {
            x: 0,
            y: 1
        },
        ArrowLeft: {
            x: -1,
            y: 0
        },
        ArrowRight: {
            x: 1,
            y: 0
        },
        w: {
            x: 0,
            y: -1
        },
        s: {
            x: 0,
            y: 1
        },
        a: {
            x: -1,
            y: 0
        },
        d: {
            x: 1,
            y: 0
        }
    };

    if (directionKeys[e.key]) {
        game.snake.setDirection(directionKeys[e.key]);
        e.preventDefault();

    } else if (e.key === ' ') {

        if (game && game.gameOver) {
            game.reset();
            game.start();
        } else {
            isPaused = !isPaused;
            if (isPaused) {
                renderPauseOverlay();
            } else {
                game.render();
            }
        }
        e.preventDefault();

    } else if (e.key === 'Escape' && game && game.gameOver) {

        game.reset();
        game.start();
    }
});



let touchStartPos = null;
canvas.addEventListener('touchstart', e => {
    touchStartPos = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY
    };
    e.preventDefault();
});

canvas.addEventListener('touchmove', e => {
    if (!touchStartPos) return;
    const dx = e.touches[0].clientX - touchStartPos.x;
    const dy = e.touches[0].clientY - touchStartPos.y;

    if (Math.abs(dx) > Math.abs(dy)) {
        const newDirection = dx > 0 ? {
            x: 1,
            y: 0
        } : {
            x: -1,
            y: 0
        };
        game.snake.setDirection(newDirection);
    } else {
        const newDirection = dy > 0 ? {
            x: 0,
            y: 1
        } : {
            x: 0,
            y: -1
        };
        game.snake.setDirection(newDirection);
    }

    touchStartPos = null;
    e.preventDefault();
});

canvas.addEventListener('touchend', e => {
    const currentTime = new Date().getTime();
    const tapLength = currentTime - lastTapTime;

    if (tapLength < 300 && tapLength > 0) {
        if (game.gameOver) {
            game.reset();
            game.start();
            return;
        }
        isPaused = !isPaused;
        if (isPaused) renderPauseOverlay();
        else game.render();
        e.preventDefault();
        return;
    }

    lastTapTime = currentTime;
});


function renderPauseOverlay() {
    if (game.gameOver) return;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'white';
    ctx.font = '30px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Paused', canvas.width / 2, canvas.height / 2);
    ctx.fillText('Tap to Resume', canvas.width / 2, canvas.height / 2 + 40);
}


function preventDefaultTouch(e) {
    e.preventDefault();
}

function disableScrolling() {
    document.addEventListener('touchstart', preventDefaultTouch, {
        passive: false
    });
    document.addEventListener('touchmove', preventDefaultTouch, {
        passive: false
    });
    document.body.classList.add('no-scroll');
}

function enableScrolling() {
    document.removeEventListener('touchstart', preventDefaultTouch);
    document.removeEventListener('touchmove', preventDefaultTouch);
    document.body.classList.remove('no-scroll');
}


function renderStartScreen() {

    const BG_COLOR = '#AAD751';
    const FONT_TITLE = '48px "Helvetica Neue", sans-serif';
    const FONT_BODY = '24px "Helvetica Neue", sans-serif';
    const TEXT_COLOR = 'rgba(255,255,255,0.9)';
    const PANEL_BG = 'rgba(0, 0, 0, 0.4)';
    const PANEL_BORDER = 'rgba(255,255,255,0.3)';
    const SHADOW_COLOR = 'rgba(0,0,0,0.4)';
    const SHADOW_BLUR = 10;
    const RADIUS = 12;
    const PADDING = 24;


    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, canvas.width, canvas.height);


    const lines = [{
            text: 'Snake Game',
            font: FONT_TITLE,
            gap: 16
        },
        {
            text: 'Tap to Start',
            font: FONT_BODY,
            gap: 12
        },
        {
            text: `High Score: ${highScore}`,
            font: FONT_BODY,
            gap: 0
        },
    ];


    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;


    ctx.textAlign = 'center';
    let panelWidth = 0;
    let panelHeight = PADDING * 2;
    lines.forEach(({
        text,
        font,
        gap
    }) => {
        ctx.font = font;
        const w = ctx.measureText(text).width;
        panelWidth = Math.max(panelWidth, w);
        panelHeight += parseInt(font) + gap;
    });
    panelWidth += PADDING * 2;
    const panelX = centerX - panelWidth / 2;
    const panelY = centerY - panelHeight / 2;


    ctx.shadowColor = SHADOW_COLOR;
    ctx.shadowBlur = SHADOW_BLUR;


    ctx.fillStyle = PANEL_BG;
    ctx.strokeStyle = PANEL_BORDER;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(panelX + RADIUS, panelY);
    ctx.lineTo(panelX + panelWidth - RADIUS, panelY);
    ctx.quadraticCurveTo(panelX + panelWidth, panelY, panelX + panelWidth, panelY + RADIUS);
    ctx.lineTo(panelX + panelWidth, panelY + panelHeight - RADIUS);
    ctx.quadraticCurveTo(panelX + panelWidth, panelY + panelHeight, panelX + panelWidth - RADIUS, panelY + panelHeight);
    ctx.lineTo(panelX + RADIUS, panelY + panelHeight);
    ctx.quadraticCurveTo(panelX, panelY + panelHeight, panelX, panelY + panelHeight - RADIUS);
    ctx.lineTo(panelX, panelY + RADIUS);
    ctx.quadraticCurveTo(panelX, panelY, panelX + RADIUS, panelY);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();


    ctx.shadowBlur = 0;


    let cursorY = panelY + PADDING;
    lines.forEach(({
        text,
        font,
        gap
    }) => {
        ctx.font = font;
        ctx.fillStyle = TEXT_COLOR;
        ctx.textBaseline = 'top';
        ctx.fillText(text, centerX, cursorY);
        cursorY += parseInt(font) + gap;
    });
}


canvas.addEventListener('click', () => {
    if (!game || game.gameOver) {
        game = new Game();
        game.start();
    }
});

canvas.addEventListener('touchstart', e => {
    if (!game || game.gameOver) {
        game = new Game();
        game.start();
    }
});


renderStartScreen();
disableScrolling();
