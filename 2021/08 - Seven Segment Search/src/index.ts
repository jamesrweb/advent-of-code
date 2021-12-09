import { promises } from "fs";
import { EOL } from "os";

class Display {
  constructor(public patterns: string[], public outputs: string[]) {}
}

function uniqueCharacterMatch(a: string = "", b: string = "") {
  const set = new Set([...a]);
  return [...b].every(x => set.has(x));
}

function formatDisplayPart(part: string) {
  return part.split(" ").map(code => code.split("").sort().join(""));
}

function solve_part_one(displays: Display[]) {
  return displays
    .map(display => display.outputs)
    .map(outputs =>
      outputs.filter(output => [2, 4, 3, 7].includes(output.length))
    )
    .map(outputs => outputs.length)
    .reduce((accumulator, current) => accumulator + current, 0);
}

function solve_part_two(displays: Display[]) {
  return displays.reduce((accumulator, display) => {
    const matches: { [key in number]?: string } = {
      1: display.patterns.find(x => x.length === 2),
      4: display.patterns.find(x => x.length === 4),
      7: display.patterns.find(x => x.length === 3),
      8: display.patterns.find(x => x.length === 7)
    };

    matches[6] = display.patterns.find(
      x => x.length === 6 && !uniqueCharacterMatch(x, matches[1])
    );
    matches[9] = display.patterns.find(
      x =>
        x.length === 6 &&
        x !== matches[6] &&
        uniqueCharacterMatch(x, matches[4])
    );
    matches[0] = display.patterns.find(
      x => x.length === 6 && x !== matches[6] && x !== matches[9]
    );

    matches[3] = display.patterns.find(
      x => x.length === 5 && uniqueCharacterMatch(x, matches[1])
    );
    matches[5] = display.patterns.find(
      x =>
        x.length === 5 &&
        x !== matches[3] &&
        uniqueCharacterMatch(matches[6], x)
    );
    matches[2] = display.patterns.find(
      x => x.length === 5 && x !== matches[3] && x !== matches[5]
    );

    const translationTable = Object.fromEntries(
      Object.entries(matches).map(x => x.reverse())
    );

    const translated = Number(
      display.outputs.map(signal => translationTable[signal]).join("")
    );

    return (accumulator += translated);
  }, 0);
}

async function main() {
  const file_url = new URL("input.txt", import.meta.url);
  const file_contents = await promises.readFile(file_url, "utf8");
  const lines = file_contents.split(EOL);
  const displays = lines
    .map(line => line.split(" | "))
    .map(
      ([patterns, outputs]) =>
        new Display(formatDisplayPart(patterns), formatDisplayPart(outputs))
    );

  console.log({
    part_one: solve_part_one(displays),
    part_two: solve_part_two(displays)
  });
}

main();
