use std::fs::{read_to_string};
use std::collections::{HashMap, HashSet};

type Coordinate = (i8, i8);
type Tiles = HashSet<Coordinate>;

const DIRECTIONS: [&str; 6] = ["ne", "nw", "se", "sw", "e", "w"];
const MOVEMENTS: [Coordinate; 6] = [(0, 1), (-1, 1), (1, -1), (0, -1), (1, 0), (-1, 0)];

fn read_file(path: &str) -> String {
  read_to_string(path).expect("File not found")
}

fn read_lines(path: &str) -> Vec<String> {
  read_file(path)
    .split("\r\n")
    .map(|line| line.to_string())
    .collect()
}

fn solve_part_one(lines: Vec<String>) -> Tiles {
  return lines.iter().fold(HashSet::new(), |mut accumulator, line| {
    let mut position = (0, 0);
    let mut instructions = line.as_str();

    while instructions.is_empty() == false {
      for (index, direction) in DIRECTIONS.iter().enumerate() {
        if instructions.starts_with(direction) {
          let movement = MOVEMENTS[index];
          position = (position.0 + movement.0, position.1 + movement.1);
          instructions = &instructions[direction.len()..];
          break;
        }
      }
    }

    if accumulator.contains(&position) { accumulator.remove(&position); }
    else { accumulator.insert(position); }

    return accumulator;
  });
}

fn solve_part_two(black_tiles: Tiles) -> i32 {
  return (0..100).fold(black_tiles, |accumulator, _| {
    let mut unflipped = HashSet::new();
    let mut white_tiles = HashMap::new();

    for black_tile in &accumulator {
      let mut neighbours = 0;

      for movement in &MOVEMENTS {
        let neighbour = (black_tile.0 + movement.0, black_tile.1 + movement.1);

        if accumulator.contains(&neighbour) { neighbours += 1; }
        else { *white_tiles.entry(neighbour).or_insert(0) += 1; }
      }

      if (1..3).contains(&neighbours) { unflipped.insert(*black_tile); }
    }

    let flipped = white_tiles
      .into_iter()
      .filter(|(_, neighbours)| *neighbours == 2)
      .map(|(position, _)| position)
      .collect::<Tiles>();

    return unflipped.union(&flipped).cloned().collect::<Tiles>();
  }).len() as i32;
}

fn main() {
  let lines = read_lines("./input.txt");
  let black_tiles = solve_part_one(lines);
  println!("part_one: {}", black_tiles.len());
  println!("part_two: {}", solve_part_two(black_tiles));
}