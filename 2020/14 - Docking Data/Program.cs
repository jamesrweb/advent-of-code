using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Collections.Generic;

namespace Docking_Data
{
    class Program
    {
        static string ChangeBase(string value, int from, int to)
        {
            return Convert.ToString(Convert.ToInt64(value, from), to);
        }

        static long SolvePartOne(string[] data)
        {
            var mask = String.Empty;
            var memory = new Dictionary<string, long>();

            foreach (var line in data)
            {
                var info = line.Split(" = ");

                if (info[0] == "mask")
                {
                    mask = info[1];
                    continue;
                }

                var start = 4;
                var size = info[0].Length - start - 1;
                var address = info[0].Substring(start, size);
                var result = String.Empty;
                var binary_value = ChangeBase(info[1], 10, 2).Reverse().ToArray();
                var mask_bits = mask.Reverse().ToList();

                foreach (var current in mask_bits.Select((bit, index) => new { index, bit }))
                {
                    if (current.bit == '0' || current.bit == '1')
                    {
                        result = current.bit + result;
                        continue;
                    }

                    if (current.index < binary_value.Length)
                    {
                        result = binary_value[current.index] + result;
                        continue;
                    }

                    result = result = "0" + result;
                }

                memory[address] = Convert.ToInt64(ChangeBase(result, 2, 10));
            }

            return memory.Values.Sum();
        }

        static long SolvePartTwo(string[] data)
        {
            var mask = string.Empty;
            var memory = new Dictionary<long, long>();
            var combinations = 0;

            foreach (var line in data)
            {
                var info = line.Split(" = ");

                if (info[0] == "mask")
                {
                    mask = info[1];
                    var xs = mask.Count(value => value == 'X');
                    combinations = Convert.ToInt32(Math.Pow(2, xs));
                    continue;
                }

                var start = 4;
                var size = info[0].Length - start - 1;
                var address = info[0].Substring(start, size);
                var value = info[1];

                for (var i = 0; i < combinations; i++)
                {
                    var offset = 0;
                    var result = Convert.ToInt64(address);

                    for (var j = 0; j < mask.Length; j++)
                    {
                        var current = mask[mask.Length - j - 1];

                        if (current == 'X')
                        {
                            if (((i >> offset) & 1) == 0) result &= ~(1L << j);
                            else result |= (1L << j);

                            offset++;
                        }
                        else if (current == '1')
                        {
                            result |= (1L << j);
                        }
                    }

                    memory[result] = Convert.ToInt64(value);
                }
            }

            return memory.Values.Sum();
        }

        static void Main(string[] args)
        {
            var input = File.ReadAllLines("./input.txt", Encoding.UTF8);
            Console.WriteLine("part_one: " + SolvePartOne(input));
            Console.WriteLine("part_two: " + SolvePartTwo(input));
        }
    }
}
