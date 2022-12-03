<?php

declare(strict_types=1);

namespace AdventOfCode;

require_once dirname(__DIR__) . "/vendor/autoload.php";

use Ds\Map;
use Exception;

class Polymer
{
  /** @var Map<string, array<string>> */
  private Map $insertion_rules;
  private string $initial_polymer;

  /**
   * @param Map<string, array<string>> $insertion_rules
   */
  public function __construct(string $initial_polymer, Map $insertion_rules)
  {
    $this->initial_polymer = $initial_polymer;
    $this->insertion_rules = $insertion_rules;
  }

  public function initialPolymer(): string
  {
    return $this->initial_polymer;
  }

  /**
   * @return Map<string, array<string>>
   */
  public function insertionRulesMap(): Map
  {
    return $this->insertion_rules;
  }
}

/**
 * @return Map<string, int>
 */
function createPolymerWindowsWithCounts(string $string): Map
{
  $polymer_windows_with_counts = new Map();

  for ($index = 0; $index < strlen($string) - 1; $index++) {
    $polymer = $string[$index] . $string[$index + 1];
    $polymer_windows_with_counts->put($polymer, 1);
  }

  return $polymer_windows_with_counts;
}

/**
 * @param Map<string, int> $polymer_windows
 * @param Map<string, array<string>> $insertion_rules
 *
 * @return Map<string, int>
 */
function updatePolymerWindowsWithCounts(
  Map $polymer_windows,
  Map $insertion_rules
): Map {
  $new_polymer_windows = new Map();

  foreach ($polymer_windows->keys() as $polymer) {
    $insertion_polymer = $insertion_rules->get($polymer);
    $left_element_count = $new_polymer_windows->get($insertion_polymer[0], 0);
    $right_element_count = $new_polymer_windows->get($insertion_polymer[1], 0);
    $polymer_window_count = $polymer_windows->get($polymer, 0);

    $new_polymer_windows->putAll([
      $insertion_polymer[0] => $left_element_count + $polymer_window_count,
      $insertion_polymer[1] => $right_element_count + $polymer_window_count
    ]);
  }

  return $new_polymer_windows;
}

/**
 * @param Map<string, int> $polymer_windows
 *
 * @return Map<string, int>
 */
function countAtomsInPolymerWindows(
  Map $polymer_windows,
  string $initial_polymer
) {
  $atom_counts = new Map();
  $final_element = $initial_polymer[strlen($initial_polymer) - 1];
  $atom_counts->put($final_element, 1);

  foreach ($polymer_windows->keys() as $polymer) {
    $atom = $polymer[0];
    $current_atom_count = $atom_counts->get($atom, 0);
    $current_element_count = $polymer_windows->get($polymer, 0);

    $atom_counts->put($atom, $current_atom_count + $current_element_count);
  }

  return $atom_counts;
}

function solve(Polymer $polymer, int $steps): int
{
  $initial_polymer = $polymer->initialPolymer();
  $insertion_rules = $polymer->insertionRulesMap();
  $polymer_windows = array_reduce(
    range(0, $steps - 1),
    fn(Map $polymer_windows) => updatePolymerWindowsWithCounts(
      $polymer_windows,
      $insertion_rules
    ),
    createPolymerWindowsWithCounts($initial_polymer)
  );

  $element_counts = countAtomsInPolymerWindows(
    $polymer_windows,
    $initial_polymer
  );
  $element_counts->sort();
  $values = $element_counts->values()->toArray();
  $min = min($values);
  $max = max($values);

  if ($min === false || $max === false) {
    return 0;
  }

  return intval($max - $min);
}

function loadInputData(): string
{
  $file = __DIR__ . "/input.txt";
  $contents = file_get_contents($file, true);

  if ($contents === false) {
    throw new Exception("Could not load file: \"$file\".");
  }

  return $contents;
}

function parseInputData(string $data): Polymer
{
  $sections = mb_split(PHP_EOL . PHP_EOL, $data);

  if ($sections === false) {
    throw new Exception("Could not parse the input data.");
  }

  [$initial_polymer, $raw_insertion_rules] = $sections;

  $raw_insertion_rules = mb_split(PHP_EOL, $raw_insertion_rules);

  if ($raw_insertion_rules === false) {
    throw new Exception("Could not parse insertion rules.");
  }

  $insertion_rules = new Map();

  foreach ($raw_insertion_rules as $raw_insertion_rule) {
    $insertion_rule_parts = mb_split(" -> ", $raw_insertion_rule);

    if ($insertion_rule_parts === false) {
      throw new Exception(
        "Could not parse insertion rule: '$raw_insertion_rule'."
      );
    }

    [$polymer_pair, $insertion_element] = $insertion_rule_parts;

    $created_elements = [
      $polymer_pair[0] . $insertion_element,
      $insertion_element . $polymer_pair[1]
    ];
    $insertion_rules->put($polymer_pair, $created_elements);
  }

  return new Polymer($initial_polymer, $insertion_rules);
}

function main(): void
{
  $data = loadInputData();
  $polymer = parseInputData($data);

  print_r([
    "part_one" => solve($polymer, 10),
    "part_two" => solve($polymer, 40)
  ]);
}

main();
