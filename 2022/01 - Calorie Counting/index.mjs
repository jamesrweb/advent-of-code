import { promises } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const directory = dirname(import.meta.url);
const __dirname = fileURLToPath(directory);

/**
 * Sum the values of a given array.
 *
 * @param {number[]} array
 * @returns {number} The sum of the numbers in the given array.
 */
function sum(array) {
  return array.reduce((augend, addend) => augend + addend, 0);
}

/**
 * Driver code for the solution to part one.
 *
 * @param {number[][]} caloriesByElf
 * @returns {number} The sum of the calories held by the elf in possession of the most calories.
 */
function solve_part_one(caloriesByElf) {
  const caloriesSumByElf = caloriesByElf.flatMap(sum);

  return Math.max(...caloriesSumByElf);
}

/**
 * Driver code for the solution to part two.
 *
 * @param {number[][]} caloriesByElf
 * @returns {number} The sum of the calories held by the top three elves by calorie count.
 */
function solve_part_two(caloriesByElf) {
  const caloriesSumByElf = caloriesByElf.flatMap(sum);
  const topThreeElvesByCalories = caloriesSumByElf
    .slice()
    .sort((a, b) => b - a)
    .slice(0, 3);

  return sum(topThreeElvesByCalories);
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const caloriesByElf = file
    .split("\n\n")
    .map(line => line.split("\n").map(item => parseInt(item, 10)));

  console.log({
    part_one: solve_part_one(caloriesByElf),
    part_two: solve_part_two(caloriesByElf)
  });
}

main();
