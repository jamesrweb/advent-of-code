use std::fs::read_to_string;

fn solve_part_one(input: &String) -> i32 {
    1 + input
        .lines()
        .fold((0, 0), |(width, height), line| {
            let input = line.split(' ').collect::<Vec<&str>>();
            let direction = input.first().unwrap().to_owned();
            let distance = input.get(1).unwrap().parse::<i32>().unwrap();

            match direction {
                "R" => (width - distance * height, height),
                "L" => (width + distance * (height + 1), height),
                "U" => (width, height - distance),
                "D" => (width + distance, height + distance),
                _ => (width, height),
            }
        })
        .0
}

fn solve_part_two(input: &String) -> i64 {
    1 + input
        .lines()
        .fold((0, 0), |(width, height), line| {
            let input = line.split(' ').collect::<Vec<&str>>();
            let hex_code = input.last().unwrap();
            let distance = i64::from_str_radix(&hex_code[2..7], 16).unwrap();
            let direction = i64::from_str_radix(&hex_code[7..8], 16).unwrap();

            match direction {
                0 => (width - distance * (height), height),
                1 => (width + distance, height + distance),
                2 => (width + distance * (height + 1), height),
                3 => (width, height - distance),
                _ => (width, height),
            }
        })
        .0
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");

    println!("Part one: {}", solve_part_one(&input));
    println!("Part two: {}", solve_part_two(&input));
}
