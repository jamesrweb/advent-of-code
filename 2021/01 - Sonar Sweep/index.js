const { promises } = require("fs");
const { join } = require("path");

/**
 * Create a windowed view of a given array where each window is of a given size when output.
 *
 * @template T
 * @param {Array<T>} array
 * @param {number} size
 * @returns {Array<[T]>}
 */
function windowed(array, size) {
  const result = [];

  if (array.length < size || size <= 0) {
    return result;
  }

  for (let index = 0; index < array.length - size + 1; index++) {
    result.push(array.slice(index, size + index));
  }

  return result;
}

/**
 * Sum the values of a given array.
 *
 * @param {Array<number>} array
 * @returns {number} The sum of the numbers in the given array.
 */
function sum(array) {
  return array.reduce((augend, addend) => augend + addend, 0);
}

/**
 * Counts if the current measurement increased from the last.
 *
 * @param {number} accumulator
 * @param {Array<number>} current
 * @returns {number} The count of occurrences where there was an increase in depth from the last reading to the current one.
 */
function depthMeasurementIncreaseCounter(accumulator, current) {
  const [lastMeasurement, currentMeasurement] = current;

  if (currentMeasurement > lastMeasurement) {
    return accumulator + 1;
  }

  return accumulator;
}

/**
 * Counts occassions where the sum of a group of readings increases when compared to the previous grouping.
 *
 * @param {number} accumulator
 * @param {Array<[Array<number>, Array<number>]>} current
 * @returns {number} The count of occurrences where there was an increase in the sum of each grouping of depths from the last set to the current set.
 */
function depthGroupingSumIncreaseCounter(accumulator, current) {
  const [lastSetOfReadings, currentSetOfReadings] = current;
  const lastSum = sum(lastSetOfReadings);
  const currentSum = sum(currentSetOfReadings);

  return currentSum > lastSum ? accumulator + 1 : accumulator;
}

/**
 * Driver code for the solution to part one.
 *
 * @param {Array<number>} measurements
 * @returns {number} The count of measurements which were greater than the one before it.
 */
function solve_part_one(measurements) {
  return windowed(measurements, 2).reduce(depthMeasurementIncreaseCounter, 0);
}

/**
 * Driver code for the solution to part two.
 *
 * @param {Array<number>} measurements
 * @returns {number} The count of measurements of group size 3 whose sum is greater than the sum of the one before it.
 */
function solve_part_two(measurements) {
  const threeMeasurementWindows = windowed(measurements, 3);
  const measurementPairings = windowed(threeMeasurementWindows, 2);

  return measurementPairings.reduce(depthGroupingSumIncreaseCounter, 0);
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const measurements = file.split("\n").map(item => parseInt(item, 10));

  console.log({
    part_one: solve_part_one(measurements),
    part_two: solve_part_two(measurements)
  });
}

main();
