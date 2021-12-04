import { promises } from "fs";
import { EOL } from "os";

type Draws = number[];
type Boards = Board[];

class Column {
  value: number;
  marked: boolean;

  constructor(value: number) {
    this.value = value;
    this.marked = false;
  }
}

class Board {
  #id: number;
  #rows: Column[][];

  constructor(rows: string[], id: number) {
    this.#id = id;
    this.#rows = rows.map(this.#parse_row);
  }

  static createFromStringWithId(board: string, id: number) {
    return new Board(board.split(EOL), id);
  }

  #parse_row(row: string) {
    return row
      .trim()
      .split(/\s+/)
      .map(item => new Column(parseInt(item, 10)));
  }

  updateColumnsBasedOnCurrentDraw(draw: number) {
    this.#rows.forEach(row =>
      row.forEach(column => {
        if (column.value === draw) {
          column.marked = true;
        }
      })
    );
  }

  bingo() {
    const row_match = this.#rows.map(row => row.every(column => column.marked));
    const column_match = this.#rows
      .map((_, index) => this.#rows.map(r => r[index]))
      .some(columns => columns.every(column => column.marked));

    return row_match.includes(true) || column_match === true;
  }

  sumUnmarked() {
    return this.#rows.reduce((accumulator, row) => {
      row.forEach(column => {
        if (column.marked === false) {
          accumulator += column.value;
        }
      });

      return accumulator;
    }, 0);
  }

  get id() {
    return this.#id;
  }
}

function solve_part_one(draws: Draws, boards: Boards) {
  for (const draw of draws) {
    for (const board of boards) {
      board.updateColumnsBasedOnCurrentDraw(draw);
      if (board.bingo()) {
        return board.sumUnmarked() * draw;
      }
    }
  }

  return 0;
}

function solve_part_two(draws: Draws, boards: Boards) {
  const bingos: number[] = [];

  for (const draw of draws) {
    for (const board of boards) {
      board.updateColumnsBasedOnCurrentDraw(draw);

      if (board.bingo() && !bingos.includes(board.id)) {
        bingos.push(board.id);
      }

      if (bingos.length === boards.length) {
        const last_winner_id = bingos[bingos.length - 1];
        const last_winner = boards.find(board => board.id === last_winner_id);

        return (last_winner?.sumUnmarked() ?? 1) * draw;
      }
    }
  }

  return 0;
}

async function main() {
  const file_url = new URL("input.txt", import.meta.url);
  const file_contents = await promises.readFile(file_url, "utf8");
  const [draw_items, ...board_data] = file_contents.split(EOL + EOL);
  const draws = draw_items.split(",").map(draw => parseInt(draw, 10));
  const boards = board_data.map((board, index) =>
    Board.createFromStringWithId(board, index + 1)
  );

  console.log({
    part_one: solve_part_one(draws, boards),
    part_two: solve_part_two(draws, boards)
  });
}

main();
