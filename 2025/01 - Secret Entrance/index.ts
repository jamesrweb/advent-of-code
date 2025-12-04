import * as fs from "node:fs/promises";
import * as os from "node:os";

type PasswordSolverConfiguration = {
  dial: number;
  landings: number;
  touches: number;
};

type Instruction = { kind: "left" | "right"; steps: number };

/**
 * Loads and processes instructions from the input file.
 *
 * The method reads the input file containing instructions, separates
 * them by lines, and parses each line into an object containing the
 * instruction type and its associated count.
 *
 * @return {Promise<Instruction[]>} A promise that resolves to an array of instruction objects,
 *                                  where each object contains a `kind` key representing the
 *                                  direction ('left' or 'right') and a `count` key representing
 *                                  the associated moves to make in that direction.
 */
async function loadInstructions(): Promise<Instruction[]> {
  const instructions = await fs.readFile("input.txt", "utf8");

  return instructions
    .trim()
    .split(os.EOL)
    .map(line => line.trim())
    .map(line => {
      const direction = line[0];
      const steps = parseInt(line.slice(1), 10);

      return { steps, kind: direction === "L" ? "left" : "right" };
    });
}

/**
 * Generates an array of consecutive numbers within a specified range, inclusive of both start and end values.
 *
 * @param {number} start - The starting number of the range.
 * @param {number} end - The ending number of the range.
 *
 * @return {number[]} An array containing numbers from the starting value to the ending value, inclusive.
 */
function createRange(start: number, end: number): number[] {
  if (start > end) {
    [start, end] = [end, start];
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}
/**
 * Calculates the number of times the dial crosses zero during a rotation
 * based on the provided instructions and initial and current configurations.
 *
 * @param {PasswordSolverConfiguration} previous - The previous dial configuration.
 * @param {PasswordSolverConfiguration} current - The current dial configuration.
 *
 * @return {number} The number of times the dial crossed zero during the rotation.
 */
function timesCrossedZeroDuringRotation(
  previous: PasswordSolverConfiguration,
  current: PasswordSolverConfiguration
): number {
  const range = createRange(current.dial, previous.dial);

  return range.filter(n => n % 100 === 0).length;
}

/**
 * Reduces the password state based on the current configuration and instruction.
 *
 * @param {PasswordSolverConfiguration} configuration - The current configuration containing the password and dial settings.
 * @param {Instruction} instruction - The instruction specifying how the dial should be rotated.
 *
 * @return {PasswordSolverConfiguration} The updated password and the resulting dial number.
 */
function passwordReducer(
  configuration: PasswordSolverConfiguration,
  instruction: Instruction
): PasswordSolverConfiguration {
  const dial =
    instruction.kind === "left"
      ? configuration.dial - instruction.steps
      : configuration.dial + instruction.steps;
  const landings =
    dial % 100 === 0 ? configuration.landings + 1 : configuration.landings;
  const crosses = timesCrossedZeroDuringRotation(configuration, {
    ...configuration,
    landings,
    dial
  });

  return { dial, landings, touches: configuration.touches + crosses };
}

async function main() {
  const instructions = await loadInstructions();
  const { touches, landings } =
    instructions.reduce<PasswordSolverConfiguration>(passwordReducer, {
      landings: 0,
      touches: 0,
      dial: 50
    });

  console.log({
    part_one: landings,
    part_two: touches - landings
  });
}

await main();
