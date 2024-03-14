#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_qua(int cents);
int calculate_dimes(int cents);
int calculate_nick(int cents);
int calculate_pen(int cents);

int main(void)
{
    
    int cents = get_cents();

    
    int quarters = calculate_qua(cents);
    cents = cents - quarters * 25;

   
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

   
    int nickels = calculate_nick(cents);
    cents = cents - nickels * 5;

    
    int pennies = calculate_pen(cents);
    cents = cents - pennies * 1;

   
    int coins = quarters + dimes + nickels + pennies;

    
    printf("%i\n", coins);
}

int get_cents(void)
{

    int no_cents;
    do
    {
        no_cents = get_int("Change owed: ");
    }
    while (no_cents < 0);
    return no_cents;
}

int calculate_qua(int cents)
{
    
    int quarters = cents / 25;
    return quarters;
}

int calculate_dimes(int cents)
{
   
    int dimes = cents / 10;
    return dimes;
}

int calculate_nick(int cents)
{
   
    int nickels = cents / 5;
    return nickels;
}

int calculate_pen(int cents)
{
   
    return cents;
}