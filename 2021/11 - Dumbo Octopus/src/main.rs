use std::fs::read_to_string;

type Measurements2D = (usize, usize);
type Row<T> = Vec<T>;
type Matrix2D<T> = Vec<Row<T>>;

fn parse_matrix(input: String) -> Matrix2D<u8> {
    return input.split("\n").map(parse_matrix_row).collect();
}

fn parse_matrix_row(row: &str) -> Row<u8> {
    return row
        .split("")
        .filter(|&column| column.ne(""))
        .map(|column| column.parse::<u8>().unwrap().to_owned())
        .collect();
}

fn increment_column(matrix: &mut Matrix2D<u8>, x: usize, y: usize) {
    matrix[y][x] += 1;
}

fn increment_columns(matrix: &mut Matrix2D<u8>, (width, height): Measurements2D) {
    for y in 0..height {
        for x in 0..width {
            increment_column(matrix, x, y);
        }
    }
}

fn count_flashes_in_matrix(matrix: &mut Matrix2D<u8>, (width, height): Measurements2D) -> u32 {
    let mut flash_count = 0;

    for y in 0..height {
        for x in 0..width {
            if matrix[y][x] <= 9 {
                continue;
            }

            flash_count += flashes_in_vicinity(matrix, (width, height), (x, y));
        }
    }

    return flash_count;
}

fn reset_flashing_columns(matrix: &mut Matrix2D<u8>) {
    for row in matrix.iter_mut() {
        for column in row {
            if *column > 9 {
                *column = 0;
            }
        }
    }
}

fn sum_matrix(matrix: &mut Matrix2D<u8>) -> u32 {
    return matrix
        .iter()
        .map(|row| row.iter().map(|&column| u32::from(column)).sum::<u32>())
        .sum::<u32>();
}

fn solve(matrix: &mut Matrix2D<u8>, part_one: bool) -> u32 {
    let mut flash_count = 0;
    let mut current_step = 0;
    let dimensions = (matrix[0].len(), matrix.len());

    loop {
        increment_columns(matrix, dimensions);

        current_step += 1;
        flash_count += count_flashes_in_matrix(matrix, dimensions);

        reset_flashing_columns(matrix);

        if part_one && current_step == 100 {
            return flash_count;
        }

        if sum_matrix(matrix) == 0 {
            break;
        }
    }

    return current_step;
}

fn flashes_in_vicinity(
    matrix: &mut Matrix2D<u8>,
    (width, height): Measurements2D,
    (x, y): Measurements2D,
) -> u32 {
    if matrix[y][x] < 9 {
        increment_column(matrix, x, y);

        return 0;
    }

    if matrix[y][x] > 10 {
        return 0;
    }

    matrix[y][x] = 11;

    let top_left_neighbour = if x > 0 && y > 0 {
        flashes_in_vicinity(matrix, (width, height), (x - 1, y - 1))
    } else {
        0
    };

    let top_neighbour = if y > 0 {
        flashes_in_vicinity(matrix, (width, height), (x, y - 1))
    } else {
        0
    };

    let top_right_neighbour = if x < width - 1 && y > 0 {
        flashes_in_vicinity(matrix, (width, height), (x + 1, y - 1))
    } else {
        0
    };

    let left_neighbour = if x > 0 {
        flashes_in_vicinity(matrix, (width, height), (x - 1, y))
    } else {
        0
    };

    let right_neighbour = if x < width - 1 {
        flashes_in_vicinity(matrix, (width, height), (x + 1, y))
    } else {
        0
    };

    let bottom_left_neighbour = if x > 0 && y < height - 1 {
        flashes_in_vicinity(matrix, (width, height), (x - 1, y + 1))
    } else {
        0
    };

    let bottom_neighbour = if y < height - 1 {
        flashes_in_vicinity(matrix, (width, height), (x, y + 1))
    } else {
        0
    };

    let bottom_right_neighbour = if x < width - 1 && y < height - 1 {
        flashes_in_vicinity(matrix, (width, height), (x + 1, y + 1))
    } else {
        0
    };

    return 1
        + top_left_neighbour
        + top_neighbour
        + top_right_neighbour
        + left_neighbour
        + right_neighbour
        + bottom_left_neighbour
        + bottom_neighbour
        + bottom_right_neighbour;
}

fn solve_part_one(matrix: &mut Matrix2D<u8>) -> u32 {
    return solve(matrix, true);
}

fn solve_part_two(matrix: &mut Matrix2D<u8>) -> u32 {
    return solve(matrix, false);
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");
    let matrix = parse_matrix(input);

    println!("Part one: {}", solve_part_one(matrix.clone().as_mut()));
    println!("Part two: {}", solve_part_two(matrix.clone().as_mut()));
}
