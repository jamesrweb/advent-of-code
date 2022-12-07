use std::collections::hash_map::RandomState;
use std::collections::HashSet;
use std::error::Error;
use std::fs::read_to_string;
use std::path::Path;

fn main() -> Result<(), Box<dyn Error>> {
    let contents: String = read_to_string(Path::new("src/input.txt"))?.parse()?;
    let datastream_buffer: String = contents.lines().take(1).map(String::from).collect();

    match solve_part_one(datastream_buffer.clone()) {
        Some(result) => println!("Part one: {}", result),
        None => println!("No solution for part one found."),
    }

    match solve_part_two(datastream_buffer.clone()) {
        Some(result) => println!("Part two: {}", result),
        None => println!("No solution for part two found."),
    }

    Ok(())
}

fn solve_part_one(datastream_buffer: String) -> Option<usize> {
    search_packet(datastream_buffer, 4)
}

fn solve_part_two(datastream_buffer: String) -> Option<usize> {
    search_packet(datastream_buffer, 14)
}

fn search_packet(datastream_buffer: String, skip_size: usize) -> Option<usize> {
    Vec::from_iter(datastream_buffer.chars().into_iter())
        .as_slice()
        .windows(skip_size)
        .enumerate()
        .fold(None, |marker_index, (index, window)| {
            if marker_index.is_some() {
                return marker_index;
            }

            if String::from_iter(window.to_vec().iter()).unique().len() == skip_size {
                return Some(index + skip_size);
            }

            marker_index
        })
}

trait Unique {
    fn unique(&self) -> Self;
}

impl Unique for String {
    fn unique(&self) -> Self {
        let unique_chars: HashSet<char, RandomState> = HashSet::from_iter(self.chars().into_iter());

        unique_chars.into_iter().collect()
    }
}
