<?php

declare(strict_types=1);

namespace AdventOfCode;

require_once dirname(__DIR__) . "/vendor/autoload.php";

use Exception;

function main(): void
{
  $data = load_file_contents(__DIR__ . "/input.txt");
  $backpacks = array_map(
    fn(string $line) => Backpack::fromString($line),
    explode(PHP_EOL, $data),
  );

  print_r([
    "part_one" => solve_part_one($backpacks),
    "part_two" => solve_part_two($backpacks),
  ]);
}

main();

/**
 * Driver code for part one.
 *
 * @param array<Backpack> $backpacks
 *
 * @return int
 */
function solve_part_one(array $backpacks): int
{
  $scores = array_map(
    fn(Backpack $backpack) => $backpack->commonCompartmentItemsScore(),
    $backpacks,
  );

  return array_sum($scores);
}

/**
 * Driver code for part two.
 *
 * @param array<Backpack> $backpacks
 *
 * @return int
 */
function solve_part_two(array $backpacks): int
{
  $groups = array_chunk($backpacks, 3);
  $sharedGroupItems = array_map(
    fn(array $group) => Backpack::empty()->shared($group),
    $groups,
  );
  $line = join("", array_merge(...$sharedGroupItems));

  return Backpack::fromString($line)->itemsScore();
}

/**
 * Load file data.
 *
 * @param string $file Path of the file to load.
 *
 * @throws Exception If data could not be loaded.
 * @return string
 */
function load_file_contents(string $file): string
{
  $contents = file_get_contents($file, true);

  if ($contents === false) {
    throw new Exception("Could not load file: \"$file\".");
  }

  return $contents;
}
