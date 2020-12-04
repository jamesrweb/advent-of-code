const { promises } = require("fs");
const { join } = require("path");

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const expenses = file.split("\n").map(item => parseInt(item, 10));
  const part_one = new Array(2);
  const part_two = new Array(3);

  for (const outer of expenses) {
    for (const middle of expenses) {
      for (const inner of expenses) {
        if (middle + inner === 2020) {
          part_one[0] = middle;
          part_one[1] = inner;
        }

        if (outer + middle + inner === 2020) {
          part_two[0] = outer;
          part_two[1] = middle;
          part_two[2] = inner;
        }
      }
    }
  }

  console.log({
    part_one: part_one.reduce((a, c) => a * c, 1),
    part_two: part_two.reduce((a, c) => a * c, 1)
  });
}

main();