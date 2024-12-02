package LogIn;



import javax.swing.*;
import java.util.*;

public class Main {

    public Scanner scan = new Scanner(System.in);
    public static Main Interface = new Main();
    public static Validation.LogInValidation LogInValidate = new Validation().new LogInValidation();

    public static void main(String[] args) {
        Interface.SwiftPayInteface();
    }


    public void SwiftPayInteface(){
        System.out.println("\n============ SwiftPay ============ \n");
        System.out.print("[1] LogIn\n");
        System.out.print("[2] Register\n");
        System.out.print("[3] Exit\n");

        int UIChoice = scan.nextInt();
        scan.nextLine();

        switch (UIChoice){
            case 1 :
                Interface.LoginInterface();
                break;
            case 2 :
                Interface.RegisterAccount();
                break;
            case 3 :
                System.exit(0);
                break;
            default:
        }


    }

    private void RegisterAccount(){
        System.out.println("============ SwiftPay ============ \n");

        System.out.print("Enter Your Fullname :");
        String Fullname = scan.nextLine();



    }

    private void LoginInterface() {
        System.out.println("============ SwiftPay ============ \n");

        System.out.print("Enter your CellphoneNo: ");
        String CpNo = scan.nextLine();

        while (true) {
            if (CpNo.isEmpty()) {
                System.out.println("CellphoneNumber is Empty");
                return;
            } else {
                System.out.println(LogInValidate.LengthCellPhoneNumber(CpNo));
                break;
            }
        }

        System.out.print("Enter Your PinNumber: ");
        String PinNo = scan.nextLine();
        System.out.println(LogInValidate.LengthPinNumber(PinNo));
    }




}