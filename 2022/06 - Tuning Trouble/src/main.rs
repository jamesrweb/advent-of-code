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
    let mut marker_index = None;
    let mut seen = HashSet::new();
    let mut start = 0;
    let end = datastream_buffer.len() - 1;

    loop {
        if start > end - skip_size {
            break;
        }

        let packet: Vec<char> = datastream_buffer
            .chars()
            .skip(start)
            .take(skip_size)
            .collect();

        let unique_packet = packet
            .clone()
            .into_iter()
            .fold(true, |accumulator, signal| {
                if accumulator == false {
                    return accumulator;
                }

                if packet.clone().into_iter().filter(|&c| c == signal).count() > 1 {
                    return false;
                }

                true
            });

        let letters_not_seen = packet
            .clone()
            .into_iter()
            .fold(false, |accumulator, signal| {
                if accumulator == true {
                    return accumulator;
                }

                if seen.contains(&signal) {
                    return true;
                }

                accumulator
            });

        packet.clone().into_iter().for_each(|signal| {
            seen.insert(signal);
        });

        if unique_packet && letters_not_seen {
            marker_index = Some(start + skip_size);
            break;
        }

        start += 1;
    }

    marker_index
}
