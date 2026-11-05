namespace Playground

open System.IO

type ConfigurationOptions = {| isExampleInput: bool |}
type Configuration = {| path: string; connectionCount: int |}

type ConfigurationBuilder(configurationOptions: ConfigurationOptions) =
    member _.Build() : Configuration =
        {|
            path = Path.Join(__SOURCE_DIRECTORY__, "input.txt")
            connectionCount = if configurationOptions.isExampleInput then 10 else 1000
        |}
