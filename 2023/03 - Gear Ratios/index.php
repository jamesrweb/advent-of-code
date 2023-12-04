<?php declare(strict_types=1);

final class EngineSchematic
{
  /** @param array<array<string>> $schematic */
  public function __construct(private array $schematic)
  {
  }

  public function __toString(): string
  {
    return array_reduce(
      $this->schematic,
      function ($accumulator, $current) {
        return $accumulator . implode($current) . PHP_EOL;
      },
      ""
    );
  }

  public static function fromFile(string $file): self
  {
    $handle = fopen($file, "r");
    $schematic = [];

    while (!feof($handle)) {
      $line = fgets($handle);
      $line = trim($line);
      $schematic[] = str_split($line);
    }

    return new self($schematic);
  }

  private function isSymbolMarker(string $char): bool
  {
    return !is_numeric($char) && $char !== ".";
  }

  /**
   * Returns a list of numbers adjacent to a symbol within the engine schematic.
   *
   * @return array<int>
   */
  private function partNumbers(): array
  {
    $numbers = [];

    foreach ($this->schematic as $row_index => $row) {
      $number = null;
      $row_string = implode($row);

      foreach ($row as $char_index => $char) {
        if ($char === "." && !is_null($number)) {
          for (
            $i = $char_index - mb_strlen($number);
            $i <= $char_index;
            $i = $i + 1
          ) {
            $above = array_key_exists($row_index - 1, $this->schematic)
              ? $this->schematic[$row_index - 1]
              : null;
            $below = array_key_exists($row_index + 1, $this->schematic)
              ? $this->schematic[$row_index + 1]
              : null;

            // Row above
            $top_left =
              !is_null($above) &&
              array_key_exists($i - 1, $above) &&
              is_string($above[$i - 1]) &&
              $this->isSymbolMarker($above[$i - 1]);
            $top =
              !is_null($above) &&
              array_key_exists($i, $above) &&
              is_string($above[$i]) &&
              $this->isSymbolMarker($above[$i]);
            $top_right =
              !is_null($above) &&
              array_key_exists($i + 1, $above) &&
              is_string($above[$i + 1]) &&
              $this->isSymbolMarker($above[$i + 1]);

            // Current row
            $left =
              array_key_exists($i - 1, $row) &&
              is_string($row[$i - 1]) &&
              $this->isSymbolMarker($row[$i - 1]);
            $right =
              array_key_exists($i + 1, $row) &&
              is_string($row[$i + 1]) &&
              $this->isSymbolMarker($row[$i + 1]);

            // Row below
            $bottom_left =
              !is_null($below) &&
              array_key_exists($i - 1, $below) &&
              is_string($below[$i - 1]) &&
              $this->isSymbolMarker($below[$i - 1]);
            $bottom =
              !is_null($below) &&
              array_key_exists($i, $below) &&
              is_string($below[$i]) &&
              $this->isSymbolMarker($below[$i]);
            $bottom_right =
              !is_null($below) &&
              array_key_exists($i + 1, $below) &&
              is_string($below[$i + 1]) &&
              $this->isSymbolMarker($below[$i + 1]);

            if (
              $top_left ||
              $top ||
              $top_right ||
              $left ||
              $right ||
              $bottom_left ||
              $bottom ||
              $bottom_right
            ) {
              $numbers[] = intval($number, 10);
              break;
            }
          }

          $number = null;
        }

        if (is_numeric($char) && is_string($number)) {
          $number .= $char;
        }

        if (is_numeric($char) && is_null($number)) {
          $number = $char;
        }
      }
    }

    return $numbers;
  }

  public function solvePartOne(): int
  {
    return array_sum($this->partNumbers());
  }

  public function solvePartTwo(): int
  {
    return 2;
  }
}

$engineSchematic = EngineSchematic::fromFile(__DIR__ . "/input.txt");

print_r([
  "part_one" => $engineSchematic->solvePartOne(),
  "part_two" => $engineSchematic->solvePartTwo()
]);
