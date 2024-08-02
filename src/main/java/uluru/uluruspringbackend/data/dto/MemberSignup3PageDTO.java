package uluru.uluruspringbackend.data.dto;

import lombok.Data;
import uluru.uluruspringbackend.data.embed.Address;

@Data
public class MemberSignup3PageDTO {

    private String email;
    private Address address;
    private String emergencyContact;
}