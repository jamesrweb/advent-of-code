import { promises } from "fs";
import { EOL } from "os";

type MatchValue = string | undefined;
type Matches = Map<number, MatchValue>;
type DisplayPatternValue = Display["patterns"][number];

class Display {
  constructor(
    public patterns: string[],
    public outputs: string[]
  ) {}
}

function uniqueCharacterMatch(haystack: string = "", needles: string = "") {
  const stack = new Set([...haystack]);
  return [...needles].every(needle => stack.has(needle));
}

function formatDisplayPart(part: string) {
  return part.split(" ").map(code => code.split("").sort().join(""));
}

function reverseArray<T>(array: T[]) {
  return array.reverse();
}

function initialiseMatchesFromPatterns(patterns: Display["patterns"]) {
  const matches: Matches = new Map();

  const ones = patterns.find(pattern => pattern.length === 2);
  const fours = patterns.find(pattern => pattern.length === 4);
  const sevens = patterns.find(pattern => pattern.length === 3);
  const eights = patterns.find(pattern => pattern.length === 7);

  matches.set(1, ones);
  matches.set(2, undefined);
  matches.set(3, undefined);
  matches.set(4, fours);
  matches.set(5, undefined);
  matches.set(6, undefined);
  matches.set(7, sevens);
  matches.set(8, eights);

  return matches;
}

function findSixes(matches: Matches) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 6;
    const noOnesCrossover = !uniqueCharacterMatch(pattern, matches.get(1));

    return lengthMatch && noOnesCrossover;
  };
}

function findNines(matches: Matches, sixes: MatchValue) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 6;
    const notTheSixesMatch = pattern !== sixes;
    const foursCrossover = uniqueCharacterMatch(pattern, matches.get(4));

    return lengthMatch && notTheSixesMatch && foursCrossover;
  };
}

function findZeros(sixes: MatchValue, nines: MatchValue) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 6;
    const notTheSixesMatch = pattern !== sixes;
    const notTheNinesMatch = pattern !== nines;

    return lengthMatch && notTheSixesMatch && notTheNinesMatch;
  };
}

function findThrees(matches: Matches) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 5;
    const onesCrossover = uniqueCharacterMatch(pattern, matches.get(1));

    return lengthMatch && onesCrossover;
  };
}

function findFives(threes: MatchValue, sixes: MatchValue) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 5;
    const notTheThreesMatch = pattern !== threes;
    const sixesCrossover = uniqueCharacterMatch(sixes, pattern);

    return lengthMatch && notTheThreesMatch && sixesCrossover;
  };
}

function findTwos(threes: MatchValue, fives: MatchValue) {
  return (pattern: DisplayPatternValue) => {
    const lengthMatch = pattern.length === 5;
    const notTheThreesMatch = pattern !== threes;
    const notTheFivesMatch = pattern !== fives;

    return lengthMatch && notTheThreesMatch && notTheFivesMatch;
  };
}

function solvePartOne(displays: Display[]) {
  return displays
    .map(display => display.outputs)
    .map(outputs =>
      outputs.filter(output => [2, 4, 3, 7].includes(output.length))
    )
    .map(outputs => outputs.length)
    .reduce((accumulator, current) => accumulator + current, 0);
}

function solvePartTwo(displays: Display[]) {
  return displays.reduce((accumulator, display) => {
    const matches = initialiseMatchesFromPatterns(display.patterns);
    const sixes = display.patterns.find(findSixes(matches));
    const nines = display.patterns.find(findNines(matches, sixes));
    const zeros = display.patterns.find(findZeros(sixes, nines));
    const threes = display.patterns.find(findThrees(matches));
    const fives = display.patterns.find(findFives(threes, sixes));
    const twos = display.patterns.find(findTwos(threes, fives));

    matches.set(0, zeros);
    matches.set(2, twos);
    matches.set(3, threes);
    matches.set(5, fives);
    matches.set(6, sixes);
    matches.set(9, nines);

    const flippedMatches = Array.from(matches.entries()).map(reverseArray);
    const translationTable = Object.fromEntries(flippedMatches);
    const translatedOutputValues = display.outputs.map<string>(
      signal => translationTable[signal]
    );

    return accumulator + parseInt(translatedOutputValues.join(""), 10);
  }, 0);
}

async function main() {
  const file_url = new URL("input.txt", import.meta.url);
  const file_contents = await promises.readFile(file_url, "utf8");
  const lines = file_contents.split(EOL);
  const displays = lines
    .map(line => line.split(" | "))
    .map(([patterns, outputs]) => {
      const formattedPatterns = formatDisplayPart(patterns);
      const formattedOutputs = formatDisplayPart(outputs);

      return new Display(formattedPatterns, formattedOutputs);
    });

  console.log({
    part_one: solvePartOne(displays),
    part_two: solvePartTwo(displays)
  });
}

main();
