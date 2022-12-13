function solve_part_one(instructions: string[]): number {
  let cycle = 1;
  let sum = 0;
  let x = 1;

  for (const line of instructions) {
    const [op, v] = line.split(" ");
    const cycles = op === "addx" ? 2 : 1;

    for (let i = 0; i < cycles; i++) {
      if ((cycle - 20) % 40 === 0) sum += cycle * x;
      cycle++;
    }

    if (cycles === 2) x += parseInt(v, 10);
  }

  return sum;
}

function solve_part_two(instructions: string[]): string[][] {
  let cycle = 1;
  let x = 1;
  let row = "";
  let image = [];

  for (const line of instructions) {
    const [op, v] = line.split(" ");
    const cycles = op === "addx" ? 2 : 1;

    for (let i = 0; i < cycles; i++) {
      const column = (cycle - 1) % 40;

      if (x - 1 <= column && column <= x + 1) {
        row += "#";
      } else {
        row += " ";
      }

      if (column === 39) {
        image.push(row.split(""));
        row = "";
      }

      cycle++;
    }

    if (cycles === 2) x += parseInt(v, 10);
  }

  return image;
}

function outputResults(part_one: number, part_two: string[][]): void {
  const app = document.getElementById("app")!;
  const pre = document.createElement("pre");

  pre.textContent = JSON.stringify(
    { part_one, part_two },
    (_, value) => {
      if (value instanceof Array) {
        return value.reduce((accumulator: any[], current: any[]) => {
          accumulator.push(current.join(""));

          return accumulator;
        }, []);
      }

      return value;
    },
    2
  );

  app.appendChild(pre);
}

async function main() {
  const response = await fetch("/input.txt");
  const content = await response.text();
  const instructions = content
    .split("\n")
    .map(line => line.trim())
    .filter(line => line !== "");
  const part_one = solve_part_one(instructions);
  const part_two = solve_part_two(instructions);

  outputResults(part_one, part_two);
}

main();

export {};
