const { promises } = require("fs");
const { join } = require("path");
const { EOL } = require("os");

type Item = { ingredients: Array<string>, allergens: Array<string> };
type Items = Array<Item>;
type Allergens = Map<string, Array<string>>;

function ParseData(file: string): Items {
  return file.split(EOL)
    .map((val) => val.match(/^([a-z\ ]+) \(contains ([a-z,\ ]+)\)$/))
    .reduce((accumulator, current) => {
      if (current === null) return accumulator;
      return [...accumulator, { ingredients: current[1].split(" "), allergens: current[2].split(", ") }];
    }, [] as Items);
}

function AllergenMapFactory(data: Items): Allergens {
  return data.reduce((accumulator, { allergens, ingredients }) => {
    allergens.forEach(allergen => {
      if (!accumulator.has(allergen)) {
        accumulator.set(allergen, [...ingredients]);
      } else {
        const current = accumulator.get(allergen) || [];
        const next = current.filter(allergen => ingredients.includes(allergen));
        accumulator.set(allergen, next);
      }
    });

    return accumulator;
  }, new Map() as Allergens);
}

function solve_part_one(data: Items): number {
  const values = AllergenMapFactory(data).values();
  const allergens = [...values].reduce((accumulator, current) => {
    current.forEach(allergen => accumulator.add(allergen));
    return accumulator;
  }, new Set<string>());

  return data.reduce((accumulator, { ingredients }) => {
    accumulator += ingredients.length;
    allergens.forEach(allergen => ingredients.includes(allergen) && accumulator--);
    return accumulator;
  }, 0);
}

function solve_part_two(data: Items): string {
  const allergens = AllergenMapFactory(data);
  const keys = [...allergens.keys()];

  while (true) {
    keys.forEach(first => {
      let possibilities = allergens.get(first) || [];

      keys.forEach(second => first !== second && (
        possibilities = possibilities.filter(value => (
          !(allergens.get(second) || []).includes(value)
        ))
      ));

      if (possibilities.length >= 1) allergens.set(first, possibilities);
    });

    if (![...allergens.values()].some(({ length }) => length > 1)) break;
  }

  return keys.sort().reduce((accumulator, current) => {
    return [...accumulator, (allergens.get(current) || [])[0]];
  }, [] as string[]).join(",");
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = await promises.readFile(uri, "utf8") as string;
  const data = ParseData(file);

  console.log({
    part_one: solve_part_one(data),
    part_two: solve_part_two(data)
  })
}

main();