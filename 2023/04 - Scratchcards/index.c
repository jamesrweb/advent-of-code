#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Game
{
    int gameId;
    int *winningNumbers;
    int winningNumbersCount;
    int *myNumbers;
    int myNumbersCount;
};

void freeGame(struct Game *game)
{
    free(game->winningNumbers);
    free(game->myNumbers);
}

struct Game toGame(const char *line)
{
    struct Game game;
    char *winningNumbersStr = strtok((char *)line, "|");
    char *myNumbersStr = strtok(NULL, "|");
    char *token = strtok(winningNumbersStr + 8, " ");

    sscanf(line, "Card %d:", &game.gameId);
    game.winningNumbers = (int *)malloc(sizeof(int));
    game.winningNumbersCount = 0;

    while (token != NULL)
    {
        game.winningNumbers[game.winningNumbersCount++] = atoi(token);
        game.winningNumbers = (int *)realloc(game.winningNumbers, (game.winningNumbersCount + 1) * sizeof(int));
        token = strtok(NULL, " ");
    }

    game.myNumbers = (int *)malloc(sizeof(int));
    game.myNumbersCount = 0;
    token = strtok(myNumbersStr, " ");

    while (token != NULL)
    {
        game.myNumbers[game.myNumbersCount++] = atoi(token);
        game.myNumbers = (int *)realloc(game.myNumbers, (game.myNumbersCount + 1) * sizeof(int));
        token = strtok(NULL, " ");
    }

    return game;
}

struct Game *parseGames(FILE *file, int *gameCount)
{
    char line[256];
    struct Game *games = NULL;

    *gameCount = 0;

    while (fgets(line, sizeof(line), file) != NULL)
    {
        line[strcspn(line, "\n")] = '\0';
        struct Game game = toGame(line);
        games = (struct Game *)realloc(games, (*gameCount + 1) * sizeof(struct Game));
        games[(*gameCount)++] = game;
    }

    return games;
}

int countMatchingNumbers(const int *winningNumbers, int winningNumbersSize, const int *myNumbers, int myNumbersSize)
{
    int count = 0;

    for (int i = 0; i < winningNumbersSize; i++)
    {
        for (int j = 0; j < myNumbersSize; j++)
        {
            if (myNumbers[j] == winningNumbers[i])
            {
                count++;
                break;
            }
        }
    }

    return count;
}

int scoreForGame(struct Game game)
{
    int matchingNumbers = countMatchingNumbers(game.winningNumbers, game.winningNumbersCount, game.myNumbers, game.myNumbersCount);
    int score = 0;

    for (int i = 0; i < matchingNumbers; i++)
    {
        if (score == 0)
        {
            score = 1;
            continue;
        }

        score *= 2;
    }

    return score;
}

int scoreAcrossGames(struct Game *games, int *gameCount)
{
    int score = 0;

    for (int i = 0; i < *gameCount; i++)
    {
        struct Game game = games[i];
        score += scoreForGame(game);
    }

    for (int i = 0; i < *gameCount; i++)
    {
        freeGame(&games[i]);
    }

    return score;
}

int main()
{
    FILE *file;

    file = fopen("input.txt", "r");

    if (file == NULL)
    {
        perror("Error opening file");
        return 1;
    }

    int gameCount;
    struct Game *games = parseGames(file, &gameCount);
    int totalScore = scoreAcrossGames(games, &gameCount);

    printf("Part one: %d", totalScore);
    free(games);
    fclose(file);

    return 0;
}
