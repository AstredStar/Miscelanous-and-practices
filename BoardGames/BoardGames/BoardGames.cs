using System;
using System.Runtime.InteropServices;
namespace BoardGames
{
    class BoardGames
    {
        static void Main(string[] args)
        {
            Backgammon foo = new();

            foo.SetupBoard();

            foo.ConsoleDisplayBoard();

            foo.ConsoleDisplayDice();
            foo.RollDice();
            foo.ConsoleDisplayDice();

            return;
        }
    }
}
