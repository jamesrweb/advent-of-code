const { promises } = require("fs");
const { join } = require("path");
const { EOL } = require("os");

type Cups = Array<number>;

function extract_cups(file: string): Cups {
  return file.split("").map(v => +v);
}

function find_destination_cup(cups: Cups, removed: Cups, current: number): number {
  let guess = current - 1;

  while (removed.includes(guess) || !cups.includes(guess)) {
    guess--;
    const smallest = Math.min(...cups);
    if (guess < smallest) guess = Math.max(...cups);
  }

  return guess;
}

function find_next_current(cups: Cups, current: number): number {
  const next_index = cups.indexOf(current) + 1;
  if (next_index >= cups.length) return cups[0];
  return cups[next_index];
}

function split(cups: Cups, element: number, keep_element: boolean): Array<Cups> {
  const index = cups.indexOf(element);
  return [
    cups.slice(0, keep_element ? index + 1 : index),
    cups.slice(index + 1)
  ];
}

function remove(cups: Cups, current: number, count: number): Cups {
  const start = cups.indexOf(current) + 1;

  if (start + (count - 1) >= cups.length) {
    const diff = (start + (count - 1)) - cups.length;
    return [...cups.splice(start), ...cups.splice(0, diff + 1)];
  }

  return cups.splice(start, count);
}

function move(cups: Cups, current: number): [Cups, number] {
  const removed = remove(cups, current, 3);
  const destination = find_destination_cup(cups, removed, current);
  const [left, right] = split(cups, destination, true);
  const next_cups = [...left, ...removed, ...right];
  const next_current = find_next_current(cups, current);
  return [next_cups, next_current];
}

function solve_part_one(cups: Cups): number {
  let current = cups[0];

  for (let round = 0; round < 100; round++) {
    [cups, current] = move(cups, current);
  }

  const [left, right] = split(cups, 1, false);
  return parseInt([...right, ...left].join(""), 10);
}

function solve_part_two(cups: Cups): number {
  return 1;
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8") as string;

  console.log({
    part_one: solve_part_one(extract_cups(file)),
    part_two: solve_part_two(extract_cups(file))
  })
}

main();