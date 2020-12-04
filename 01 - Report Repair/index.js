const { promises } = require("fs");
const { join } = require("path");

function first(expenses) {
  const checked = new Set();

  for (const expense of expenses) {
    const target = 2020 - expense;
    if (checked.has(target)) return target * expense;
    checked.add(expense);
  }

  return null;
}

function second(expenses) {
  const targets = new Map();

  for (const outer of expenses) {
    const target = 2020 - outer;
    if (targets.has(target)) return outer * targets.get(target);
    for (const inner of expenses) targets.set(outer + inner, outer * inner);
  }

  return null;
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const expenses = file.split("\n").map(item => parseInt(item, 10));

  console.log({
    part_one: first(expenses),
    part_two: second(expenses)
  });
}

main();