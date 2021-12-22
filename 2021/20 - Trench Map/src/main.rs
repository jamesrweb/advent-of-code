use std::collections::HashSet;
use std::fs::read_to_string;

type AlgorithmRules = Vec<u8>;
type LitPixels = HashSet<Point2D>;

#[derive(Eq, Hash)]
struct Point2D {
    x: i32,
    y: i32,
}

struct ImageEnhancementAlgorithmSimulator {
    rules: AlgorithmRules,
    lit_pixels: LitPixels,
    row_min: i32,
    row_max: i32,
    column_min: i32,
    column_max: i32,
}

impl PartialEq for Point2D {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl ImageEnhancementAlgorithmSimulator {
    fn new() -> ImageEnhancementAlgorithmSimulator {
        ImageEnhancementAlgorithmSimulator {
            rules: Vec::new(),
            lit_pixels: HashSet::new(),
            row_min: i32::MAX,
            row_max: i32::MIN,
            column_min: i32::MAX,
            column_max: i32::MIN,
        }
    }

    fn initialise_from_input(&mut self, input: String) {
        let mut lines = input.lines();
        self.rules = lines
            .next()
            .unwrap()
            .chars()
            .map(|character| {
                if character == '#' {
                    return 1;
                }

                return 0;
            })
            .collect();

        for (row_index, row) in lines.enumerate() {
            for (column_index, column) in row.chars().enumerate() {
                if column == '#' {
                    let row_index_i32 = i32::try_from(row_index).unwrap_or(0);
                    let column_index_i32 = i32::try_from(column_index).unwrap_or(0);

                    self.row_min = self.row_min.min(row_index_i32);
                    self.row_max = self.row_max.max(row_index_i32);
                    self.column_min = self.column_min.min(column_index_i32);
                    self.column_max = self.column_max.max(column_index_i32);

                    let lit_pixel = Point2D {
                        x: column_index_i32,
                        y: row_index_i32,
                    };

                    self.lit_pixels.insert(lit_pixel);
                }
            }
        }
    }

    fn run(&mut self, steps: i32) -> i32 {
        for step in 0..steps {
            self.lit_pixels = self.simulate_algorithm_cycles(step % 2 == 0);
        }

        return i32::try_from(self.lit_pixels.len()).unwrap_or(0);
    }

    fn simulate_algorithm_cycles(&mut self, track_lit_pixels: bool) -> LitPixels {
        let mut next_lit_pixels: LitPixels = HashSet::new();
        let mut next_row_min = i32::MAX;
        let mut next_row_max = i32::MIN;
        let mut next_column_min = i32::MAX;
        let mut next_column_max = i32::MIN;

        for row in (self.row_min - 1)..=(self.row_max + 1) {
            for column in (self.column_min - 1)..=(self.column_max + 1) {
                let mut index_bits = Vec::new();

                for row_index in (row - 1)..=(row + 1) {
                    for column_index in (column - 1)..=(column + 1) {
                        let lit_pixel = Point2D {
                            x: column_index,
                            y: row_index,
                        };

                        if self.lit_pixels.contains(&lit_pixel) {
                            let next_bit = if track_lit_pixels { 1 } else { 0 };
                            index_bits.push(next_bit);
                            continue;
                        }

                        let next_bit = if track_lit_pixels { 0 } else { 1 };
                        index_bits.push(next_bit);
                    }
                }

                let binary_index = index_bits
                    .iter()
                    .map(|digit| digit.to_string())
                    .collect::<String>();
                let index = usize::from_str_radix(&binary_index, 2).unwrap();

                if (self.rules[index] == 0) == track_lit_pixels {
                    next_lit_pixels.insert(Point2D { x: column, y: row });
                    let row_i32 = i32::try_from(row).unwrap_or(0);
                    let column_i32 = i32::try_from(column).unwrap_or(0);

                    next_row_min = next_row_min.min(row_i32);
                    next_row_max = next_row_max.max(row_i32);
                    next_column_min = next_column_min.min(column_i32);
                    next_column_max = next_column_max.max(column_i32);
                }
            }
        }

        self.row_min = next_row_min;
        self.row_max = next_row_max;
        self.column_min = next_column_min;
        self.column_max = next_column_max;

        return next_lit_pixels;
    }
}

fn solve_part_one(input: String) -> i32 {
    let mut simulator = ImageEnhancementAlgorithmSimulator::new();
    simulator.initialise_from_input(input);

    return simulator.run(2);
}

fn solve_part_two(input: String) -> i32 {
    let mut simulator = ImageEnhancementAlgorithmSimulator::new();
    simulator.initialise_from_input(input);

    return simulator.run(50);
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");

    println!("Part one: {}", solve_part_one(input.clone()));
    println!("Part two: {}", solve_part_two(input.clone()));
}
