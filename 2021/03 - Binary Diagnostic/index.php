<?php
declare(strict_types=1);

class ReportManager
{
    /** @var array<string> */
    private array $report = [];
    private int $gamma_rate_decimal = 0;
    private int $epsilon_rate_decimal = 0;
    private string $gamma_rate_binary = "";
    private string $epsilon_rate_binary = "";

    /**
     * @param array<string> $report
     */
    public function __construct(array $report)
    {
        if (count($report) === 0) {
            return;
        }

        $line_length = strlen($report[0]);
        $digit_counters = $this->initialiseDigitCounters($line_length);
        $digit_counts = $this->countDigits(
            $report,
            $digit_counters,
            $line_length
        );

        $this->report = array_map(fn($line) => trim($line), $report);
        $this->gamma_rate_binary = $this->generateGammaBits(
            $digit_counts,
            $line_length
        );
        $this->epsilon_rate_binary = $this->generateEpsilonBits(
            $digit_counts,
            $line_length
        );
        $this->gamma_rate_decimal = intval(bindec($this->gamma_rate_binary));
        $this->epsilon_rate_decimal = intval(
            bindec($this->epsilon_rate_binary)
        );
    }

    public function gamma_rate(): int
    {
        return $this->gamma_rate_decimal;
    }

    public function epsilon_rate(): int
    {
        return $this->epsilon_rate_decimal;
    }

    public function gamma_bits(): string
    {
        return $this->gamma_rate_binary;
    }

    public function epsilon_bits(): string
    {
        return $this->epsilon_rate_binary;
    }

    public function oxygenRating(): int
    {
        return $this->rating("1", "0");
    }

    public function co2Rating(): int
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
     * @param array<int, array<int>> $digit_counters
     *
     * @return array<int, array<int>>
     */
    private function countDigits(
        array $report,
        array $digit_counters,
        int $line_length
    ): array {
        $counts = $digit_counters;

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

    private function rating(string $onesChar, string $zerosChar): int
    {
        $rating = array_values($this->report);

        for ($i = 0; $i < strlen($this->report[1]); $i++) {
            $ones = array_filter(
                $rating,
                fn(string $line) => $line[$i] === "1"
            );
            $zeros = array_filter(
                $rating,
                fn(string $line) => $line[$i] === "0"
            );
            $character = count($ones) >= count($zeros) ? $onesChar : $zerosChar;
            $rating = array_filter(
                $rating,
                fn(string $line) => $line[$i] === $character
            );
            $rating = array_values($rating);

            if (count($rating) === 1) {
                break;
            }
        }

        return intval(bindec($rating[0]));
    }
}

/**
 * @param array<string> $report
 */
function solve_part_one(array $report): int
{
    $reportBitManager = new ReportManager($report);
    $gamma_rate = $reportBitManager->gamma_rate();
    $epsilon_rate = $reportBitManager->epsilon_rate();

    return $gamma_rate * $epsilon_rate;
}

/**
 * @param array<string> $report
 */
function solve_part_two(array $report): int
{
    $reportBitManager = new ReportManager($report);
    $oxygenRating = $reportBitManager->oxygenRating();
    $co2Rating = $reportBitManager->co2Rating();

    return $oxygenRating * $co2Rating;
}

function main(): void
{
    /** @var string **/
    $contents = file_get_contents(__DIR__ . "/input.txt", true);

    /** @var array<string> */
    $report = explode("\r\n", $contents);

    print_r([
        "part_one" => solve_part_one($report),
        "part_two" => solve_part_two($report),
    ]);
}

main();
?>
