const { promises } = require("fs");
const { join } = require("path");

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const expenses = file.split("\n").map(item => parseInt(item, 10));
  const first_part = new Array(2);
  const second_part = new Array(3);

  for (const outer of expenses) {
    for (const middle of expenses) {
      for (const inner of expenses) {
        if (middle + inner === 2020) {
          first_part[0] = middle;
          first_part[1] = inner;
        }

        if (outer + middle + inner === 2020) {
          second_part[0] = outer;
          second_part[1] = middle;
          second_part[2] = inner;
        }
      }
    }
  }

  console.log({
    first_part,
    first_result: first_part.reduce((a, c) => a * c, 1),
    second_part,
    second_result: second_part.reduce((a, c) => a * c, 1),
  });
}

main();