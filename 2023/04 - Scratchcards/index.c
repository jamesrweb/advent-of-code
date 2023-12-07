#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 256
#define INITIAL_ARRAY_SIZE 10

struct Card
{
    int cardId;
    int *winningNumbers;
    int winningNumbersCount;
    int *myNumbers;
    int myNumbersCount;
};

void freeCard(struct Card *card)
{
    free(card->winningNumbers);
    free(card->myNumbers);
}

struct Card toCard(const char *line)
{
    struct Card card;
    char *winningNumbersStr = strtok(strdup(line), "|");
    char *myNumbersStr = strtok(NULL, "|");
    char *token = strtok(winningNumbersStr + 8, " ");

    sscanf(line, "Card %d:", &card.cardId);
    card.winningNumbers = (int *)malloc(INITIAL_ARRAY_SIZE * sizeof(int));
    card.winningNumbersCount = 0;

    while (token != NULL)
    {
        if (card.winningNumbersCount >= INITIAL_ARRAY_SIZE)
        {

            card.winningNumbers = (int *)realloc(card.winningNumbers, 2 * card.winningNumbersCount * sizeof(int));
        }

        card.winningNumbers[card.winningNumbersCount++] = atoi(token);
        token = strtok(NULL, " ");
    }

    card.myNumbers = (int *)malloc(INITIAL_ARRAY_SIZE * sizeof(int));
    card.myNumbersCount = 0;
    token = strtok(myNumbersStr, " ");

    while (token != NULL)
    {
        if (card.myNumbersCount >= INITIAL_ARRAY_SIZE)
        {

            card.myNumbers = (int *)realloc(card.myNumbers, 2 * card.myNumbersCount * sizeof(int));
        }

        card.myNumbers[card.myNumbersCount++] = atoi(token);
        token = strtok(NULL, " ");
    }

    free(winningNumbersStr);
    return card;
}

struct Card *parseCards(FILE *file, int *cardCount)
{
    char line[MAX_LINE_LENGTH];
    struct Card *cards = NULL;

    *cardCount = 0;

    while (fgets(line, sizeof(line), file) != NULL)
    {
        line[strcspn(line, "\n")] = '\0';
        struct Card card = toCard(line);
        cards = (struct Card *)realloc(cards, (*cardCount + 1) * sizeof(struct Card));
        cards[(*cardCount)++] = card;
    }

    return cards;
}

struct Card cloneCard(const struct Card *original)
{
    struct Card clone;

    clone.cardId = original->cardId;
    clone.winningNumbersCount = original->winningNumbersCount;
    clone.myNumbersCount = original->myNumbersCount;

    clone.winningNumbers = original->winningNumbers;
    clone.myNumbers = original->myNumbers;

    return clone;
}

struct MatchingNumbersResult
{
    int *matches;
    int size;
};

struct MatchingNumbersResult findMatchingNumbersForCard(struct Card card)
{
    struct MatchingNumbersResult result;
    result.matches = NULL;
    result.size = 0;

    for (int i = 0; i < card.winningNumbersCount; i++)
    {
        for (int j = 0; j < card.myNumbersCount; j++)
        {
            if (card.myNumbers[j] == card.winningNumbers[i])
            {
                result.size++;
                result.matches = (int *)realloc(result.matches, result.size * sizeof(int));
                result.matches[result.size - 1] = card.myNumbers[j];
                break;
            }
        }
    }

    return result;
}

int scoreForCard(struct Card card)
{
    struct MatchingNumbersResult matchingNumbers = findMatchingNumbersForCard(card);
    int score = 0;

    for (int i = 0; i < matchingNumbers.size; i++)
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

int scoreAcrossCards(struct Card *cards, int *cardCount)
{
    int score = 0;

    for (int i = 0; i < *cardCount; i++)
    {
        struct Card card = cards[i];
        score += scoreForCard(card);
    }

    return score;
}

int scratchCardsWon(struct Card *cards, int *cardCount)
{
    int wonCards[*cardCount];
    int matchCount = 0;

    for (int i = 0; i < *cardCount; i++)
    {
        wonCards[i] = 1;
    }

    for (int i = 0; i < *cardCount; i++)
    {
        struct MatchingNumbersResult matches = findMatchingNumbersForCard(cards[i]);
        matchCount = matches.size;

        for (int j = 1; j < matchCount + 1; j++)
        {
            wonCards[i + j] += 1 * wonCards[i];
        }
    }

    int sum = 0;

    for (int i = 0; i < sizeof(wonCards) / sizeof(wonCards[0]); i++)
    {
        sum += wonCards[i];
    }

    return sum;
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

    int cardCount;
    struct Card *cards = parseCards(file, &cardCount);

    printf("Part one: %d\n", scoreAcrossCards(cards, &cardCount));
    printf("Part two: %d\n", scratchCardsWon(cards, &cardCount));

    free(cards);
    fclose(file);

    return 0;
}