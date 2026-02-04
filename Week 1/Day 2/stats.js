#!/usr/bin/env node
const fs = require("fs/promises");
const path = require("path");
const { performance } = require("perf_hooks");

const args = process.argv.slice(2);

// parse args
const tasks = [];
let unique = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];

  if (arg === "--unique") {
    unique = true;
    continue;
  }

  if (["--lines", "--words", "--chars"].includes(arg)) {
    const file = args[i + 1];
    if (!file) throw new Error(`File not found for ${arg}`);
    tasks.push({ flag: arg.slice(2), file });
    i++;
  }
}

// helpers
const countLines = (text) => text.split("\n").length;
const countWords = (text) =>
  text.trim().split(/\s+/).filter(Boolean).length;
const countChars = (text) => text.length;

async function removeDuplicateLines(file, text) {
  const uniqueLines = [...new Set(text.split("\n"))].join("\n");
  await fs.mkdir("output", { recursive: true });
  const outPath = path.join("output", `unique-${path.basename(file)}`);
  await fs.writeFile(outPath, uniqueLines);
  return outPath;
}

// worker
async function processFile({ flag, file }) {
  const start = performance.now();
  const startMem = process.memoryUsage().heapUsed;

  const text = await fs.readFile(file, "utf8");

  let result;
  if (flag === "lines") result = countLines(text);
  if (flag === "words") result = countWords(text);
  if (flag === "chars") result = countChars(text);

  let outputFile;
  if (unique) {
    outputFile = await removeDuplicateLines(file, text);
  }

  const end = performance.now();
  const endMem = process.memoryUsage().heapUsed;

  const perfStats = {
    flag,
    result,
    executionTimeMs: Math.round(end - start),
    memoryMB: ((endMem - startMem) / 1024 / 1024).toFixed(1),
  };

  await fs.mkdir("logs", { recursive: true });
  const perfFile = `./logs/${path.basename(file)}-${flag}.json`;
  await fs.writeFile(perfFile, JSON.stringify(perfStats, null, 2));

  return {
    file,
    flag,
    result,
    executionTimeMs: perfStats.executionTimeMs,
    memoryMB: perfStats.memoryMB,
    outputFile,
  };
}

// run max 3 in parallel
(async () => {
  const queue = [...tasks];
  const running = [];

  async function runNext() {
    if (!queue.length) return;

    const task = queue.shift();
    const p = processFile(task)
      .then((res) => {
        console.log(`\n${res.file}`);
        console.log(`${res.flag}: ${res.result}`);
        console.log(
          JSON.stringify(
            {
              executionTimeMs: res.executionTimeMs,
              memoryMB: Number(res.memoryMB),
            },
            null,
            2
          )
        );

        if (res.outputFile) {
          console.log(`unique -> ${res.outputFile}`);
        }
      })
      .finally(() => {
        running.splice(running.indexOf(p), 1);
      });

    running.push(p);

    if (running.length < 3) {
      await runNext();
    }
  }

  await Promise.all(
    Array.from({ length: Math.min(3, queue.length) }, runNext)
  );
})();
