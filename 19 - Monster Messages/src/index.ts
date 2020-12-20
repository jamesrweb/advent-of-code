const { promises } = require("fs");
const { join } = require("path");

type Lines = Array<string>;
type Rules = Map<number, string>;

function build_rules(rules: Rules, token: number | string, depth: number, special_rules: boolean): string {
  if (Object.is(parseInt(`${token}`, 10), NaN)) {
    return (token === "a" || token === "b") ? token : "";
  }

  if (special_rules === true) {
    if (+token === 8) {
      return `(?:${build_rules(rules, 42, depth, special_rules)})+`;
    }

    if (+token === 11) {
      const ft = build_rules(rules, 42, depth, special_rules);
      const to = build_rules(rules, 31, depth, special_rules);

      if (depth < 5) {
        return `(?:${ft}${build_rules(rules, 11, depth + 1, special_rules)}?${to})`;
      }

      return `(?:${ft}${to})`;
    }
  }

  let regex = "";
  const rule = rules.get(+token);

  if (!rule) return regex;

  for (const part of rule.split("|")) {
    regex += "|";
    for (const item of part.split(" ")) {
      regex += build_rules(rules, item.trim(), depth, special_rules)
    }
  }

  return "(?:" + regex.slice(1) + ")";
}

function solve_part_one(rules: Rules, messages: Lines): number {
  const regex = new RegExp(`^${build_rules(rules, 0, 0, false)}$`);

  return messages.reduce((accumulator, current) => {
    return regex.test(current) ? accumulator + 1 : accumulator;
  }, 0);
}

function solve_part_two(rules: Rules, messages: Lines): number {
  const regex = new RegExp(`^${build_rules(rules, 0, 0, true)}$`);

  return messages.reduce((accumulator, current) => {
    return regex.test(current) ? accumulator + 1 : accumulator;
  }, 0);
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8") as string;
  const [rh, mh] = file.split("\r\n\r\n");
  const messages = mh.split("\r\n");
  const rules = rh.split("\r\n").reduce((accumulator, current) => {
    const [id, rule] = current.split(": ");
    accumulator.set(+id, rule.replace(/\"/g, ""));
    return accumulator;
  }, new Map() as Rules);

  console.log({
    part_one: solve_part_one(rules, messages),
    part_two: solve_part_two(rules, messages)
  })
}

main();