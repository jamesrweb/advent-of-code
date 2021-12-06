use std::convert::TryInto;
use std::fs::read_to_string;

fn population_reproduction_timers_from_state(state: Vec<u8>) -> [i64; 9] {
    let mut counts = [0; 9];

    for (count, index) in counts.iter_mut().zip(0..=8) {
        *count = state
            .iter()
            .filter(|&n| *n == index)
            .count()
            .try_into()
            .unwrap();
    }

    return counts;
}

fn solve(state: Vec<u8>, days: i32) -> i64 {
    let mut population_reproduction_timers = population_reproduction_timers_from_state(state);

    for _ in 0..days {
        let fish_to_reproduce = population_reproduction_timers[0];
        population_reproduction_timers.rotate_left(1);
        population_reproduction_timers[6] += fish_to_reproduce;
        population_reproduction_timers[8] = fish_to_reproduce;
    }

    return population_reproduction_timers.iter().sum();
}

fn solve_part_one(initial_state: Vec<u8>) -> i64 {
    return solve(initial_state, 80);
}

fn solve_part_two(initial_state: Vec<u8>) -> i64 {
    return solve(initial_state, 256);
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");
    let state: Vec<u8> = input
        .split(",")
        .map(|value| value.parse::<u8>().unwrap().to_owned())
        .collect();

    println!("Part one: {}", solve_part_one(state.clone()));
    println!("Part two: {}", solve_part_two(state.clone()));
}
