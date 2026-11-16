package com.driveease.service;

import com.driveease.dto.RegisterRequest;
import com.driveease.dto.UserDto;
import com.driveease.model.User;
import java.util.List;

public interface UserService {

    User registerCustomer(RegisterRequest request);

    User findByEmail(String email);

    User findById(Long id);

    boolean existsByEmail(String email);

    List<UserDto> getAllCustomers();

    UserDto getCurrentUserDto(String email);
}
