// games/DiceRollingGame/src/Main.java
//AdoptOpenJDk 15
// Jefaxe

//imports
import java.util.Locale;
import java.util.Random;
import java.util.Scanner;


public class Main{
    public static void main(String[] args){
        Random myRandom = new Random();
        //ask for player 1's name
        Scanner keyboard = new Scanner(System.in);
        System.out.println("PLAYER 1: What is your name?");
        String Player1_name = keyboard.nextLine();
        System.out.println("PLAYER 2: What is your name?");
        String Player2_name = keyboard.nextLine();
        System.out.println("MASTER: how many rolls per player?");
        Integer numberOfRolls = keyboard.nextInt();
        //define the dice array
        int[] dicePlayer1 = new int[numberOfRolls]; //this is an integer array of size 3
        int[] dicePlayer2 = new int[numberOfRolls]; //this is an integer array of size 3

        String decsion;
        for (int i=0; i<numberOfRolls; i++){
            //ask for player 1
            System.out.println(Player1_name+" : Press ENTER to roll, or type SKIP to skip this roll and keep your current score");
            decsion = keyboard.nextLine().toUpperCase();
            if(decsion.equals("SKIP")){
                System.out.println("SKipping dice roll...");
            }
            else{
                dicePlayer1[i]=myRandom.nextInt(6)+1;
            }
            //ask for player 2
            System.out.println(Player2_name+" : Press ENTER to roll, or type SKIP to skip this roll and keep your current score");
            decsion = keyboard.nextLine().toUpperCase();
            if(decsion.equals("SKIP")){
                System.out.println("SKipping dice roll...");
            }
            else{
                dicePlayer2[i]=myRandom.nextInt(6)+1;
            }
        }
        int Player1_total = 0;
        int Player2_total =0;
        for(int i=0; i< dicePlayer1.length; i++){
            Player1_total=Player1_total+
        }
        keyboard.close();


    }
}