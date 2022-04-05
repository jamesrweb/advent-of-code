<?php

declare(strict_types=1);

namespace AdventOfCodeDay3;

use Exception;

class Report
{
  /** @var array<string> */
  private array $lines = [];

  /** @param array<string> $lines */
  public function __construct(array $lines)
  {
    $this->lines = $lines;
  }

  public static function fromInputData(string $data): Report
  {
    $lines = explode(PHP_EOL, $data);

    return new Report($lines);
  }

  public function lineCount(): int
  {
    return count($this->lines);
  }

  /** @return array<string> */
  public function lines(): array
  {
    return $this->lines;
  }
}

class ReportManager
{
  private Report $report;
  private int|float $gamma_rate_decimal = 0;
  private int|float $epsilon_rate_decimal = 0;
  private string $gamma_rate_binary = "";
  private string $epsilon_rate_binary = "";

  public function __construct(Report $report)
  {
    if ($report->lineCount() === 0) {
      return;
    }

    $lines = $report->lines();
    $line_length = strlen($lines[0]);
    $digit_counts = $this->countDigits($lines, $line_length);

    $this->report = $report;
    $this->gamma_rate_binary = $this->generateGammaBits(
      $digit_counts,
      $line_length
    );
    $this->epsilon_rate_binary = $this->generateEpsilonBits(
      $digit_counts,
      $line_length
    );
    $this->gamma_rate_decimal = bindec($this->gamma_rate_binary);
    $this->epsilon_rate_decimal = bindec($this->epsilon_rate_binary);
  }

  public function gamma_rate(): int|float
  {
    return $this->gamma_rate_decimal;
  }

  public function epsilon_rate(): int|float
  {
    return $this->epsilon_rate_decimal;
  }

  public function oxygenRating(): int|float
  {
    return $this->rating("1", "0");
  }

  public function co2Rating(): int|float
  {
    return $this->rating("0", "1");
  }

  /**
   * @return array<int, array<int>>
   */
  private function initialiseDigitCounters(int $line_length): array
  {
    $digit_counters = [];

    for ($index = 0; $index < $line_length; $index++) {
      $digit_counters[$index] = [0, 0];
    }

    return $digit_counters;
  }

  /**
   * @param array<string> $report
   *
   * @return array<int, array<int>>
   */
  private function countDigits(array $report, int $line_length): array
  {
    $counts = $this->initialiseDigitCounters($line_length);

    foreach ($report as $line) {
      for ($index = 0; $index < $line_length; $index++) {
        $digit = $line[$index];
        $counts[$index][$digit]++;
      }
    }

    return $counts;
  }

  /**
   * @param array<int, array<int>> $digit_counts
   */
  private function generateGammaBits(
    array $digit_counts,
    int $line_length
  ): string {
    $gamma_rate_binary = "";

    for ($index = 0; $index < $line_length; $index++) {
      $counts = $digit_counts[$index];
      $gamma_rate_binary[$index] = $counts[1] >= $counts[0] ? 1 : 0;
    }

    return $gamma_rate_binary;
  }

  /**
   * @param array<int, array<int>> $digit_counts
   */
  private function generateEpsilonBits(
    array $digit_counts,
    int $line_length
  ): string {
    $epsilon_bits = "";

    for ($index = 0; $index < $line_length; $index++) {
      $counts = $digit_counts[$index];
      $epsilon_bits[$index] = $counts[1] >= $counts[0] ? 0 : 1;
    }

    return $epsilon_bits;
  }

  private function rating(string $onesChar, string $zerosChar): int|float
  {
    $lines = $this->report->lines();

    for ($index = 0; $index < strlen($lines[1]); $index++) {
      $ones = array_filter(
        $lines,
        static fn(string $line) => $line[$index] === "1"
      );
      $zeros = array_filter(
        $lines,
        static fn(string $line) => $line[$index] === "0"
      );
      $character = count($ones) >= count($zeros) ? $onesChar : $zerosChar;
      $lines = array_reduce(
        $lines,
        $this->keepLinesWithCharacterAtIndex($character, $index),
        []
      );

      if (count($lines) === 1) {
        break;
      }
    }

    return bindec($lines[0]);
  }

  /**
   * @return callable(array<string>, string): array<string>
   */
  private function keepLinesWithCharacterAtIndex(
    string $character,
    int $index
  ): callable {
    return static function (array $carry, string $line) use (
      $character,
      $index
    ) {
      if ($line[$index] === $character) {
        return array_merge($carry, [$line]);
      }

      return $carry;
    };
  }
}

function solve_part_one(Report $report): int|float
{
  $reportBitManager = new ReportManager($report);
  $gamma_rate = $reportBitManager->gamma_rate();
  $epsilon_rate = $reportBitManager->epsilon_rate();

  return $gamma_rate * $epsilon_rate;
}

function solve_part_two(Report $report): int|float
{
  $reportBitManager = new ReportManager($report);
  $oxygenRating = $reportBitManager->oxygenRating();
  $co2Rating = $reportBitManager->co2Rating();

  return $oxygenRating * $co2Rating;
}

function load_input_data(): string
{
  $file = __DIR__ . "/input.txt";
  $contents = file_get_contents($file, true);

  if ($contents === false) {
    throw new Exception("Could not load file: \"$file\".");
  }

  return $contents;
}

function main(): void
{
  $data = load_input_data();
  $report = Report::fromInputData($data);

  print_r([
    "part_one" => solve_part_one($report),
    "part_two" => solve_part_two($report)
  ]);
}

main();
