package com.example.ai_demo7.mapper;


import com.example.ai_demo7.entity.User;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserMapper {
    @Select("SELECT * FROM users WHERE username = #{username}")
    User findByUsername(String username);

//    @Insert("INSERT INTO users (username, password, role) VALUES (#{username}, #{password}, #{role})")
//    void insert(User user);

    @Delete("DELETE FROM users WHERE username = #{username}")
    void deleteByUsername(String username);

    @Update("UPDATE users SET password=#{password}, role=#{role} WHERE username=#{username}")
    void updateByUsername(User user);

    @Select("SELECT * FROM users WHERE created_by = #{createdBy}")
    List<User> findByCreatedBy(String createdBy);

    @Select("SELECT * FROM users")
    List<User> findAll();

    @Insert("INSERT INTO users (username, password, role, created_by) VALUES (#{username}, #{password}, #{role}, #{createdBy})")
    void insert(User user);

    @Update("UPDATE users SET created_by = #{createdBy} WHERE username = #{username}")
    void updateCreatedBy(@Param("username") String username,
                         @Param("createdBy") String createdBy);
}
