const { promises } = require("fs");
const { join } = require("path");

function filter(policies, predicate) {
  return policies.filter(predicate);
}

function format(item) {
  const [policy, password] = item.split(": ");
  const [counts, char] = policy.split(" ");
  return {
    char,
    password,
    count: counts.split("-").map(item => parseInt(item, 10))
  }
}

function solve_part_one(policies) {
  return filter(policies, ({ char, count, password }) => {
    const [min, max] = count;
    const appearances = [...password].reduce((accumulator, letter) => {
      return letter === char ? accumulator + 1 : accumulator;
    }, 0);

    return appearances >= min && appearances <= max;
  });
}

function solve_part_two(policies) {
  return filter(policies, ({ char, count: positions, password }) => {
    const [first, second] = positions;

    return (
      password[first - 1] === char && password[second - 1] !== char ||
      password[second - 1] === char && password[first - 1] !== char
    );
  });
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const policies = file.split("\r\n").map(format);

  console.log({
    part_one: solve_part_one(policies).length,
    part_two: solve_part_two(policies).length
  });
}

main();