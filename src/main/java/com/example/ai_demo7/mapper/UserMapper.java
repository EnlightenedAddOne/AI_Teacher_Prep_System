package com.example.ai_demo7.mapper;


import com.example.ai_demo7.entity.User;
import org.apache.ibatis.annotations.*;

@Mapper
public interface UserMapper {
    @Select("SELECT * FROM users WHERE username = #{username}")
    User findByUsername(String username);

    @Insert("INSERT INTO users (username, password, role) VALUES (#{username}, #{password}, #{role})")
    void insert(User user);

    @Delete("DELETE FROM users WHERE username = #{username}")
    void deleteByUsername(String username);

    @Update("UPDATE users SET password=#{password}, role=#{role} WHERE username=#{username}")
    void updateByUsername(User user);
}
