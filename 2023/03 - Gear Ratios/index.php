<?php declare(strict_types=1);

readonly final class EngineSchematic
{
  /** @param array<array<string>> $schematic */
  public function __construct(private array $schematic)
  {
  }

  public static function fromFile(string $file): self
  {
    $handle = fopen($file, "r");

    if ($handle === false) {
      throw new Exception("No such file: " . $file);
    }

    $schematic = [];

    while (!feof($handle)) {
      $line = fgets($handle);

      if ($line === false) {
        continue;
      }

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

      foreach ($row as $char_index => $char) {
        if (is_numeric($char)) {
          $number = is_null($number) ? $char : $number . $char;
        } elseif (is_string($number)) {
          for (
            $i = $char_index - mb_strlen($number);
            $i < $char_index;
            $i = $i + 1
          ) {
            assert(is_numeric($row[$i]));

            $above = array_key_exists($row_index - 1, $this->schematic)
              ? $this->schematic[$row_index - 1]
              : null;
            $below = array_key_exists($row_index + 1, $this->schematic)
              ? $this->schematic[$row_index + 1]
              : null;

            // Row above
            $top_left =
              is_array($above) &&
              array_key_exists($i - 1, $above) &&
              $this->isSymbolMarker($above[$i - 1]);
            $top =
              is_array($above) &&
              array_key_exists($i, $above) &&
              $this->isSymbolMarker($above[$i]);
            $top_right =
              is_array($above) &&
              array_key_exists($i + 1, $above) &&
              $this->isSymbolMarker($above[$i + 1]);

            // Current row
            $left =
              array_key_exists($i - 1, $row) &&
              $this->isSymbolMarker($row[$i - 1]);
            $right =
              array_key_exists($i + 1, $row) &&
              $this->isSymbolMarker($row[$i + 1]);

            // Row below
            $bottom_left =
              is_array($below) &&
              array_key_exists($i - 1, $below) &&
              $this->isSymbolMarker($below[$i - 1]);
            $bottom =
              is_array($below) &&
              array_key_exists($i, $below) &&
              $this->isSymbolMarker($below[$i]);
            $bottom_right =
              is_array($below) &&
              array_key_exists($i + 1, $below) &&
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

  public function __toString(): string
  {
    return array_reduce(
      $this->schematic,
      function ($accumulator, $current) {
        $key = array_search($current, $this->schematic, true);

        if ($key === false) {
          return $accumulator;
        }

        $end = $key === count($this->schematic) - 1 ? "" : PHP_EOL;
        return $accumulator . json_encode(implode($current)) . $end;
      },
      ""
    );
  }
}

$engineSchematic = EngineSchematic::fromFile(__DIR__ . "/input.txt");

print_r([
  "part_one" => $engineSchematic->solvePartOne(),
  "part_two" => $engineSchematic->solvePartTwo()
]);
