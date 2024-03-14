#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX 9

typedef struct
{
    string name;
    int votes;
} candidate;

candidatecandidates[MAX];

int candidate_count;

bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{

    if (argc < 2)
    {
        printf("usage: plurality [candidate ...]\n");
        return 1;
    }

    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i \n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }
    int voter_count = get_int("Number of voters:");

    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote:");
        if (!vote(name))
        {
            printf("Invalid vote . \n");
        }
    }
    print_winner();
}

bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].vtes++;
            return true;
        }
    }
    return false;
}
void print_winner()
{
    int max_votes = candidates[0].votes;
    for (int i = 0; i < candidate_count; i++)
    {
        max_votes = candidates[i].votes;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == max_votes)
        {
            printf("%s \n", candidates[i].name);
        }
    }
}