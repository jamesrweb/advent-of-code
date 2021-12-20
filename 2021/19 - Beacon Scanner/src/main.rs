use std::collections::{HashMap, HashSet};
use std::fs::read_to_string;

type Point = (i64, i64, i64);
type Distance = Point;
type Scanner = HashSet<Point>;

const MIN_REQUIRED_OVERLAPPING_BEACON_COUNT: usize = 12;

struct ScannerDetectionResult {
    base_scanner_index: usize,
    comparison_scanner_index: usize,
    distance: Distance,
    moved_scanner: Scanner,
}

fn calculate_scanner_distance(input: String) -> i64 {
    let mut scanners = parse_input(input);
    let mut distances = Vec::new();

    while scanners.len() > 1 {
        if let Some(merge_result) = try_detect_scanners(&scanners) {
            distances.push(merge_result.distance);
            scanners.remove(merge_result.comparison_scanner_index);
            *scanners.get_mut(merge_result.base_scanner_index).unwrap() =
                merge_result.moved_scanner;
        }
    }

    let mut distance_comparisons = Vec::new();
    for (index, base_point) in distances.iter().copied().enumerate() {
        for comparison_point in distances.iter().skip(index + 1).copied() {
            let x_difference = (base_point.0 - comparison_point.0).abs();
            let y_difference = (base_point.1 - comparison_point.1).abs();
            let z_difference = (base_point.2 - comparison_point.2).abs();
            let distance = x_difference + y_difference + z_difference;

            distance_comparisons.push(distance);
        }
    }

    return distance_comparisons.iter().max().unwrap_or(&0).to_owned();
}

fn count_beacons(scanners: &mut Vec<Scanner>) -> usize {
    while scanners.len() > 1 {
        if let Some(merge_result) = try_detect_scanners(&scanners) {
            scanners.remove(merge_result.comparison_scanner_index);
            *scanners.get_mut(merge_result.base_scanner_index).unwrap() =
                merge_result.moved_scanner;
        }
    }

    return scanners.first().unwrap().len();
}

fn try_detect_scanners(scanners: &Vec<Scanner>) -> Option<ScannerDetectionResult> {
    for (base_scanner_index, base_scanner) in scanners.iter().enumerate() {
        let comparison_scanners = scanners.iter().enumerate().skip(base_scanner_index + 1);

        for (comparison_scanner_index, comparison_scanner) in comparison_scanners {
            for comparison_scanner in apply_rotation_to_scanner(comparison_scanner) {
                if let Some(distance) =
                    try_match_points_within_range(base_scanner, &comparison_scanner)
                {
                    let mut moved_scanner =
                        shift_scanner_by_distance(&comparison_scanner, distance);

                    for point in base_scanner {
                        moved_scanner.insert(*point);
                    }

                    let merge_result = ScannerDetectionResult {
                        base_scanner_index,
                        comparison_scanner_index,
                        distance,
                        moved_scanner,
                    };

                    return Some(merge_result);
                }
            }
        }
    }

    return None;
}

fn shift_scanner_by_distance(scanner: &Scanner, distance: Distance) -> Scanner {
    return scanner
        .iter()
        .map(|(x, y, z)| (x + distance.0, y + distance.1, z + distance.2))
        .collect();
}

fn try_match_points_within_range(
    base_scanner: &Scanner,
    comparison_scanner: &Scanner,
) -> Option<Distance> {
    let mut distances_point: HashMap<Distance, HashSet<Point>> = HashMap::new();

    for comparison_point in comparison_scanner.iter().copied() {
        for base_point in base_scanner.iter().copied() {
            let point_position_difference = (
                base_point.0 - comparison_point.0,
                base_point.1 - comparison_point.1,
                base_point.2 - comparison_point.2,
            );

            distances_point
                .entry(point_position_difference)
                .or_default()
                .insert(comparison_point);
        }
    }

    let matching_distances = distances_point
        .iter()
        .filter(|(_, points)| points.len() >= MIN_REQUIRED_OVERLAPPING_BEACON_COUNT)
        .map(|(distance, _)| *distance)
        .collect::<Vec<Distance>>();

    if matching_distances.is_empty() {
        return None;
    }

    return Some(*matching_distances.first().unwrap());
}

fn apply_rotation_to_scanner(scanner: &Scanner) -> Vec<Scanner> {
    let axis_shifts = [
        |(x, y, z): Point| (x, y, z),
        |(x, y, z): Point| (x, z, y),
        |(x, y, z): Point| (y, x, z),
        |(x, y, z): Point| (y, z, x),
        |(x, y, z): Point| (z, x, y),
        |(x, y, z): Point| (z, y, x),
    ];
    let rotations = [
        |(x, y, z): Point| (x, y, z),
        |(x, y, z): Point| (-x, -y, z),
        |(x, y, z): Point| (x, -y, -z),
        |(x, y, z): Point| (-x, y, -z),
        |(x, y, z): Point| (-x, -y, -z),
        |(x, y, z): Point| (-x, y, z),
        |(x, y, z): Point| (x, -y, z),
        |(x, y, z): Point| (x, y, -z),
    ];

    let mut all_possible_scanner_rotations = Vec::new();

    for apply_axis_shift in axis_shifts {
        for apply_rotation in rotations {
            let variation = scanner
                .iter()
                .map(|point| {
                    let with_rotation = apply_rotation(point.clone());

                    return apply_axis_shift(with_rotation);
                })
                .collect::<Scanner>();
            all_possible_scanner_rotations.push(variation);
        }
    }

    return all_possible_scanner_rotations;
}

fn parse_input(input: String) -> Vec<Scanner> {
    let mut scanners = Vec::new();
    let mut scanner = Scanner::new();

    for line in input.lines() {
        if line.trim() == "" {
            continue;
        }

        if line.starts_with("---") {
            if !scanner.is_empty() {
                scanners.push(scanner);
                scanner = Scanner::new();
            }
            continue;
        }

        let parts = line.split(",").collect::<Vec<_>>();
        let x = parts[0].parse().unwrap();
        let y = parts[1].parse().unwrap();
        let z = parts[2].parse().unwrap();

        scanner.insert((x, y, z));
    }

    scanners.push(scanner);

    return scanners;
}

fn solve_part_one(input: String) -> usize {
    let mut scanners = parse_input(input);

    return count_beacons(scanners.as_mut());
}

fn solve_part_two(input: String) -> i64 {
    return calculate_scanner_distance(input);
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");

    println!("Part one: {}", solve_part_one(input.clone()));
    println!("Part two: {}", solve_part_two(input.clone()));
}
