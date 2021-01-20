use std::fs::File;
use std::ops::{Add};
use std::io::{BufRead, BufReader, Error, ErrorKind, Read};

fn read_lines<R: Read>(io: R) -> Result<Vec<i32>, Error> {
    let reader = BufReader::new(io);
    let lines = reader.lines();
    let parsed = lines.map(|line| {
      let value = line.unwrap();
      value.parse().map_err(|error| {
        Error::new(ErrorKind::InvalidData, error)
      })
    });

    parsed.collect()
}

fn distances(lines: &Vec<i32>) -> Vec<i32> {
  (1..lines.len()).map(|index| {
    let current = lines[index];
    let previous = lines[index - 1];
    current - previous
  }).collect()
}

fn count_of(value: i32, vector: &Vec<i32>) -> i32 {
  vector.iter().filter(|&n| *n == value).count() as i32
}

fn wrap<T: Ord + Add<Output = T>>(value: T, min: T, max: T) -> T {
  if value < min {
    max + value
  } else {
    value
  }
}

fn max<T: PartialOrd + Copy>(vector: &Vec<T>) -> T {
  let mut largest = vector[0];

  for item in vector.iter() {
      if item > &largest {
          largest = *item;
      }
  }

  largest
}

fn solve_part_one(lines: &Vec<i32>) -> i32 {
  let differences = distances(&lines);
  let ones = count_of(1, &differences);
  let threes = count_of(3, &differences);
  ones * threes
}

fn solve_part_two(lines: &Vec<i32>) -> i64 {
  let size = lines.len();
  let possibility_count = max(&lines);
  let mut possibilities = Vec::new();
  possibilities.push(1);

  for _i in 0..possibility_count { possibilities.push(0); }

  for index in 1..size {
    let value = lines[index];
    let count = possibilities.len() as i32;
    let first = wrap(value - 1, 0, count);
    let second = wrap(value - 2, 0, count);
    let third = wrap(value - 3, 0, count);

    possibilities[value as usize] = possibilities[first as usize] + possibilities[second as usize] + possibilities[third as usize];
  }

  max(&possibilities)
}

fn main() -> Result<(), Error> {
    let mut lines = read_lines(File::open("./input.txt")?)?;
    lines.insert(0, 0);
    lines.push(max(&lines) + 3);
    lines.sort();
    println!("part_one: {}", solve_part_one(&lines));
    println!("part_two: {:?}", solve_part_two(&lines));
    Ok(())
}