use std::fs::{read_to_string};
use std::collections::HashMap;

#[derive(Debug, PartialEq)]
enum Direction { North, South, East, West }

#[derive(Debug, PartialEq)]
enum Instruction {
  Left,
  Right,
  Forward,
  North(Direction),
  South(Direction),
  East(Direction),
  West(Direction)
}

type Action = (Instruction, i32);
type Actions = Vec<Action>;
type Orientations = HashMap<i32, Direction>;

fn read_lines(filename: &str) -> String {
  return read_to_string(filename).unwrap();
}

fn parse_value(string: String) -> i32 {
  return string.parse::<i32>().unwrap();
}

fn parse_instructions(data: String) -> Actions {
  return data.lines().map(|line| {
    let bytes = line.as_bytes();
    let instruction = parse_instruction(bytes[0] as char);
    let value = parse_value(
      String::from_utf8(
        bytes[1..line.len()].to_vec()
      ).unwrap()
    );
    return (instruction, value);
  }).collect();
}

fn parse_instruction(character: char) -> Instruction {
  return match character {
    'N' => Instruction::North(Direction::North),
    'S' => Instruction::South(Direction::South),
    'E' => Instruction::East(Direction::East),
    'W' => Instruction::West(Direction::West),
    'L' => Instruction::Left,
    'R' => Instruction::Right,
    _ => Instruction::Forward
  }
}

fn rotate(current: i32, value: i32) -> i32 {
  let mut next = (current + value) % 360;
  if next < 0 { next += 360; }
  return next;
}

fn generate_orientations() -> Orientations {
  let mut orientations = HashMap::new();
  orientations.insert(0, Direction::East);
  orientations.insert(90, Direction::South);
  orientations.insert(180, Direction::West);
  orientations.insert(270, Direction::North);
  return orientations;
}

fn solve_part_one(instructions: &Actions) -> i32 {
  let mut angle = 0;
  let (mut x, mut y) = (0, 0);
  let orientations = generate_orientations();

  for (instruction, value) in instructions {
    let orientation = orientations.get(&angle).unwrap();

    match instruction {
      Instruction::Forward => match orientation {
        Direction::North => y += value,
        Direction::South => y -= value,
        Direction::East => x += value,
        Direction::West => x -= value
      },
      Instruction::North(_) => y += value,
      Instruction::South(_) => y -= value,
      Instruction::East(_) => x += value,
      Instruction::West(_) => x -= value,
      Instruction::Left => angle = rotate(angle, -value.clone()),
      Instruction::Right => angle = rotate(angle, value.clone())
    }
  }

  return x.abs() + y.abs();
}

fn solve_part_two(instructions: &Actions) -> i32 {
  let (mut x, mut y) = (0, 0);
  let mut waypoint = vec!(1, 10, 0, 0);

  for (instruction, value) in instructions {
    match instruction {
      Instruction::Forward => {
        x += value * (waypoint[1] - waypoint[3]);
        y += value * (waypoint[0] - waypoint[2]);
      },
      Instruction::North(_) => waypoint[0] += value,
      Instruction::South(_) => waypoint[2] += value,
      Instruction::East(_) => waypoint[1] += value,
      Instruction::West(_) => waypoint[3] += value,
      Instruction::Left => {
        for _ in 0..(value / 90) { waypoint.rotate_left(1); }
      },
      Instruction::Right => {
        for _ in 0..(value / 90) { waypoint.rotate_right(1); }
      }
    }
  }

  return x.abs() + y.abs();
}

fn main() {
  let lines = read_lines("./input.txt");
  let instructions = parse_instructions(lines);
  println!("part_one: {:?}", solve_part_one(&instructions));
  println!("part_two: {:?}", solve_part_two(&instructions));
}