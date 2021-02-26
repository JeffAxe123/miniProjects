package src;
import java.util.Random;
import java.util.Scanner;
public class Main {
  static int IsItAnImposter(String prompt, Scanner keyboard){
    while(true) {
        try{
          System.out.print(prompt);
          int integer = keyboard.nextInt();
          return integer;
        }
        catch(Exception e){
            System.out.println("ERROR:Your input was not a valid integr");
        }
    }
  }

  static int insideRange(int RangeOfValues){
    do{
      int userNumber = IsItAnImposter("Enter a number between 1 and "+RangeOfValues+" ", new Scanner(System.in));
      if(userNumber>RangeOfValues){
        System.out.println("CORRECTION: number must be bellow "+RangeOfValues+" ");
      }
      else if(userNumber<1){
        System.out.println("CORRECTION: number must be above 1 ");
      }
      else{
        return userNumber;
      }
    }
    while(true);
    
  }
    
    public static void main(String[] args) {
      //sets up a Random instance
      Random r= new Random();
      //sets the number of chances
      int lives = IsItAnImposter("please enter the number of lives you wish to have for this turn (recommended: 10) ",new Scanner(System.in));
      int RangeOfValues = IsItAnImposter("please enter the range of values for this game. It will be between 1 and you chosen number (recommended: 10) ", new Scanner(System.in));
      //the computer's generated number
      int ComputerNumber = r.nextInt(RangeOfValues)+1;
      boolean AnswerIsCorrect=false;
      boolean IsDead=false;
      while(AnswerIsCorrect==false || IsDead==false){
        System.out.println("You have "+lives+" lives left");
        //asks the user for a number
        int userNumber=insideRange(RangeOfValues);
        
        // test for perfect score
        if(userNumber==ComputerNumber){
          //win state
          System.out.println("You win!");
          AnswerIsCorrect=true;
          break;
        }
        else if(userNumber<ComputerNumber){
          //too low state
          System.out.println("Too low!");
          lives--;
        }
        else if(userNumber>ComputerNumber){
          //too high state
          System.out.println("Too high!");
          lives--;
        }
        if(lives<=0){
          //you're dead!
          IsDead=true;
          System.out.println("You died!");
          break;
        }
        
      }
    }
      
  }