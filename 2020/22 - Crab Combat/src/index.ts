const { promises } = require("fs");
const { join } = require("path");
const { EOL } = require("os");

enum Players {
  One,
  Two
}

type Player = Array<number>;

function clone(array: Array<any>): Array<any> {
  return JSON.parse(JSON.stringify(array));
}

function cards(player: string): Player {
  return player
    .split(EOL)
    .slice(1)
    .map(v => +v);
}

function score(player: Player): number {
  return player.reduce((accumulator, current, index, { length }) => {
    const result = current * (length - index);
    return accumulator + result;
  }, 0);
}

function solve_part_one(players: Player[]): number {
  const [player_one, player_two] = players;

  do {
    const first = player_one.shift() || 0;
    const second = player_two.shift() || 0;
    if (first > second) player_one.push(first, second);
    else player_two.push(second, first);
  } while (player_one.length && player_two.length);

  if (player_one.length) return score(player_one);
  return score(player_two);
}

function part_two_helper(players: Player[]): [Players, Player] {
  const [player_one, player_two] = players;
  const seen = {
    player_one: new Set<string>(),
    player_two: new Set<string>()
  };

  while (player_one.length && player_two.length) {
    const first = player_one.join(",");
    const second = player_two.join(",");

    if (seen.player_one.has(first) || seen.player_two.has(second)) {
      return [Players.One, player_one];
    }

    seen.player_one.add(first);
    seen.player_two.add(second);

    let winner = Players.One;
    const [a, b] = [player_one.shift() || 0, player_two.shift() || 0];

    if (a <= player_one.length && b <= player_two.length) {
      [winner] = part_two_helper([
        player_one.slice(0, a),
        player_two.slice(0, b)
      ]);
    } else if (a > b) {
      winner = Players.One;
    } else {
      winner = Players.Two;
    }

    if (winner === Players.One) player_one.push(a, b);
    else player_two.push(b, a);
  }

  if (player_one.length > 0) return [Players.One, player_one];

  return [Players.Two, player_two];
}

function solve_part_two(players: Player[]): number {
  const [winner, cards] = part_two_helper(players);
  return score(cards);
}

async function main() {
  const uri = join(__dirname, "input.txt");
  const file = (await promises.readFile(uri, "utf8")) as string;
  const decks = file.split(EOL + EOL);
  const players = [cards(decks[0]), cards(decks[1])];

  console.log({
    part_one: solve_part_one(clone(players)),
    part_two: solve_part_two(clone(players))
  });
}

main();
