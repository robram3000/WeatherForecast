package LogIn;

public class Validation {


    class LogInValidation{
        public String LengthCellPhoneNumber(String CellPhone){
            int CountingCpNoElements = CellPhone.length();
            if(CountingCpNoElements != 11){
                return "Number Must 11 Numbers";
            }
            return "Phonumber Valid";
        }
        public String LengthPinNumber(String PinNumber)
        {
            int CountringPinNumber = PinNumber.length();
            if(CountringPinNumber != 4){
                return  "Number Pin Must 4 Numbers";
            }
            return "Pin No Valid";
        }
    }



}
