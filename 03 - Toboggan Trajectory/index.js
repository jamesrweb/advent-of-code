const { promises } = require("fs");
const { join } = require("path");

function hits(grid, right, down) {
  let count = 0;
  let x = down;
  let y = right;

  do {
    grid[x][y % grid[x].length] && count++;
    x += down;
    y += right;
  } while (x < grid.length);

  return count;
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const gradients = file.split("\r\n");
  const grid = gradients.map(g => [...g].map(char => char === "#"));
  const go = hits.bind(this, grid);

  console.log({
    part_one: go(3, 1),
    part_two: go(1, 1) * go(3, 1) * go(5, 1) * go(7, 1) * go(1, 2)
  });
}

main();