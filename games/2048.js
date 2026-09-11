#!/usr/bin/env node

/**
 * 2048 终端版游戏
 * 
 * 操作方式:
 *   方向键 / WASD  - 移动方块
 *   R              - 重新开始
 *   Q / Ctrl+C     - 退出游戏
 * 
 * 运行: node 2048.js
 */

const readline = require('readline');

// ============ 颜色主题 ============
const COLORS = {
    0:    { bg: '\x1b[48;5;236m', fg: '\x1b[38;5;236m' },
    2:    { bg: '\x1b[48;5;230m', fg: '\x1b[38;5;239m' },
    4:    { bg: '\x1b[48;5;223m', fg: '\x1b[38;5;239m' },
    8:    { bg: '\x1b[48;5;216m', fg: '\x1b[38;5;255m' },
    16:   { bg: '\x1b[48;5;215m', fg: '\x1b[38;5;255m' },
    32:   { bg: '\x1b[48;5;203m', fg: '\x1b[38;5;255m' },
    64:   { bg: '\x1b[48;5;196m', fg: '\x1b[38;5;255m' },
    128:  { bg: '\x1b[48;5;220m', fg: '\x1b[38;5;255m' },
    256:  { bg: '\x1b[48;5;178m', fg: '\x1b[38;5;255m' },
    512:  { bg: '\x1b[48;5;172m', fg: '\x1b[38;5;255m' },
    1024: { bg: '\x1b[48;5;166m', fg: '\x1b[38;5;255m' },
    2048: { bg: '\x1b[48;5;226m', fg: '\x1b[38;5;255m' },
};
const SUPER_COLOR = { bg: '\x1b[48;5;232m', fg: '\x1b[38;5;255m' };
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

class Game2048 {
    constructor() {
        this.size = 4;
        this.grid = [];
        this.score = 0;
        this.best = 0;
        this.won = false;
        this.over = false;
        this.moveCount = 0;
    }

    init() {
        this.grid = Array.from({ length: this.size }, () => Array(this.size).fill(0));
        this.score = 0;
        this.won = false;
        this.over = false;
        this.moveCount = 0;
        this.addRandomTile();
        this.addRandomTile();
    }

    addRandomTile() {
        const empty = [];
        for (let r = 0; r < this.size; r++) {
            for (let c = 0; c < this.size; c++) {
                if (this.grid[r][c] === 0) empty.push({ r, c });
            }
        }
        if (empty.length === 0) return null;
        const cell = empty[Math.floor(Math.random() * empty.length)];
        this.grid[cell.r][cell.c] = Math.random() < 0.9 ? 2 : 4;
        return cell;
    }

    move(direction) {
        if (this.over) return false;

        const oldGrid = this.grid.map(row => [...row]);
        let scoreGain = 0;

        const isRow = direction === 'left' || direction === 'right';
        const isReverse = direction === 'right' || direction === 'down';

        for (let i = 0; i < this.size; i++) {
            // 提取一行/列
            let line = [];
            for (let j = 0; j < this.size; j++) {
                const [r, c] = isRow ? [i, j] : [j, i];
                if (this.grid[r][c] !== 0) line.push(this.grid[r][c]);
            }

            if (isReverse) line.reverse();

            // 合并
            const merged = [];
            let skip = false;
            for (let k = 0; k < line.length; k++) {
                if (skip) { skip = false; continue; }
                if (k + 1 < line.length && line[k] === line[k + 1]) {
                    const newVal = line[k] * 2;
                    merged.push(newVal);
                    scoreGain += newVal;
                    if (newVal === 2048) this.won = true;
                    skip = true;
                } else {
                    merged.push(line[k]);
                }
            }

            // 补零
            while (merged.length < this.size) merged.push(0);
            if (isReverse) merged.reverse();

            // 写回
            for (let j = 0; j < this.size; j++) {
                const [r, c] = isRow ? [i, j] : [j, i];
                this.grid[r][c] = merged[j];
            }
        }

        // 检查是否有移动
        let moved = false;
        for (let r = 0; r < this.size; r++) {
            for (let c = 0; c < this.size; c++) {
                if (this.grid[r][c] !== oldGrid[r][c]) { moved = true; break; }
            }
            if (moved) break;
        }

        if (moved) {
            this.score += scoreGain;
            if (this.score > this.best) this.best = this.score;
            this.moveCount++;
            this.addRandomTile();

            if (this.isGameOver()) {
                this.over = true;
            }
        }

        return moved;
    }

    isGameOver() {
        for (let r = 0; r < this.size; r++) {
            for (let c = 0; c < this.size; c++) {
                if (this.grid[r][c] === 0) return false;
                if (c + 1 < this.size && this.grid[r][c] === this.grid[r][c + 1]) return false;
                if (r + 1 < this.size && this.grid[r][c] === this.grid[r + 1][c]) return false;
            }
        }
        return true;
    }

    getMaxTile() {
        let max = 0;
        for (let r = 0; r < this.size; r++) {
            for (let c = 0; c < this.size; c++) {
                if (this.grid[r][c] > max) max = this.grid[r][c];
            }
        }
        return max;
    }
}

// ============ 渲染器 ============
function getColor(val) {
    return COLORS[val] || SUPER_COLOR;
}

function padCenter(str, len) {
    const pad = Math.max(0, len - str.length);
    const left = Math.floor(pad / 2);
    const right = pad - left;
    return ' '.repeat(left) + str + ' '.repeat(right);
}

function render(game) {
    // 清屏
    process.stdout.write('\x1b[2J\x1b[H');

    const cellWidth = 8;  // 每个格子宽度（字符）
    const borderWidth = game.size * cellWidth + game.size + 1;

    // 标题
    console.log('');
    console.log(`${BOLD}      ╔══════════════════════════╗${RESET}`);
    console.log(`${BOLD}      ║       2 0 4 8           ║${RESET}`);
    console.log(`${BOLD}      ╚══════════════════════════╝${RESET}`);
    console.log('');

    // 分数
    const scoreStr = `  分数: ${BOLD}${game.score}${RESET}    最高: ${BOLD}${game.best}${RESET}    步数: ${game.moveCount}`;
    console.log(scoreStr);
    console.log('');

    // 顶边框
    let line = '  ' + '┌';
    for (let c = 0; c < game.size; c++) {
        line += '─'.repeat(cellWidth);
        if (c < game.size - 1) line += '┬';
    }
    line += '┐';
    console.log(line);

    // 网格
    for (let r = 0; r < game.size; r++) {
        // 数字行
        let numLine = '  ' + '│';
        for (let c = 0; c < game.size; c++) {
            const val = game.grid[r][c];
            const color = getColor(val);
            const text = val === 0 ? '' : String(val);
            const padded = padCenter(text, cellWidth);
            if (val === 0) {
                numLine += `${DIM}${padded}${RESET}│`;
            } else {
                numLine += `${color.bg}${color.fg}${BOLD}${padded}${RESET}│`;
            }
        }
        console.log(numLine);

        // 分隔线
        if (r < game.size - 1) {
            let sepLine = '  ' + '├';
            for (let c = 0; c < game.size; c++) {
                sepLine += '─'.repeat(cellWidth);
                if (c < game.size - 1) sepLine += '┼';
            }
            sepLine += '┤';
            console.log(sepLine);
        }
    }

    // 底边框
    let bottomLine = '  ' + '└';
    for (let c = 0; c < game.size; c++) {
        bottomLine += '─'.repeat(cellWidth);
        if (c < game.size - 1) bottomLine += '┴';
    }
    bottomLine += '┘';
    console.log(bottomLine);
    console.log('');

    // 状态提示
    if (game.over) {
        if (game.won) {
            console.log(`  ${BOLD}\x1b[38;5;226m🎉 恭喜！你达到了 2048！${RESET}`);
        } else {
            console.log(`  ${BOLD}\x1b[38;5;196m💀 游戏结束！最终分数: ${game.score}${RESET}`);
        }
        console.log(`  ${DIM}按 R 重新开始，按 Q 退出${RESET}`);
    } else {
        console.log(`  ${DIM}方向键/WASD: 移动  R: 重开  Q: 退出${RESET}`);
    }
    console.log('');
}

// ============ 主程序 ============
function main() {
    const game = new Game2048();
    game.init();

    // 设置终端
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.isTTY) {
        process.stdin.setRawMode(true);
    }

    render(game);

    process.stdin.on('keypress', (str, key) => {
        // Ctrl+C 退出
        if (key.ctrl && key.name === 'c') {
            process.stdout.write('\x1b[2J\x1b[H');
            console.log(`${BOLD}👋 再见！${RESET}\n`);
            process.exit(0);
        }

        // 退出
        if (key.name === 'q' && !key.ctrl) {
            process.stdout.write('\x1b[2J\x1b[H');
            console.log(`${BOLD}👋 再见！${RESET}\n`);
            process.exit(0);
        }

        // 重新开始
        if (key.name === 'r') {
            game.init();
            render(game);
            return;
        }

        // 方向控制
        const dirMap = {
            'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
            'w': 'up', 's': 'down', 'a': 'left', 'd': 'right',
        };

        const dir = dirMap[key.name];
        if (dir) {
            game.move(dir);
            render(game);
        }
    });

    // 退出时恢复终端
    process.on('exit', () => {
        if (process.stdin.isTTY) {
            process.stdin.setRawMode(false);
        }
        process.stdin.pause();
    });
}

main();