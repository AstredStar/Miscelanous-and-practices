using System;

namespace BoardGames
{
    class Backgammon
    {

        /// <summary>
        /// ------------- Logic and Data ----------------------------------------------------------------------
        /// </summary>
        
        #region instance members

        public readonly Random random = new();
        public static readonly sbyte[] BASEBOARD = { 0,       // length 28, [0,25] killed pieces | [0]-> white, [25]-> black
                                 2, 0, 0, 0, 0,-5,
                                 0,-3, 0, 0, 0, 5,
                                -5, 0, 0, 0, 3, 0,            // [1:24] pieces in active play
                                 5, 0, 0, 0, 0,-2,
                                 0,
                                 0 , 0};                      // [26,27] pieces in home | [26]-> white, [27]-> black

        public sbyte[] board = new sbyte[28];           // 28 bytes
        public byte[] dice = new byte[4];               // 32 bytes   + 4
        public uint[] scores = new uint[2];          // 40 bytes      + 8

        public ushort round; // values of 0 (white) and 1 (black) indicate last matches winner.
                                // also indicates that no game is ongoing
                                                           // 42 bytes

        public sbyte pcolor; // 1 for white, -1 for black    // 43 bytes
        public byte stakes;                                    // 44 bytes 

        #endregion
        
        public void SetFirstPlayer(int whiteorblack)
        {
            round = 2; // round 1, turn 0

            whiteorblack &= 0xffff; // budget absolute value

            if (whiteorblack > 1) whiteorblack = random.Next(0, 2);

            pcolor = (sbyte)(1 - whiteorblack * 2);
        }

        public void SetupBoard()
        {
            for (byte i = 0; i < 28; i++)
            {
                board[i] = BASEBOARD[i];
            }
            stakes = 0;
            round = 2;   // round 1, turn 0
        }

        public void RollDice()
        {
            dice[0] = (byte)random.Next(1, 7);
            dice[1] = (byte)random.Next(1, 7);

            if (dice[0] == dice[1])
            {
                dice[2] = dice[0];
                dice[3] = dice[0];
            }
        }

        public void NextRound()
        {
            if (!InProgress())
            {
                throw new InvalidOperationException("Backgammon.NextRound called outside of an ongoing game.");
            }
            round++;
            pcolor *= -1;
        }

        public void SetScores(ushort white=0,ushort black=0)
        {
            scores[0] = white;
            scores[1] = black;
        }

        public bool InProgress()
        {
            if (round < 2) return false;
            else return true;
        }

        public sbyte GetWinner()
        {
            if (round == 0) return 1;       // white win
            else if (round == 1) return -1; // black win
            else return 0;                  // no winner
        }

        public uint CheckNormalWin()
        {
            int friendlybase;
            if (pcolor == 1) friendlybase = 26;
            else friendlybase = 27;
            int enemybase = (26 + 27) - friendlybase;

            if (board[friendlybase]*pcolor == 15)
            {
                if (board[enemybase] == 0) return 2;
                else return 1;
            }
            return 0;
        }

        public uint CheckTechnicalWin()
        {
            int houseptr;
            if (pcolor == 1) houseptr=1;
            else houseptr = 19;
            
            for (int i = houseptr+1; i <= houseptr+6; i++)
            {
                if (board[i] != board[houseptr]) return 0;
            }
 
            int budgetabsvalue = board[houseptr];            // poormans absolute value
            if (budgetabsvalue < 0) budgetabsvalue *= -1;    // need to convert to int anyway to convert it to uint. C# is weird

            return (uint)budgetabsvalue;
        }

        public void UpdateWin() // Checks if there is a winner, updates game status accordingly
        {
            uint winnings = CheckNormalWin() + CheckTechnicalWin();  // only one function will ever return a nonzero value
            if (winnings == 0) return;              // no winner
            if (pcolor == 1) round = 0;             // white is winner
            else round = 1;                         // black is winner
            scores[round] += (winnings << stakes);
        }

        //
        // -----------------------------UNFINISHED--------------------------------------------------------------------
        //

        public bool IsValidMove(int startpos, int endpos)
        {
            if (!(0 < startpos & startpos < 25)) return false;

            if (board[startpos] * pcolor < 1) return false; // start pos must have atleast 1 friendly unit
            if (board[endpos] * pcolor < -1) return false;  // end pos cant have more than 1 enemies

            return true;
        }

        public bool HandleDice(int startpos, int endpos)
        {
            if (!(0 < endpos & endpos < 25)) //anything out of bounds is assumned to be home
            {
                if (pcolor == 1) endpos = 0;
                else endpos = 25;
            }
            
            return true;

        }

        public bool ValidMoveExists() { return true; }

        /// <summary>
        /// ----------------Console commands--------------------------------------------------------------------
        /// </summary> 
        public void ConsoleDisplayTurn()
        {
            int round = this.round >> 1;

            Console.WriteLine("Round " + round.ToString());

            string playercolor;

            if (pcolor == 1) playercolor = "White";
            else playercolor = "Black";

            Console.WriteLine(playercolor + "'s turn to play");
        }

        public void ConsoleSetFirstPlayer()
        {
            Console.WriteLine("Who goes first?\n1-White\n2-Black\n3-Random\n");
            ushort holder = Convert.ToUInt16(Console.ReadLine());
            holder--;

            SetFirstPlayer(holder);

            if (pcolor == 1) Console.WriteLine("White goes first\n");
            else Console.WriteLine("Black goes first\n");
        }

        public void ConsoleDisplayScores()
        {
            Console.WriteLine("White " + String.Join("  :  ", scores) + " Black\n");
        }

        public void ConsoleDisplayWinner()
        {
            switch (GetWinner())
            {
                case 0:
                    Console.WriteLine("White wins!\n");
                    break;
                case 1:
                    Console.WriteLine("Black wins!\n");
                    break;
                default:
                    throw new InvalidOperationException("ConsoleDisplayWinner called on an unfinished match.");
            }

        }

        public void ConsoleDisplayBoard()
        {
            /*
                     board =   { 0,
                                 2, 0, 0, 0, 0,-5,
                                 0,-3, 0, 0, 0, 5,
                                -5, 0, 0, 0, 3, 0,
                                 5, 0, 0, 0, 0, 2,
                                 0,
                                 0, 0 };
 
            */
            const int length = 14 * 6+4;
            String horisontal_bar = new('-', length);

            Console.Write("\n\n\t");

            for(int i = 12; i > 0; i--)
            {
                Console.Write($"{i,-6}");
                if (i == 7) Console.Write($"{"|   |",-10}");                  //!!!
            }
            Console.WriteLine($"{0,5}");

            Console.WriteLine($"{horisontal_bar,length+3}");

            Console.Write($"{"|",4}{"",4}");

            for(int i = 12; i > 0; i--)
            {
                Console.Write($"{board[i],-6}");    
                if (i == 7) Console.Write($"{"|",-2}{board[0],-2}{"|",-6}");                  //!!!
            }
            Console.Write($"{"|",0}{board[27],4}\n");
            Console.Write($"{"|",4}{"|   |",45}{"|",42}\n");                  //!!!
            Console.Write($"{"|",4}{"",4}");

            for (int i = 13; i < 25; i++)
            {
                Console.Write($"{board[i],-6}");
                if (i == 18) Console.Write($"{"|",-2}{board[25],-2}{"|",-6}");                  //!!!
            }
            Console.WriteLine($"{"|",0}{board[26],4}");

            Console.WriteLine($"{horisontal_bar,length + 3}");

            Console.Write('\t');

            for (int i = 13; i < 25; i++)
            {
                Console.Write($"{i,-6}");
                if (i == 18) Console.Write($"{"|   |",-10}");                  //!!!
            }
            Console.Write($"{25,5}\n");
            Console.WriteLine();
        }

        public void ConsoleDisplayDice()
        {
            Console.WriteLine($"Dice: " + string.Join(" ", dice));
            Console.WriteLine($"Stakes: {Math.Pow(2,stakes)}");
        }
        //
        // ---------------------UNFINISHED--------------------------------------------------------------------
        //
        public void ConsolePlayRound()
        {

        }

        public void ConsolePlayMatch()
        {

            ConsoleSetFirstPlayer();

            SetupBoard();

            ConsolePlayRound();

            while (InProgress() )
            {

                NextRound();

                ConsolePlayRound();

                UpdateWin();

            }
             
            ConsoleDisplayWinner();

            ConsoleDisplayScores();

            Console.WriteLine("End of execution");
        }

    }

}