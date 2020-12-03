const { promises } = require("fs");
const { join } = require("path");

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const policies = file.split("\n").map(item => {
    const [policy, password] = item.split(": ");
    const [counts, char] = policy.split(" ");
    return {
      char,
      password: password.replace("\r", ""),
      count: counts.split("-").map(item => parseInt(item, 10))
    }
  });

  const part_one = policies.filter(({ char, count, password }) => {
    let appearances = 0;
    const [min, max] = count;

    for (const letter of password) {
      if (letter === char) appearances++;
    }

    return appearances >= min && appearances <= max;
  });

  console.log(part_one.length);

  const part_two = policies.filter(({ char, count: positions, password }) => {
    const [first, second] = positions;
    return (
      password[first - 1] === char && password[second - 1] !== char ||
      password[second - 1] === char && password[first - 1] !== char
    );
  });

  console.log(part_two.length);
}

main();