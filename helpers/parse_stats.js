// Paste script into the console at: https://adventofcode.com/<year>/statistics.
// This will scrape the statistics for the given <year> and parse them into helpful objects which break down the data for you to do with as you wish.

/**
 * Parse out the values from the elements
 *
 * @param {HTMLElement[]} statistics
 */
const parse = statistics => {
  return Array.from(statistics)
    .map(span => span.textContent.trim())
    .map(row => row.replace(/\D/g, ""))
    .map(value => parseInt(value, 10))
    .filter(Boolean);
};

/**
 * Chunk an array
 *
 * @param {any[]} array
 * @param {number} size
 */
const chunk = (array, size) => {
  return array.reduce((accumulator, item, index) => {
    const position = Math.floor(index / size);
    if (!accumulator[position]) accumulator[position] = [];
    accumulator[position].push(item);
    return accumulator;
  }, []);
};

/**
 * Parse and display the statistics for the given year
 *
 * @param {number[]} points
 * @param {function} chunkFn
 * @param {function|undefined} displayFn
 * @returns {object[]} The overall statistics for that year
 */
const main = (points, chunkFn, displayFn) => {
  const statistics = chunkFn(points, 2)
    .reverse()
    .map(([part_two, part_one], index) => ({
      day: index + 1,
      part_one: part_one,
      part_two: part_two - part_one,
      combined: part_two
    }));

  if (typeof displayFn !== "undefined") {
    statistics.forEach((statistic, index) => displayFn({ ...statistic }));
  }

  return statistics;
};

const statistics = document.querySelectorAll(".stats-firstonly, .stats-both");
const points = parse(statistics);
main(points, chunk, console.table);
