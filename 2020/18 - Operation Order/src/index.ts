const { promises } = require("fs");
const { join } = require("path");
const { evaluate } = require("mathjs");

type Expressions = Array<string>;

function part_one_helper(expression: string, index: number): [number, number] {
  let result = 0;
  let operation = "+";

  while (index < expression.length) {
    let char = expression[index];

    if (["+", "*"].includes(char)) {
      operation = char;
    } else {
      let value = 0;

      if (/[0-9]/.test(char)) {
        value = parseInt(char);
      } else if (char == "(") {
        [value, index] = part_one_helper(expression, index + 1);
      } else if (char == ")") {
        return [result, index];
      }

      result = evaluate(result + operation + value);
    }

    index += 1;
  }

  return [result, index];
}
function solve_part_one(expressions: Expressions): number {
  return expressions
    .map(expression => {
      const [result, index] = part_one_helper(expression.replace(/\s/g, ''), 0);
      return result;
    })
    .reduce((accumulator, current) => accumulator + current, 0);
}

function solve_part_two(expressions: Expressions): number {
  return expressions
    .map(expression => {
      const tokens = expression.split(" ");
      tokens.forEach((token, index) => {
        if (token === "+") {
          tokens[index - 1] = '(' + tokens[index - 1];
          tokens[index + 1] = tokens[index + 1] + ")";
        }
      });
      return tokens.join(" ");
    })
    .map(expression => evaluate(expression))
    .reduce((accumulator, current) => accumulator + current, 0);
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8");
  const expressions = file.split("\r\n");

  console.log({
    part_one: solve_part_one(expressions),
    part_two: solve_part_two(expressions)
  });
}

main();