import fs from "fs";

/**
 * The result of the recursion per line of the input to find the relevant digits.
 *
 * @typedef {{ count: number, head?: number, tail?: number }} Result
 */

/**
 * Collect the digits representable within the given line.
 *
 * @param {string} line
 * @param {Map<string, number>} digitMappings
 * @param {boolean} isPartOne
 *
 * @returns {Result}
 */
function collectDigits(line, digitMappings, isPartOne) {
  return collectDigitsHelper(line, digitMappings, isPartOne, []);
}

/**
 * Collect the digits representable within the given line.
 *
 * @param {string} line
 * @param {Map<string, number>} digitMappings
 * @param {boolean} isPartOne
 * @param {Array<number>} digits
 *
 * @returns {Result}
 */
function collectDigitsHelper(line, digitMappings, isPartOne, digits) {
  if (line === "") {
    return {
      head: digits[0],
      tail: digits[digits.length - 1]
    };
  }

  const current = parseInt(line[0], 10);
  const textDigitKey = Array.from(digitMappings.keys()).find(key =>
    line.startsWith(key)
  );

  if (!isNaN(current)) {
    digits.push(current);
  }

  if (textDigitKey !== undefined && !isPartOne) {
    digits.push(digitMappings.get(textDigitKey));
  }

  return collectDigitsHelper(line.slice(1), digitMappings, isPartOne, digits);
}

function main() {
  const data = fs.readFileSync("input.txt", { encoding: "utf8", flag: "r" });
  const lines = data.trim().split(/\r?\n/);
  const digitMapping = new Map()
    .set("one", 1)
    .set("two", 2)
    .set("three", 3)
    .set("four", 4)
    .set("five", 5)
    .set("six", 6)
    .set("seven", 7)
    .set("eight", 8)
    .set("nine", 9);

  const [partOne, partTwo] = Array.from({ length: 2 }).map((_, i) => {
    return lines.reduce((accumulator, line) => {
      const { head, tail } = collectDigits(line, digitMapping, i === 0);

      if (head === undefined && tail === undefined) {
        return accumulator;
      }

      if (head !== undefined && tail === undefined) {
        return accumulator + parseInt(`${head}${head}`, 10);
      }

      if (head !== undefined && tail !== undefined) {
        return accumulator + parseInt(`${head}${tail}`, 10);
      }

      throw new Error("This should never trigger...");
    }, 0);
  });

  console.log({
    part_one: partOne,
    part_two: partTwo
  });
}

main();
