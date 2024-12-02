package LogIn;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Validation {

    class LogInValidation {
        public String lengthCellPhoneNumber(String cellPhone) {
            if (cellPhone == null || cellPhone.length() != 11) {
                return "Cell phone number must be 11 digits.";
            }
            return "";
        }

        public String lengthPinNumber(String pinNumber) {
            if (pinNumber == null || pinNumber.length() != 4) {
                return "PIN must be 4 digits.";
            }
            return "";
        }
    }

    class RegisterValidation {
        public String nameValidation(String name) {
            if (name == null || name.trim().isEmpty()) {
                return "Name cannot be empty.";
            }
            return "";
        }

        public String addressValidate(String address) {
            if (address == null || address.length() <= 20) {
                return "Address must be more than 20 characters.";
            }
            return "";
        }

        public String dateBirthdayFormatValidate(String birthday) {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            sdf.setLenient(false);
            try {
                Date date = sdf.parse(birthday);
                if (date.after(new Date())) {
                    return "Birthday cannot be in the future.";
                }
                return "";
            } catch (ParseException e) {
                return "Invalid date format. Use yyyy-MM-dd.";
            }
        }
    }
}
